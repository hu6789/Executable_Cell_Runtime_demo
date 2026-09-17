from typing import Dict

from shell.world import World
from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import NodeState

def get_shh_for_cell(
    world: World,
    cell_id: str,
) -> float:
    """
    Read the current extracellular SHH concentration at one cell.

    Shell owns the conversion from World SHH field to
    InternalNet-facing input.
    """

    source = world.state.shh_field.sources.get(cell_id)

    if source is None:
        raise KeyError(
            "SHH position not found for cell: {}".format(cell_id)
        )

    position, _ = source

    return world.shh_concentration(position)


def shh_to_ptch1(
    shh_concentration: float,
    K_shh: float = 1.0,
    n: float = 2.0,
) -> Dict[str, float]:
    """
    Convert extracellular SHH concentration into PTCH1 state.

    Demo abstraction:

        PTCH1_inactive =
            SHH^n / (K_shh^n + SHH^n)

        PTCH1_active =
            1 - PTCH1_inactive

    This is a Shell-side external-input conversion.
    InternalNet does not know about SHH.
    """

    if K_shh <= 0:
        raise ValueError("K_shh must be positive")

    if n <= 0:
        raise ValueError("n must be positive")

    if shh_concentration < 0:
        raise ValueError(
            "shh_concentration must not be negative"
        )

    shh_power = shh_concentration ** n
    K_power = K_shh ** n

    inactive = shh_power / (K_power + shh_power)
    active = 1.0 - inactive

    return {
        "active": active,
        "inactive": inactive,
    }


def get_ptch1_input(
    world: World,
    cell_id: str,
) -> Dict[str, float]:
    """
    Build the PTCH1 input for one cell.

    A cell receives SHH-derived PTCH1 input only when
    its current World label contains 'PTCH1'.
    """

    cell = world.get_cell(cell_id)

    if "PTCH1" not in cell.labels:
        return {}

    shh = get_shh_for_cell(
        world=world,
        cell_id=cell_id,
    )

    return shh_to_ptch1(shh)
    
    
def build_runtime_input(
    world: World,
    cell_id: str,
) -> Runtime:
    """
    Build the InternalNet Runtime input for one cell.

    Shell converts World-level external information into
    InternalNet-facing Runtime state.

    Currently only PTCH1 external input is supported.
    """

    cell = world.get_cell(cell_id)

    runtime = Runtime(
        id=cell.id,
        type=cell.type,
        node_states=dict(cell.nodes),
        gene_states=dict(cell.genes),
    )

    ptch1_input = get_ptch1_input(
        world=world,
        cell_id=cell_id,
    )

    if ptch1_input:
        shh = get_shh_for_cell(
            world=world,
            cell_id=cell_id,
        )
        
        
        print(
            "  [EXTERNAL INPUT] Cell {}: SHH={:.4f} -> PTCH1 active={:.4f}, inactive={:.4f}".format(
                cell_id,
                shh,
                ptch1_input["active"],
                ptch1_input["inactive"],
            )
        )
        
        runtime.set_node(
            NodeState(
                name="PTCH1",
                total=1.0,
                states=ptch1_input,
            )
        )

    return runtime
