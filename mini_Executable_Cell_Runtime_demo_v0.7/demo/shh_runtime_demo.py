# demo/shh_runtime_demo.py

import json
from pathlib import Path
from typing import Tuple

from internalnet.compute_plan.builder import ComputePlanBuilder
from internalnet.graph_engine.engine import GraphEngine
from internalnet.graph_engine.repository import GraphRepository
from internalnet.graph_engine.schema import (
    GraphDefinition,
    GraphEdge,
)
from internalnet.runtime.state import NodeState, GeneState
from shell.schema import CellState
from shell.world import World
from shell.shh_field import SHHField
from shell.input import build_runtime_input
from internalnet.internalnet import InternalNet
from internalnet.node_engine.schema import NodeDefinition
from internalnet.node_engine.engine import NodeEngine
from internalnet.node_engine.repository import NodeRepository

from internalnet.passive_engine.engine import PassiveEngine
from internalnet.passive_engine.repository import PassiveRepository
from internalnet.passive_engine.schema import PassiveDefinition
from internalnet.gene_engine.engine import GeneEngine
from internalnet.gene_engine.repository import GeneRepository
from internalnet.gene_engine.schema import GeneDefinition
from internalnet.behavior_engine.engine import BehaviorEngine
from internalnet.behavior_engine.repository import BehaviorRepository
from internalnet.behavior_engine.schema import BehaviorDefinition
from internalnet.hir.engine import HIREngine
from internalnet.hir.behavior_state_merger import BehaviorStateMerger
from internalnet.hir.label.determination import LabelDetermination
from internalnet.hir.realization.resource_allocator import ResourceAllocator
from internalnet.hir.realization.resource_realizer import ResourceRealizer
from internalnet.hir.regulation.repository import (
    TFElementRelationRepository,
)
from internalnet.hir.regulation.tf_regulator import TFRegulator
from internalnet.hir.type.determination import TypeDetermination
from internalnet.hir.type.repository import TypeCriteriaRepository

from internalnet.runtime.merger import RuntimeMerger
from shell.apply import apply_hir_output

from demo.trace import DemoTraceRecorder
from demo.trace_formatter import print_tick_trace

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GRAPH_DIR = PROJECT_ROOT / "internalnet" / "graph"
NODE_DIR = PROJECT_ROOT / "internalnet" / "node"
GENE_DIR = PROJECT_ROOT / "internalnet" / "gene"
BEHAVIOR_DIR = PROJECT_ROOT / "internalnet" / "behavior"
PASSIVE_DIR = PROJECT_ROOT / "internalnet" / "passive"
HIR_LIBRARY_DIR = PROJECT_ROOT / "internalnet" / "hir" / "library"


class DemoCellConfig:
    def __init__(
        self,
        cell_id: str,
        cell_type: str,
        graph_ids: Tuple[str, ...],
        position: float,
    ):
        self.cell_id = cell_id
        self.cell_type = cell_type
        self.graph_ids = graph_ids
        self.position = position


CELL_CONFIGS = (
    DemoCellConfig(
        cell_id="A",
        cell_type="neural_progenitor",
        graph_ids=("common_shh_signaling",),
        position=0.0,
    ),
    DemoCellConfig(
        cell_id="B",
        cell_type="floor_plate_progenitor",
        graph_ids=(
            "common_shh_signaling",
            "floor_plate_progenitor",
        ),
        position=1.0,
    ),
    DemoCellConfig(
        cell_id="C",
        cell_type="motor_neuron_progenitor",
        graph_ids=("floor_plate_progenitor",),
        position=2.0,
    ),
)


def load_graph_definition(path: Path) -> GraphDefinition:
    with path.open("r") as handle:
        data = json.load(handle)

    edges = tuple(
        GraphEdge(
            name=edge["name"],
            type=edge["type"],
            source=edge["source"],
            target=edge["target"],
            required=edge.get("required", True),
        )
        for edge in data.get("edges", [])
    )

    return GraphDefinition(
        name=data["name"],
        type=data["type"],
        nodes=data.get("nodes", []),
        genes=data.get("genes", []),
        behaviors=data.get("behaviors", []),
        edges=edges,
    )

def load_node_definition(path: Path) -> NodeDefinition:
    with path.open("r") as handle:
        data = json.load(handle)

    return NodeDefinition(
        name=data["name"],
        category=data["category"],
        polymorphism=data.get("polymorphism", []),
        half_life=data.get("half_life"),
        diffusion=data.get("diffusion"),
        formulation=data.get("formulation"),
    )

def load_passive_definition(path: Path) -> PassiveDefinition:
    with path.open("r") as handle:
        data = json.load(handle)

    return PassiveDefinition(
        name=data["name"],
        applies_to=data.get("applies_to", []),
        formula=data.get("formula", {}),
        update=data.get("update", {}),
    )

def load_gene_definition(path: Path) -> GeneDefinition:
    with path.open("r") as handle:
        data = json.load(handle)

    return GeneDefinition(
        name=data["name"],
        category=data.get("category"),
        polymorphism=data.get("polymorphism", []),
        elements=data.get("elements", []),
        formula=data.get("formula", {}),
    )

def load_behavior_definition(path: Path) -> BehaviorDefinition:
    with path.open("r") as handle:
        data = json.load(handle)

    return BehaviorDefinition(
        name=data["name"],
        category=data.get("category"),
        formula=data.get("formula", {}),
        resources=data.get("resources", {}),
        internal_outputs=data.get("internal_outputs", {}),
        outputs=data.get("outputs", {}),
    )

def build_graph_engine() -> GraphEngine:
    repository = GraphRepository()
    engine = GraphEngine(repository=repository)

    for graph_name in (
        "common_shh_signaling",
        "floor_plate_progenitor",
    ):
        path = GRAPH_DIR / "{}.json".format(graph_name)
        graph = load_graph_definition(path)
        engine.register(graph)

    return engine


def build_compute_plans(
    graph_engine: GraphEngine,
):
    builder = ComputePlanBuilder(graph_engine)

    plans = {}

    for config in CELL_CONFIGS:
        plans[config.cell_id] = builder.build(
            cell_id=config.cell_id,
            graph_ids=config.graph_ids,
        )

    return plans


def build_demo_world() -> World:
    """Build the initial persistent World state for the demo."""

    world = World(
        shh_field=SHHField(decay_length=1.0),
    )

    for config in CELL_CONFIGS:
        labels = set()

        if "common_shh_signaling" in config.graph_ids:
            labels.add("PTCH1")

        nodes = {}
        genes = {}

        # Common SHH-signaling nodes.
        if "common_shh_signaling" in config.graph_ids:
            nodes["PTCH1"] = NodeState(
                name="PTCH1",
                total=1.0,
                states={
                    "active": 1.0,
                    "inactive": 0.0,
                },
            )

            nodes["SMO"] = NodeState(
                name="SMO",
                total=1.0,
                states={
                    "unrecruited": 1.0,
                    "recruited": 0.0,
                },
            )

            nodes["GLI2"] = NodeState(
                name="GLI2",
                total=1.0,
                states={
                    "SUFU_bound": 0.5,
                    "free": 0.5,
                    "nuclear": 0.0,
                },
            )

            nodes["ATP"] = NodeState(
                name="ATP",
                total=10.0,
                states={},
            )

            nodes["enzyme"] = NodeState(
                name="enzyme",
                total=1.0,
                states={},
            )

            nodes["molecule"] = NodeState(
                name="molecule",
                total=10.0,
                states={},
            )

        # Floor-plate-specific nodes and genes.
        if "floor_plate_progenitor" in config.graph_ids:
            nodes["FOXA2"] = NodeState(
                name="FOXA2",
                total=0.0,
                states={},
            )

            nodes["SHH"] = NodeState(
                name="SHH",
                total=0.0,
                states={
                    "free": 0.0,
                },
            )

            nodes["H3K27ac"] = NodeState(
                name="H3K27ac",
                total=1.0,
                states={
                    "nuclear": 0.5,
                },
            )

            genes["FOXA2"] = GeneState(
                name="FOXA2",
                baseline=0.0,
                value=0.0,
                modifications={
                    "lysine_modified": 0.0,
                },
            )

            genes["SHH"] = GeneState(
                name="SHH",
                baseline=0.5,
                value=0.5,
                modifications={},
            )

        cell = CellState(
            id=config.cell_id,
            type=config.cell_type,
            nodes=nodes,
            genes=genes,
            labels=labels,
        )

        world.add_cell(cell)

        world.state.shh_field.set_source(
            cell_id=config.cell_id,
            position=config.position,
            amount=0.0,
        )

    return world

def print_world(world: World) -> None:
    print()
    print("=" * 60)
    print("World")
    print("=" * 60)

    for config in CELL_CONFIGS:
        cell = world.get_cell(config.cell_id)
        position, amount = world.state.shh_field.sources[config.cell_id]

        print()
        print("Cell {}".format(cell.id))
        print("  type: {}".format(cell.type))
        print("  position: {}".format(position))
        print("  labels: {}".format(
            ", ".join(sorted(cell.labels))
            if cell.labels
            else "-"
        ))

        print("  nodes:")
        if cell.nodes:
            for name, state in cell.nodes.items():
                print(
                    "    - {}: total={}, states={}".format(
                        name,
                        state.total,
                        state.states,
                    )
                )
        else:
            print("    -")

        print("  genes:")
        if cell.genes:
            for name, state in cell.genes.items():
                print(
                    "    - {}: baseline={}, value={}, "
                    "modifications={}".format(
                        name,
                        state.baseline,
                        state.value,
                        state.modifications,
                    )
                )
        else:
            print("    -")

        print("  SHH source amount: {}".format(amount))


def print_compute_plans(plans) -> None:
    print()
    print("=" * 60)
    print("Compute Plans")
    print("=" * 60)

    for cell_id in ("A", "B", "C"):
        plan = plans[cell_id]

        print()
        print("Cell {}".format(cell_id))
        print("  graphs:")
        for graph_id in plan.graph_ids:
            print("    - {}".format(graph_id))

        print("  candidate_nodes:")
        for node in plan.candidate_nodes:
            print("    - {}".format(node))

        print("  candidate_genes:")
        for gene in plan.candidate_genes:
            print("    - {}".format(gene))

        print("  candidate_behaviors:")
        for behavior in plan.candidate_behaviors:
            print("    - {}".format(behavior))

        print("  node_execution_order:")
        print("    {}".format(" -> ".join(plan.node_execution_order)))

        print("  edges:")
        for edge in plan.edges:
            print(
                "    - {}: {} -> {} "
                "(required={})".format(
                    edge.type,
                    edge.source,
                    edge.target,
                    edge.required,
                )
            )

def build_internalnet(trace=None) -> InternalNet:
    """Build the InternalNet runtime for the demo."""

    node_repository = NodeRepository()
    
    for path in sorted(NODE_DIR.glob("*.json")):
        node_repository.register(
            load_node_definition(path)
        )
    
    passive_repository = PassiveRepository()
    
    for path in sorted(PASSIVE_DIR.glob("*.json")):
        passive_repository.register(
            load_passive_definition(path)
        )
    
    gene_repository = GeneRepository()
    
    for path in sorted(GENE_DIR.glob("*.json")):
        gene_repository.register(
            load_gene_definition(path)
        )
     
    behavior_repository = BehaviorRepository()
    
    for path in sorted(BEHAVIOR_DIR.glob("*.json")):
        behavior_repository.register(
            load_behavior_definition(path)
        )

    node_engine = NodeEngine(
        repository=node_repository,
    )

    passive_engine = PassiveEngine(
        passive_repository=passive_repository,
        node_repository=node_repository,
    )

    gene_engine = GeneEngine(
        gene_repository,
    )

    behavior_engine = BehaviorEngine(
        repository=behavior_repository,
    )

    tf_relation_repository = TFElementRelationRepository(
        PROJECT_ROOT
        / "internalnet"
        / "hir"
        / "library"
        / "tf_element_relations.json"
    )

    tf_regulator = TFRegulator(
        relation_repository=tf_relation_repository,
    )

    resource_allocator = ResourceAllocator()
    resource_realizer = ResourceRealizer()
    behavior_state_merger = BehaviorStateMerger()
    label_determination = LabelDetermination()
    type_determination = TypeDetermination()

    type_criteria_repository = TypeCriteriaRepository(
        PROJECT_ROOT
        / "internalnet"
        / "hir"
        / "library"
        / "type_criteria.json"
    )

    hir_engine = HIREngine(
        behavior_engine=behavior_engine,
        tf_regulator=tf_regulator,
        resource_allocator=resource_allocator,
        resource_realizer=resource_realizer,
        behavior_state_merger=behavior_state_merger,
        label_determination=label_determination,
        type_determination=type_determination,
        type_criteria_repository=type_criteria_repository,
        trace=trace,
    )

    return InternalNet(
        node_engine=node_engine,
        passive_engine=passive_engine,
        node_repository=node_repository,
        runtime_merger=RuntimeMerger(),
        gene_engine=gene_engine,
        gene_repository=gene_repository,
        hir_engine=hir_engine,
        trace=trace,
    )



def main() -> None:
    world = build_demo_world()

    graph_engine = build_graph_engine()
    plans = build_compute_plans(graph_engine)

    trace = DemoTraceRecorder()
    internal_net = build_internalnet(trace=trace)

    print_world(world)
    print_compute_plans(plans)

    print()
    print("=" * 60)
    print("Simulation")
    print("=" * 60)

    for tick in range(1, 5):
        print()
        print("-" * 60)
        print("Tick {}".format(tick))
        print("-" * 60)
        
        trace.clear()

        outputs = {}

        # 1. Run InternalNet for all cells.
        for cell_id in ("A", "B", "C"):
            print()
            print("Running Cell {}".format(cell_id))

            runtime = build_runtime_input(
                world=world,
                cell_id=cell_id,
            )

            output = internal_net.run(
                runtime=runtime,
                plan=plans[cell_id],
                dt=1.0,
                gene_definitions={},
                node_definitions={},
                behavior_parameters={
                    "production": {
                        "production_rate": 1.0,
                    },
                    "release": {
                        "release_rate": 1.0,
                    },
                },
                resource_coefficients={
                    "production": {
                        "ATP": 2.0,
                        "molecule": 1.0,
                    },
                    "release": {
                        "ATP": 0.2,
                    },
                },
                available_resources={
                    "ATP": 10.0,
                    "molecule": 10.0,
                    "enzyme": 1.0,
                },
            )

            outputs[cell_id] = output

            print("  output: {}".format(output))

        # 2. Apply all HIR outputs to World.
        for cell_id in ("A", "B", "C"):
            apply_hir_output(
                world=world,
                cell_id=cell_id,
                output=outputs[cell_id],
            )
            
        print_tick_trace(
            trace,
            detailed_cell_id="B",
        )

        # 3. Show the updated World after this tick.
        print()
        # print("World after Tick {}".format(tick))
        print_world(world)


if __name__ == "__main__":
    main()

