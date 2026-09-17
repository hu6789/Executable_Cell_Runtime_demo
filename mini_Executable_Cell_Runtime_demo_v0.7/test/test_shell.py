import math

from internalnet.runtime.state import GeneState, NodeState
from shell.schema import CellState, WorldState
from shell.shh_field import SHHField
from shell.input import (
    get_shh_for_cell,
    shh_to_ptch1,
    get_ptch1_input,
    build_runtime_input,
)
from internalnet.compute_plan.builder import ComputePlanBuilder
from internalnet.graph_engine.engine import GraphEngine
from internalnet.graph_engine.repository import GraphRepository
from internalnet.graph_engine.schema import GraphDefinition, GraphEdge
from internalnet.node_engine.engine import NodeEngine
from internalnet.node_engine.repository import NodeRepository
from internalnet.node_engine.schema import NodeDefinition
from internalnet.passive_engine.engine import PassiveEngine
from internalnet.passive_engine.repository import PassiveRepository
from internalnet.runtime.merger import RuntimeMerger
from internalnet.internalnet import InternalNet
from internalnet.gene_engine.schema import GeneDefinition
from internalnet.gene_engine.repository import GeneRepository
from internalnet.gene_engine.engine import GeneEngine
from shell.apply import apply_hir_output

def test_cell_state():
    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        nodes={
            "SHH": NodeState(
                name="SHH",
                total=1.0,
            )
        },
        genes={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.5,
            )
        },
        labels={"floor_plate"},
    )

    assert cell.id == "B"
    assert cell.type == "floor_plate_progenitor"
    assert cell.nodes["SHH"].total == 1.0
    assert cell.genes["FOXA2"].value == 0.5
    assert "floor_plate" in cell.labels


def test_world_state():
    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
    )

    shh_field = SHHField(
        decay_length=1.0
    )

    shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=1.0,
    )

    world = WorldState(
        cells={"B": cell},
        shh_field=shh_field,
    )

    assert "B" in world.cells
    assert world.cells["B"].id == "B"
    assert world.shh_field.concentration_at(0.0) == 1.0
    
from shell.shh_field import SHHField


def test_shh_field_single_source():
    field = SHHField(decay_length=1.0)

    field.set_source(
        cell_id="B",
        position=0.0,
        amount=1.0,
    )

    assert field.concentration_at(0.0) == 1.0


def test_shh_field_distance_decay():
    field = SHHField(decay_length=1.0)

    field.set_source(
        cell_id="B",
        position=0.0,
        amount=1.0,
    )

    concentration = field.concentration_at(1.0)

    assert abs(concentration - math.exp(-1.0)) < 1e-9


def test_shh_field_multiple_sources():
    field = SHHField(decay_length=1.0)

    field.set_source("B", 0.0, 1.0)
    field.set_source("X", 2.0, 1.0)

    concentration = field.concentration_at(1.0)

    expected = 2.0 * math.exp(-1.0)

    assert abs(concentration - expected) < 1e-9
    
from shell.world import World


def test_world_add_and_get_cell():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
    )

    world.add_cell(cell)

    assert world.get_cell("B") is cell


def test_world_shh_concentration():
    world = World()

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=1.0,
    )

    assert world.shh_concentration(0.0) == 1.0


def test_world_rejects_duplicate_cell():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
    )

    world.add_cell(cell)

    try:
        world.add_cell(cell)
        assert False
    except ValueError:
        pass
        
from internalnet.hir.schema import (
    BehaviorExternalEffect,
    BehaviorRuntimeState,
    HIROutput,
)


def test_apply_hir_output_applies_behavior_output_to_node():
    from shell.apply import apply_hir_output

    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        nodes={
            "SHH": NodeState(
                name="SHH",
                total=1.0,
            )
        },
        genes={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.2,
            )
        },
        labels={"old_label"},
    )

    world.add_cell(cell)

    output = HIROutput(
        behaviors={
            "production:SHH": BehaviorRuntimeState(
                behavior_name="production",
                source_type="gene",
                source_name="SHH",
                node_states={},
                gene_states={},
                value=2.0,
                internal_outputs={
                    "target": "SHH",
                    "state": "total",
                },
            )
        },
        labels={"new_label"},
    )

    apply_hir_output(
        world=world,
        cell_id="B",
        output=output,
    )

    assert world.get_cell("B").id == "B"

    assert world.get_cell("B").nodes["SHH"].total == 2.0

    assert world.get_cell("B").genes["FOXA2"].value == 0.2

    assert world.get_cell("B").labels == {"new_label"}
    
def test_apply_hir_output_releases_shh_to_field():
    from shell.apply import apply_hir_output

    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
    )

    world.add_cell(cell)

    # Existing spatial position of cell B.
    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=0.0,
    )

    output = HIROutput(
        external_effects={
            "release:SHH": BehaviorExternalEffect(
                behavior_name="release",
                effect_type="extracellular",
                target="SHH",
                value=0.8,
            )
        }
    )

    apply_hir_output(
        world=world,
        cell_id="B",
        output=output,
    )

    assert world.state.shh_field.sources["B"] == (0.0, 0.8)
    assert world.shh_concentration(0.0) == 0.8
    
def test_get_shh_for_cell():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        labels={"PTCH1"},
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    assert get_shh_for_cell(world, "B") == 2.0


def test_shh_to_ptch1_zero_shh():
    ptch1 = shh_to_ptch1(0.0)

    assert ptch1["active"] == 1.0
    assert ptch1["inactive"] == 0.0


def test_shh_to_ptch1_one_shh():
    ptch1 = shh_to_ptch1(1.0)

    assert abs(ptch1["active"] - 0.5) < 1e-9
    assert abs(ptch1["inactive"] - 0.5) < 1e-9


def test_shh_to_ptch1_high_shh():
    ptch1 = shh_to_ptch1(2.0)

    assert abs(ptch1["active"] - 0.2) < 1e-9
    assert abs(ptch1["inactive"] - 0.8) < 1e-9


def test_cell_without_ptch1_label_receives_no_ptch1_input():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        labels=set(),
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    assert get_ptch1_input(world, "B") == {}


def test_cell_with_ptch1_label_receives_ptch1_input():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        labels={"PTCH1"},
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    ptch1 = get_ptch1_input(world, "B")

    assert abs(ptch1["active"] - 0.2) < 1e-9
    assert abs(ptch1["inactive"] - 0.8) < 1e-9
    
    
def test_build_runtime_input_with_ptch1():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        labels={"PTCH1"},
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    runtime = build_runtime_input(world, "B")

    assert runtime.id == "B"
    assert runtime.type == "floor_plate_progenitor"
    assert runtime.has_node("PTCH1")

    ptch1 = runtime.get_node("PTCH1")

    assert ptch1.total == 1.0
    assert abs(ptch1.states["active"] - 0.2) < 1e-9
    assert abs(ptch1.states["inactive"] - 0.8) < 1e-9


def test_build_runtime_input_without_ptch1():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        labels=set(),
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    runtime = build_runtime_input(world, "B")

    assert runtime.id == "B"
    assert runtime.type == "floor_plate_progenitor"
    assert not runtime.has_node("PTCH1")
    
def test_shell_runtime_enters_internalnet_node_stage():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        nodes={
            "SMO": NodeState(
                name="SMO",
                total=1.0,
                states={
                    "unrecruited": 1.0,
                    "recruited": 0.0,
                },
            ),
            "GLI2": NodeState(
                name="GLI2",
                total=1.0,
                states={
                    "SUFU_bound": 1.0,
                    "free": 0.0,
                    "nuclear": 0.0,
                },
            ),
        },
        labels={"PTCH1"},
    )

    world.add_cell(cell)

    world.state.shh_field.set_source(
        cell_id="B",
        position=0.0,
        amount=2.0,
    )

    graph = GraphDefinition(
        name="ptch1_smo",
        type="common",
        nodes=["PTCH1", "SMO", "GLI2"],
        genes=[],
        
        edges=[
            GraphEdge(
                name="PTCH1_SMO",
                type="node-node",
                source="PTCH1",
                target="SMO",
            ),
            GraphEdge(
                name="SMO_GLI2",
                type="node-node",
                source="SMO",
                target="GLI2",
            ),
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)

    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="B",
        graph_ids=["ptch1_smo"],
    )

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="PTCH1",
                category="receptor",
                polymorphism=["active", "inactive"],
            ),
            NodeDefinition(
                name="SMO",
                category="functional_protein",
                polymorphism=["unrecruited", "recruited"],
                formulation={
                    "type": "hill_inhibition",
                    "input": "PTCH1",
                    "state_mapping": {
                        "active": 1.0,
                        "inactive": 0.0,
                    },
                    "equation": (
                        "A_SMO = 1 / "
                        "(1 + (I_PTCH1 / K_PTCH1)^n)"
                    ),
                    "parameters": {
                        "K_PTCH1": 0.5,
                        "n": 2.0,
                        "theta_SMO": 0.5,
                    },
                    "transition": {
                        "from": "unrecruited",
                        "to": "recruited",
                        "condition": "A_SMO >= theta_SMO",
                    },
                },
            ),
            
            NodeDefinition(
                name="GLI2",
                category="functional_protein",
            )
        ]
    )

    internal_net = InternalNet(
        node_engine=NodeEngine(node_repository),
        passive_engine=PassiveEngine(
            passive_repository=PassiveRepository(),
            node_repository=node_repository,
        ),
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
    )

    runtime = build_runtime_input(
        world=world,
        cell_id="B",
    )

    node_runtime = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    assert node_runtime.has_node("PTCH1")
    assert node_runtime.has_node("SMO")

    ptch1 = node_runtime.get_node("PTCH1")
    smo = node_runtime.get_node("SMO")

    assert abs(ptch1.states["active"] - 0.2) < 1e-9
    assert abs(ptch1.states["inactive"] - 0.8) < 1e-9

    assert node_runtime.has_node("GLI2")

    gli2 = node_runtime.get_node("GLI2")

    assert gli2.states["SUFU_bound"] == 1.0
    assert gli2.states["free"] == 0.0
    assert gli2.states["nuclear"] == 0.0
    

def test_shell_runs_full_internalnet_tick():
    class FakeHIREngine:
        def run(
            self,
            plan,
            node_states,
            gene_states,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        ):
            # HIR receives the final InternalNet runtime.
            assert "H3K27ac" in node_states
            assert "FOXA2" in gene_states

            return HIROutput(
                labels={"FOXA2"},
                type_name="floor_plate_progenitor",
            )

    # ---------------------------------------------------------
    # 1. World
    # ---------------------------------------------------------
    world = World(
        state=WorldState(),
        shh_field=SHHField(),
    )

    cell = CellState(
        id="cell_shell_full_tick",
        type="floor_plate_progenitor",
        nodes={
            "H3K27ac": NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            ),
        },
        genes={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            ),
        },
        labels={"PTCH1"},
    )

    world.add_cell(cell)

    # Extracellular SHH source for this cell.
    world.state.shh_field.set_source(
        cell_id="cell_shell_full_tick",
        position=0.0,
        amount=2.0,
    )

    # ---------------------------------------------------------
    # 2. Graph / ComputePlan
    # ---------------------------------------------------------
    graph = GraphDefinition(
        name="shell_full_tick_graph",
        type="common",
        nodes=["PTCH1", "H3K27ac"],
        genes=["FOXA2"],
        edges=[
            GraphEdge(
                name="H3K27ac_FOXA2",
                type="node-gene",
                source="H3K27ac",
                target="FOXA2",
            ),
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)

    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_shell_full_tick",
        graph_ids=["shell_full_tick_graph"],
    )

    # ---------------------------------------------------------
    # 3. InternalNet repositories
    # ---------------------------------------------------------
    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="PTCH1",
                category="receptor",
            ),
            NodeDefinition(
                name="H3K27ac",
                category="epigenetic_mark",
            ),
        ]
    )

    gene_repository = GeneRepository(
        [
            GeneDefinition(
                name="FOXA2",
                elements=[
                    {
                        "name": "FOXA2_Gli_Response_Enhancer",
                        "category": "enhancer",
                        "effect": "activation",
                        "value": 1.0,
                        "distance": 1000,
                    },
                ],
                formula={
                    "equation": (
                        "R = H_nuclear^n / "
                        "(K_H^n + H_nuclear^n)"
                    ),
                    "parameters": {
                        "H_nuclear": "H3K27ac.states.nuclear",
                        "K_H": 0.5,
                        "n": 2,
                    },
                    "output": "lysine_modification",
                },
            ),
        ]
    )

    fake_hir = FakeHIREngine()

    internal_net = InternalNet(
        node_engine=NodeEngine(node_repository),
        passive_engine=PassiveEngine(
            passive_repository=PassiveRepository(),
            node_repository=node_repository,
        ),
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
        gene_engine=GeneEngine(gene_repository),
        gene_repository=gene_repository,
        hir_engine=fake_hir,
    )

    # ---------------------------------------------------------
    # 4. Shell -> InternalNet
    # ---------------------------------------------------------
    runtime = build_runtime_input(
        world,
        "cell_shell_full_tick",
    )

    # SHH is converted by Shell into PTCH1.
    assert math.isclose(
        runtime.get_node("PTCH1").states["active"],
        0.2,
    )
    assert math.isclose(
        runtime.get_node("PTCH1").states["inactive"],
        0.8,
    )
    # ---------------------------------------------------------
    # 5. InternalNet: Node -> Passive -> Gene -> HIR
    # ---------------------------------------------------------
    node_runtime = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    passive_runtime = internal_net.run_passive_stage(
        runtime=node_runtime,
        plan=plan,
        dt=1.0,
    )

    gene_runtime = internal_net.run_gene_stage(
        runtime=passive_runtime,
        plan=plan,
    )

    hir_output = internal_net.run_hir_stage(
        runtime=gene_runtime,
        plan=plan,
        gene_definitions={
            "FOXA2": gene_repository.get("FOXA2"),
        },
        node_definitions={
            "H3K27ac": node_repository.get("H3K27ac"),
            "PTCH1": node_repository.get("PTCH1"),
        },
        behavior_parameters={},
        resource_coefficients={},
        available_resources={},
    )

    assert isinstance(hir_output, HIROutput)

    # Gene calculation reached HIR.
    assert gene_runtime.get_gene("FOXA2").value == 0.5
    assert (
        gene_runtime.get_gene("FOXA2")
        .modifications["lysine_modified"]
        == 0.5
    )

    # ---------------------------------------------------------
    # 6. InternalNet -> Shell -> World
    # ---------------------------------------------------------
    apply_hir_output(
        world,
        "cell_shell_full_tick",
        hir_output,
    )

    updated_cell = world.get_cell(
        "cell_shell_full_tick",
    )

    # HIR output reached World.
    assert updated_cell.labels == {"FOXA2"}

    # Type is intentionally not applied yet.
    assert updated_cell.type == "floor_plate_progenitor"

def test_apply_hir_output_applies_behavior_internal_output_to_node():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        nodes={
            "FOXA2": NodeState(
                name="FOXA2",
                total=0.0,
            )
        },
    )

    world.add_cell(cell)

    output = HIROutput(
        behaviors={
            "production:FOXA2": BehaviorRuntimeState(
                behavior_name="production",
                source_type="gene",
                source_name="FOXA2",
                node_states={
                    "FOXA2": NodeState(
                        name="FOXA2",
                        total=0.0,
                    )
                },
                gene_states={},
                value=0.75,
                internal_outputs={
                    "target": "FOXA2",
                    "state": "total",
                },
            )
        }
    )

    apply_hir_output(
        world=world,
        cell_id="B",
        output=output,
    )

    assert world.get_cell("B").nodes["FOXA2"].total == 0.75
    
def test_apply_hir_output_applies_multiple_behavior_outputs():
    world = World()

    cell = CellState(
        id="B",
        type="floor_plate_progenitor",
        nodes={
            "FOXA2": NodeState(
                name="FOXA2",
                total=0.0,
            ),
            "SHH": NodeState(
                name="SHH",
                total=0.0,
            ),
        },
    )

    world.add_cell(cell)

    output = HIROutput(
        behaviors={
            "production:FOXA2": BehaviorRuntimeState(
                behavior_name="production",
                source_type="gene",
                source_name="FOXA2",
                node_states={
                    "FOXA2": NodeState(
                        name="FOXA2",
                        total=0.0,
                    ),
                    "SHH": NodeState(
                        name="SHH",
                        total=0.0,
                    ),
                },
                gene_states={},
                value=0.75,
                internal_outputs={
                    "target": "FOXA2",
                    "state": "total",
                },
            ),
            "production:SHH": BehaviorRuntimeState(
                behavior_name="production",
                source_type="gene",
                source_name="SHH",
                node_states={
                    "FOXA2": NodeState(
                        name="FOXA2",
                        total=0.0,
                    ),
                    "SHH": NodeState(
                        name="SHH",
                        total=0.0,
                    ),
                },
                gene_states={},
                value=0.40,
                internal_outputs={
                    "target": "SHH",
                    "state": "total",
                },
            ),
        },
    )

    apply_hir_output(
        world=world,
        cell_id="B",
        output=output,
    )

    assert world.get_cell("B").nodes["FOXA2"].total == 0.75
    assert world.get_cell("B").nodes["SHH"].total == 0.40
