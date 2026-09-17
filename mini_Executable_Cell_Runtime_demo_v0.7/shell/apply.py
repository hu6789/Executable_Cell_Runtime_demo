from internalnet.hir.schema import HIROutput
from shell.world import World
from internalnet.runtime.state import NodeState

def apply_hir_output(
    world: World,
    cell_id: str,
    output: HIROutput,
) -> None:
    """
    Apply one cell's HIROutput to World.

    id is used only to locate the target cell and is never modified.

    Applied outputs:
    - BehaviorRuntimeState -> node/gene states
    - labels -> current-tick labels
    - external SHH effects -> SHH field

    Type update is intentionally deferred.
    """

    cell = world.get_cell(cell_id)

    # ---------------------------------------------------------
    # 1. BehaviorRuntimeState -> World state
    # ---------------------------------------------------------
    for runtime_state in output.behaviors.values():
        internal_output = runtime_state.internal_outputs
 
        if not internal_output:
            continue

        target = internal_output.get("target")
        state = internal_output.get("state")

        if state == "total":
            if target not in cell.nodes:
                raise KeyError(
                    "Node target not found in cell: {}".format(target)
                )

            current_node = cell.nodes[target]

            cell.nodes[target] = NodeState(
                name=current_node.name,
                total=runtime_state.value,
                states=dict(current_node.states),
            )

        elif state == "free":
            if target not in cell.nodes:
                raise KeyError(
                    "Node target not found in cell: {}".format(target)
                )

            current_node = cell.nodes[target]
            states = dict(current_node.states)
            states["free"] = runtime_state.value

            cell.nodes[target] = NodeState(
                name=current_node.name,
                total=current_node.total,
                states=states,
            )
            
            print(
                "  [WORLD UPDATE] Cell {}: {}.{} <- {:.4f}".format(
                    cell_id,
                    target,
                    state,
                    runtime_state.value,
                )
            )
            
    # ---------------------------------------------------------
    # 2. Labels -> current-tick labels
    #
    # Labels are tick-based:
    # overwrite instead of accumulating.
    # ---------------------------------------------------------
    cell.labels = set(output.labels)

    # ---------------------------------------------------------
    # 3. External effects -> World
    #
    # HIR describes the external effect.
    # Shell applies it to World.
    # ---------------------------------------------------------
    for effect in output.external_effects.values():
        if effect.effect_type != "extracellular":
            continue

        if effect.target != "SHH":
            continue

        source = world.state.shh_field.sources.get(cell_id)

        if source is None:
            raise KeyError(
                "SHH source position not found for cell: {}".format(
                    cell_id
                )
            )

        position, _ = source

        world.state.shh_field.set_source(
            cell_id=cell_id,
            position=position,
            amount=effect.value,
        )
        
        print(
            "  [WORLD UPDATE] Cell {}: SHH source <- {:.4f}".format(
                cell_id,
                effect.value,
            )
        )

    # ---------------------------------------------------------
    # 4. Type update
    #
    # Deferred until AC is implemented.
    # ---------------------------------------------------------
