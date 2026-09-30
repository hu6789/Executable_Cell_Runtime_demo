from pathlib import Path
from internalnet.compute_plan.builder import ComputePlanBuilder
from internalnet.graph_engine.engine import GraphEngine
from internalnet.graph_engine.repository import GraphRepository
from internalnet.graph_engine.schema import GraphDefinition, GraphEdge
from internalnet.internalnet import InternalNet
from internalnet.node_engine.engine import NodeEngine
from internalnet.node_engine.repository import NodeRepository
from internalnet.node_engine.schema import NodeDefinition
from internalnet.runtime.merger import RuntimeMerger
from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import NodeState
from internalnet.passive_engine.engine import PassiveEngine
from internalnet.passive_engine.repository import PassiveRepository
from internalnet.passive_engine.engine import PassiveEngine
from internalnet.passive_engine.repository import PassiveRepository
from internalnet.passive_engine.schema import PassiveDefinition
from internalnet.gene_engine.engine import GeneEngine
from internalnet.gene_engine.repository import GeneRepository
from internalnet.gene_engine.schema import GeneDefinition
from internalnet.runtime.state import GeneState
from internalnet.behavior_engine.schema import BehaviorIntention
from internalnet.hir.schema import (
    TFRegulationDelta,
    ResourceAllocation,
    ResourceDelta,
    BehaviorRuntimeState,
    HIROutput,
)
from internalnet.hir.engine import HIREngine
from internalnet.hir.type.determination import TypeDetermination, TypeEvidenceStatus
from internalnet.hir.type.selection import TypeSelection
from internalnet.hir.type.repository import LineageRepository
LIBRARY = Path("internalnet/hir/library")


def test_internalnet_runs_node_dependency_chain():
    graph = GraphDefinition(
        name="shh_test",
        type="common",
        nodes=["PTCH1", "SMO"],
        edges=[
            GraphEdge(
                name="PTCH1_SMO",
                type="node-node",
                source="PTCH1",
                target="SMO",
            )
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan_builder = ComputePlanBuilder(graph_engine)

    plan = plan_builder.build(
        cell_id="cell_A",
        graph_ids=["shh_test"],
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

    runtime = Runtime(
        id="cell_A",
        type="Neural_Progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=10.0,
                states={
                    "active": 0.0,
                    "inactive": 10.0,
                },
            ),
            "SMO": NodeState(
                name="SMO",
                total=10.0,
                states={
                    "unrecruited": 10.0,
                    "recruited": 0.0,
                },
            ),
        },
    )

    result = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    smo = result.get_node("SMO")

    assert smo.states["unrecruited"] == 0.0
    assert smo.states["recruited"] == 10.0
    
def test_internalnet_does_not_mutate_input_runtime():
    graph = GraphDefinition(
        name="shh_test",
        type="common",
        nodes=["PTCH1", "SMO"],
        edges=[
            GraphEdge(
                name="PTCH1_SMO",
                type="node-node",
                source="PTCH1",
                target="SMO",
            )
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan_builder = ComputePlanBuilder(graph_engine)

    plan = plan_builder.build(
        cell_id="cell_A",
        graph_ids=["shh_test"],
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

    runtime = Runtime(
        id="cell_A",
        type="Neural_Progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=10.0,
                states={
                    "active": 0.0,
                    "inactive": 10.0,
                },
            ),
            "SMO": NodeState(
                name="SMO",
                total=10.0,
                states={
                    "unrecruited": 10.0,
                    "recruited": 0.0,
                },
            ),
        },
    )

    original_smo_states = dict(
        runtime.get_node("SMO").states
    )

    result = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    assert result is not runtime

    assert runtime.get_node("SMO").states == original_smo_states

    assert result.get_node("SMO").states["unrecruited"] == 0.0
    assert result.get_node("SMO").states["recruited"] == 10.0
    
def test_internalnet_uses_latest_runtime_state_for_downstream_node():
    graph = GraphDefinition(
        name="chain_test",
        type="common",
        nodes=["A", "B", "C"],
        edges=[
            GraphEdge(
                name="A_B",
                type="node-node",
                source="A",
                target="B",
            ),
            GraphEdge(
                name="B_C",
                type="node-node",
                source="B",
                target="C",
            ),
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_chain",
        graph_ids=["chain_test"],
    )

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="A",
                category="signal",
            ),
            NodeDefinition(
                name="B",
                category="signal",
            ),
            NodeDefinition(
                name="C",
                category="signal",
            ),
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

    runtime = Runtime(
        id="cell_chain",
        type="Test_Cell",
        node_states={
            "A": NodeState(
                name="A",
                total=10.0,
                states={"active": 10.0},
            ),
            "B": NodeState(
                name="B",
                total=5.0,
                states={"active": 5.0},
            ),
            "C": NodeState(
                name="C",
                total=1.0,
                states={"active": 1.0},
            ),
        },
    )

    result = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    assert result.get_node("A").total == 10.0
    assert result.get_node("B").total == 5.0
    assert result.get_node("C").total == 1.0
    
class RecordingNodeEngine:
    def __init__(self):
        self.inputs = []

    def run(self, node_input):
        from internalnet.runtime.delta import NodeDelta

        self.inputs.append(node_input)

        if node_input.node_name in {"A", "SMO"}:
            return NodeDelta(
                source="test",
                node_name=node_input.node_name,
                total_delta=5.0,
            )

        return NodeDelta(
            source="test",
            node_name=node_input.node_name,
        )


def test_internalnet_passes_latest_upstream_state_to_downstream_node():
    graph = GraphDefinition(
        name="latest_state_test",
        type="common",
        nodes=["A", "B"],
        edges=[
            GraphEdge(
                name="A_B",
                type="node-node",
                source="A",
                target="B",
            )
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_latest",
        graph_ids=["latest_state_test"],
    )
    
    node_repository = NodeRepository(
        [
            NodeDefinition(name="A", category="signal"),
            NodeDefinition(name="B", category="signal"),
        ]
    )

    node_engine = RecordingNodeEngine()

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=PassiveEngine(
            passive_repository=PassiveRepository(),
            node_repository=node_repository,
        ),
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
    )

    runtime = Runtime(
        id="cell_latest",
        type="Test_Cell",
        node_states={
            "A": NodeState(
                name="A",
                total=10.0,
            ),
            "B": NodeState(
                name="B",
                total=5.0,
            ),
        },
    )

    result = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    assert result.get_node("A").total == 15.0

    b_input = node_engine.inputs[1]

    assert b_input.node_name == "B"
    assert b_input.related_inputs["A"]["total"] == 15.0
    
def test_internalnet_passes_latest_smo_state_to_gli2():
    graph = GraphDefinition(
        name="shh_chain_test",
        type="common",
        nodes=["PTCH1", "SMO", "GLI2"],
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
        cell_id="cell_shh",
        graph_ids=["shh_chain_test"],
    )
    
    node_repository = NodeRepository(
        [
            NodeDefinition(name="PTCH1", category="receptor"),
            NodeDefinition(name="SMO", category="functional_protein"),
            NodeDefinition(name="GLI2", category="functional_protein"),
        ]
    )

    node_engine = RecordingNodeEngine()

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=PassiveEngine(
            passive_repository=PassiveRepository(),
            node_repository=node_repository,
        ),
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
    )

    runtime = Runtime(
        id="cell_shh",
        type="Neural_Progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=10.0,
                states={
                    "active": 0.0,
                    "inactive": 10.0,
                },
            ),
            "SMO": NodeState(
                name="SMO",
                total=10.0,
                states={
                    "unrecruited": 10.0,
                    "recruited": 0.0,
                },
            ),
            "GLI2": NodeState(
                name="GLI2",
                total=10.0,
                states={
                    "SUFU_bound": 10.0,
                    "free": 0.0,
                    "nuclear": 0.0,
                },
            ),
        },
    )

    result = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    gli2_input = node_engine.inputs[2]

    assert gli2_input.node_name == "GLI2"
    assert gli2_input.related_inputs["SMO"]["total"] == 15.0
    
def test_internalnet_runs_half_life_passive_stage():
    graph = GraphDefinition(
        name="passive_test",
        type="common",
        nodes=["GLI2"],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_passive",
        graph_ids=["passive_test"],
    )

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="GLI2",
                category="functional_protein",
                half_life=60.0,
            ),
        ]
    )

    passive_repository = PassiveRepository(
        [
            PassiveDefinition(
                name="half_life_decay",
                formula={
                    "equation": (
                        "Δ = X_total × "
                        "(1 - exp(-ln(2) × Δt / t_half))"
                    ),
                    "parameters": {
                        "t_half": "node.half_life",
                    },
                },
                update={
                    "target": "all_states",
                    "mode": "proportional_decay",
                },
            )
        ]
    )

    node_engine = NodeEngine(node_repository)

    passive_engine = PassiveEngine(
        passive_repository=passive_repository,
        node_repository=node_repository,
    )

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
    )

    runtime = Runtime(
        id="cell_passive",
        type="Neural_Progenitor",
        node_states={
            "GLI2": NodeState(
                name="GLI2",
                total=10.0,
                states={
                    "SUFU_bound": 10.0,
                    "free": 0.0,
                    "nuclear": 0.0,
                },
            ),
        },
    )

    result = internal_net.run_passive_stage(
        runtime=runtime,
        plan=plan,
        dt=60.0,
    )

    gli2 = result.get_node("GLI2")

    assert gli2.states["SUFU_bound"] == 5.0
    assert gli2.states["free"] == 0.0
    assert gli2.states["nuclear"] == 0.0
    
def test_internalnet_runs_diffusion_passive_stage():
    graph = GraphDefinition(
        name="diffusion_test",
        type="common",
        nodes=["GLI2"],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)
    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_diffusion",
        graph_ids=["diffusion_test"],
    )

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="GLI2",
                category="functional_protein",
                diffusion=0.5,
                diffusion_source_states=["free"],
            ),
        ]
    )

    passive_repository = PassiveRepository(
        [
            PassiveDefinition(
                name="diffusion",
                formula={
                    "equation": "Δ = min(D × X_free × Δt, X_free)",
                    "parameters": {
                        "D": "node.diffusion",
                    },
                },
                update={
                    "target_state": "nuclear",
                },
            )
        ]
    )

    node_engine = NodeEngine(node_repository)

    passive_engine = PassiveEngine(
        passive_repository=passive_repository,
        node_repository=node_repository,
    )

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
    )

    runtime = Runtime(
        id="cell_diffusion",
        type="Neural_Progenitor",
        node_states={
            "GLI2": NodeState(
                name="GLI2",
                total=10.0,
                states={
                    "SUFU_bound": 0.0,
                    "free": 8.0,
                    "nuclear": 2.0,
                },
            ),
        },
    )

    result = internal_net.run_passive_stage(
        runtime=runtime,
        plan=plan,
        dt=1.0,
    )

    gli2 = result.get_node("GLI2")

    assert gli2.states["SUFU_bound"] == 0.0
    assert gli2.states["free"] == 4.0
    assert gli2.states["nuclear"] == 6.0
    
def test_internalnet_runs_gene_stage_from_latest_node_state():
    graph = GraphDefinition(
        name="gene_test",
        type="common",
        nodes=["H3K27ac"],
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
        cell_id="cell_gene",
        graph_ids=["gene_test"],
    )

    node_repository = NodeRepository(
        [
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

    node_engine = NodeEngine(node_repository)
    passive_engine = PassiveEngine(
        passive_repository=PassiveRepository(),
        node_repository=node_repository,
    )

    gene_engine = GeneEngine(gene_repository)

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
        gene_engine=gene_engine,
        gene_repository=gene_repository,
    )

    runtime = Runtime(
        id="cell_gene",
        type="Floor_Plate_Progenitor",
        node_states={
            "H3K27ac": NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            ),
        },
    )

    result = internal_net.run_gene_stage(
        runtime=runtime,
        plan=plan,
    )

    foxa2 = result.get_gene("FOXA2")

    assert foxa2.value == 0.5
    assert foxa2.modifications["lysine_modified"] == 0.5
    
def test_internalnet_runs_hir_stage_from_current_runtime():
    class FakeHIREngine:
        def __init__(self):
            self.received_node_states = None
            self.received_gene_states = None

        def run(
            self,
            plan,
            node_states,
            gene_states,
            current_type,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        ):
            self.received_node_states = node_states
            self.received_gene_states = gene_states

            return HIROutput(
                labels={"PTCH1"},
                type_name="floor_plate_progenitor",
            )

    fake_hir = FakeHIREngine()

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="PTCH1",
                category="receptor",
            ),
        ]
    )

    passive_repository = PassiveRepository()

    node_engine = NodeEngine(node_repository)

    passive_engine = PassiveEngine(
        passive_repository=passive_repository,
        node_repository=node_repository,
    )

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
        hir_engine=fake_hir,
    )

    runtime = Runtime(
        id="cell_hir",
        type="floor_plate_progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=1.0,
                states={
                    "active": 0.8,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.6,
                modifications={},
            ),
        },
    )

    plan = ComputePlanBuilder(
        GraphEngine(
            GraphRepository()
        )
    ).build(
        cell_id="cell_hir",
        graph_ids=[],
    )

    result = internal_net.run_hir_stage(
        runtime=runtime,
        plan=plan,
        gene_definitions={},
        node_definitions={},
        behavior_parameters={},
        resource_coefficients={},
        available_resources={},
    )

    assert isinstance(result, HIROutput)
    assert result.labels == {"PTCH1"}
    assert result.type_name == "floor_plate_progenitor"

    assert fake_hir.received_node_states["PTCH1"].total == 1.0
    assert (
        fake_hir.received_node_states["PTCH1"].states["active"]
        == 0.8
    )

    assert fake_hir.received_gene_states["FOXA2"].value == 0.6
    
def test_internalnet_hir_stage_receives_latest_gene_state():
    class FakeHIREngine:
        def __init__(self):
            self.received_gene_states = None

        def run(
            self,
            plan,
            node_states,
            gene_states,
            current_type,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        ):
            self.received_gene_states = gene_states

            return HIROutput(
                labels={"FOXA2"},
                type_name="floor_plate_progenitor",
            )

    graph = GraphDefinition(
        name="gene_hir_test",
        type="common",
        nodes=["H3K27ac"],
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
        cell_id="cell_gene_hir",
        graph_ids=["gene_hir_test"],
    )

    node_repository = NodeRepository(
        [
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

    runtime = Runtime(
        id="cell_gene_hir",
        type="floor_plate_progenitor",
        node_states={
            "H3K27ac": NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            ),
        },
    )

    runtime_after_gene = internal_net.run_gene_stage(
        runtime=runtime,
        plan=plan,
    )

    foxa2 = runtime_after_gene.get_gene("FOXA2")

    assert foxa2.value == 0.5
    assert foxa2.modifications["lysine_modified"] == 0.5

    result = internal_net.run_hir_stage(
        runtime=runtime_after_gene,
        plan=plan,
        gene_definitions={},
        node_definitions={},
        behavior_parameters={},
        resource_coefficients={},
        available_resources={},
    )

    assert isinstance(result, HIROutput)
    assert result.labels == {"FOXA2"}
    assert result.type_name == "floor_plate_progenitor"

    assert (
        fake_hir.received_gene_states["FOXA2"].value
        == 0.5
    )

    assert (
        fake_hir.received_gene_states["FOXA2"]
        .modifications["lysine_modified"]
        == 0.5
    )
    
def test_internalnet_runs_real_hir_engine():
    class FakeBehaviorEngine:

        def run_execution(
            self,
            execution,
            parameters,
        ):
            return BehaviorIntention(
                behavior_name=execution.behavior_name,
                value=1.0,
            )

    class FakeTFRegulator:

        def regulate(
            self,
            intention,
            behavior_genes,
            node_states,
            gene_definitions,
        ):
            return TFRegulationDelta(
                behavior_name=intention.behavior_name,
                delta=0.5,
            )

    class FakeResourceAllocator:

        def allocate(
            self,
            behavior_name,
            behavior_value,
            resource_coefficients,
        ):
            return ResourceAllocation(
                behavior_name=behavior_name,
                resources={
                    "ATP": 3.0,
                },
            )

    class FakeResourceRealizer:

        def realize(
            self,
            intention,
            allocation,
            available_resources,
        ):
            return ResourceDelta(
                behavior_name=intention.behavior_name,
                delta=-0.75,
            )

    class FakeBehaviorStateMerger:

        def merge(
            self,
            intention,
            tf_delta,
            resource_delta,
            node_states,
            gene_states,
            source_type,
            source_name,
            internal_outputs,
        ):
            return BehaviorRuntimeState(
                behavior_name=intention.behavior_name,
                source_type=source_type,
                source_name=source_name,
                node_states=dict(node_states),
                gene_states=dict(gene_states),
                value=0.75,
            )

    class FakeLabelDetermination:

        def determine(
            self,
            node_states,
            node_definitions,
        ):
            return {"PTCH1"}

    class FakeTypeDetermination:

        def determine(
            self,
            evidence_list,
            node_states,
        ):
            return [
                TypeEvidenceStatus(
                    type_name="floor_plate_progenitor",
                    upstream_complete=True,
                    regulatory_complete=True,
                    output_complete=True,
                    complete=True,
                    matched_count=3,
                    total_count=3,
                )
            ]
    class FakeTypeEvidenceRepository:

        def all(self):
            return []
        
    class FakeTypeTransition:

        def resolve(
            self,
            current_type,
            statuses,
        ):
            return []
            
            
    hir_engine = HIREngine(
        behavior_engine=FakeBehaviorEngine(),
        tf_regulator=FakeTFRegulator(),
        resource_allocator=FakeResourceAllocator(),
        resource_realizer=FakeResourceRealizer(),
        behavior_state_merger=FakeBehaviorStateMerger(),
        label_determination=FakeLabelDetermination(),
        type_determination=FakeTypeDetermination(),
        type_evidence_repository=FakeTypeEvidenceRepository(),
        type_transition=FakeTypeTransition(),
                type_selection=TypeSelection(
            lineage_repository=LineageRepository(
                LIBRARY / "lineage.json"
            )
        ),
    )

    graph = GraphDefinition(
        name="real_hir_test",
        type="common",
        nodes=["PTCH1"],
        genes=["FOXA2"],
        behaviors=["production"],
        edges=[
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ],
    )

    graph_repository = GraphRepository()
    graph_repository.register(graph)

    graph_engine = GraphEngine(graph_repository)

    plan = ComputePlanBuilder(graph_engine).build(
        cell_id="cell_real_hir",
        graph_ids=["real_hir_test"],
    )

    node_repository = NodeRepository(
        [
            NodeDefinition(
                name="PTCH1",
                category="receptor",
            ),
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
        hir_engine=hir_engine,
    )

    runtime = Runtime(
        id="cell_real_hir",
        type="floor_plate_progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=1.0,
                states={
                    "active": 0.8,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.5,
                modifications={},
            ),
        },
    )

    result = internal_net.run_hir_stage(
        runtime=runtime,
        plan=plan,
        gene_definitions={},
        node_definitions={},
        behavior_parameters={
            "production": {},
        },
        resource_coefficients={
            "production": {
                "ATP": 2.0,
            },
        },
        available_resources={
            "ATP": 1.5,
        },
    )

    assert isinstance(result, HIROutput)

    assert result.behaviors["production:FOXA2"].value == 0.75
    assert result.labels == {"PTCH1"}
    assert result.type_name == "floor_plate_progenitor"
    
    
def test_internalnet_runs_node_gene_hir_chain():
    class FakeHIREngine:
        def __init__(self):
            self.received_node_states = None
            self.received_gene_states = None

        def run(
            self,
            plan,
            node_states,
            gene_states,
            current_type,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        ):
            self.received_node_states = node_states
            self.received_gene_states = gene_states

            return HIROutput(
                labels={"FOXA2"},
                type_name="floor_plate_progenitor",
            )

    graph = GraphDefinition(
        name="node_gene_hir_chain",
        type="common",
        nodes=["H3K27ac"],
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
        cell_id="cell_full_chain",
        graph_ids=["node_gene_hir_chain"],
    )

    node_repository = NodeRepository(
        [
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

    runtime = Runtime(
        id="cell_full_chain",
        type="floor_plate_progenitor",
        node_states={
            "H3K27ac": NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            ),
        },
    )

    node_runtime = internal_net.run_node_stage(
        runtime=runtime,
        plan=plan,
    )

    gene_runtime = internal_net.run_gene_stage(
        runtime=node_runtime,
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
        },
        behavior_parameters={},
        resource_coefficients={},
        available_resources={},
    )

    assert isinstance(hir_output, HIROutput)

    assert (
        node_runtime.get_node("H3K27ac").states["nuclear"]
        == 0.5
    )

    foxa2 = gene_runtime.get_gene("FOXA2")

    assert foxa2.value == 0.5
    assert foxa2.modifications["lysine_modified"] == 0.5

    assert (
        fake_hir.received_node_states["H3K27ac"]
        .states["nuclear"]
        == 0.5
    )

    assert (
        fake_hir.received_gene_states["FOXA2"]
        .value
        == 0.5
    )

    assert (
        fake_hir.received_gene_states["FOXA2"]
        .modifications["lysine_modified"]
        == 0.5
    )

    assert hir_output.labels == {"FOXA2"}
    assert hir_output.type_name == "floor_plate_progenitor"
    

def test_internalnet_runs_full_pipeline():
    class RecordingNodeEngine:
        def __init__(self):
            self.inputs = []

        def run(self, node_input):
            from internalnet.runtime.delta import NodeDelta

            self.inputs.append(node_input)

            return NodeDelta(
                source="test",
                node_name=node_input.node_name,
            )

    class FakeHIREngine:
        def __init__(self):
            self.received_node_states = None
            self.received_gene_states = None

        def run(
            self,
            plan,
            node_states,
            gene_states,
            current_type,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        ):
            self.received_node_states = node_states
            self.received_gene_states = gene_states

            return HIROutput(
                labels={"FOXA2"},
                type_name="floor_plate_progenitor",
            )

    graph = GraphDefinition(
        name="full_pipeline",
        type="common",
        nodes=["H3K27ac"],
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
        cell_id="cell_full_pipeline",
        graph_ids=["full_pipeline"],
    )

    node_repository = NodeRepository(
        [
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

    node_engine = RecordingNodeEngine()

    passive_engine = PassiveEngine(
        passive_repository=PassiveRepository(),
        node_repository=node_repository,
    )

    gene_engine = GeneEngine(
        gene_repository,
    )

    fake_hir = FakeHIREngine()

    internal_net = InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
        gene_engine=gene_engine,
        gene_repository=gene_repository,
        hir_engine=fake_hir,
    )

    runtime = Runtime(
        id="cell_full_pipeline",
        type="floor_plate_progenitor",
        node_states={
            "H3K27ac": NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            ),
        },
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            ),
        },
    )

    output = internal_net.run(
        runtime=runtime,
        plan=plan,
        dt=0.0,
        gene_definitions={
            "FOXA2": gene_repository.get("FOXA2"),
        },
        node_definitions={
            "H3K27ac": node_repository.get("H3K27ac"),
        },
        behavior_parameters={},
        resource_coefficients={},
        available_resources={},
    )

    assert isinstance(output, HIROutput)

    assert output.labels == {"FOXA2"}
    assert output.type_name == "floor_plate_progenitor"

    assert (
        fake_hir.received_node_states["H3K27ac"]
        .states["nuclear"]
        == 0.5
    )

    assert (
        fake_hir.received_gene_states["FOXA2"]
        .value
        == 0.5
    )

    assert (
        fake_hir.received_gene_states["FOXA2"]
        .modifications["lysine_modified"]
        == 0.5
    )

