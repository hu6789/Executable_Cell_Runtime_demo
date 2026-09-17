from internalnet.compute_plan.schema import CellComputePlan
from internalnet.graph_engine.schema import GraphEdge
from internalnet.compute_plan.builder import ComputePlanBuilder
from internalnet.graph_engine.engine import GraphEngine
from internalnet.graph_engine.repository import GraphRepository
from internalnet.graph_engine.schema import (
    GraphDefinition,
    GraphEdge,
)

def test_cell_compute_plan_creation():
    edge = GraphEdge(
        name="PTCH1_SMO",
        type="node-node",
        source="PTCH1",
        target="SMO",
        required=True,
    )

    plan = CellComputePlan(
        cell_id="B",
        graph_ids=(
            "common_shh_signaling",
            "floor_plate_progenitor",
        ),
        candidate_nodes=(
            "SHH",
            "PTCH1",
            "SMO",
            "GLI2",
        ),
        candidate_genes=(
            "FOXA2",
            "SHH",
        ),
        candidate_behaviors=(
            "production",
            "release",
        ),
        edges=(edge,),
    )

    assert plan.cell_id == "B"

    assert plan.graph_ids == (
        "common_shh_signaling",
        "floor_plate_progenitor",
    )

    assert "SMO" in plan.candidate_nodes
    assert "FOXA2" in plan.candidate_genes
    assert "production" in plan.candidate_behaviors

    assert len(plan.edges) == 1
    assert plan.edges[0].source == "PTCH1"
    assert plan.edges[0].target == "SMO"


def test_cell_compute_plan_defaults():
    plan = CellComputePlan(
        cell_id="A",
    )

    assert plan.graph_ids == ()
    assert plan.candidate_nodes == ()
    assert plan.candidate_genes == ()
    assert plan.candidate_behaviors == ()
    assert plan.edges == ()


def test_cell_compute_plan_is_frozen():
    plan = CellComputePlan(
        cell_id="A",
    )

    try:
        plan.cell_id = "B"
        assert False
    except AttributeError:
        pass


def test_cell_compute_plan_can_carry_multiple_edge_types():
    edges = (
        GraphEdge(
            name="PTCH1_SMO",
            type="node-node",
            source="PTCH1",
            target="SMO",
        ),
        GraphEdge(
            name="H3K27ac_FOXA2",
            type="node-gene",
            source="H3K27ac",
            target="FOXA2",
        ),
        GraphEdge(
            name="FOXA2_production",
            type="gene-behavior",
            source="FOXA2",
            target="production",
        ),
    )

    plan = CellComputePlan(
        cell_id="B",
        edges=edges,
    )

    assert len(plan.edges) == 3
    assert plan.edges[0].type == "node-node"
    assert plan.edges[1].type == "node-gene"
    assert plan.edges[2].type == "gene-behavior"


def test_cell_compute_plan_contains_no_tick_execution_state():
    plan = CellComputePlan(
        cell_id="B",
        candidate_nodes=("SMO",),
    )

    assert not hasattr(plan, "active_nodes")
    assert not hasattr(plan, "active_genes")
    assert not hasattr(plan, "active_behaviors")
    assert not hasattr(plan, "active_passives")
    
    
def make_graph_engine() -> GraphEngine:
    engine = GraphEngine()

    engine.register(
        GraphDefinition(
            name="common_shh_signaling",
            type="common",
            nodes=[
                "PTCH1",
                "SMO",
                "GLI2",
                "SUFU",
                "ATP",
            ],
            genes=[],
            behaviors=[
                "production",
                "release",
            ],
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
    )

    engine.register(
        GraphDefinition(
            name="floor_plate_progenitor",
            type="cell_specific",
            nodes=[
                "FOXA2",
                "SHH",
                "H3K27ac",
            ],
            genes=[
                "FOXA2",
                "SHH",
            ],
            behaviors=[
                "production",
                "release",
            ],
            edges=[
                GraphEdge(
                    name="H3K27ac_FOXA2",
                    type="node-gene",
                    source="H3K27ac",
                    target="FOXA2",
                ),
                GraphEdge(
                    name="FOXA2_production",
                    type="gene-behavior",
                    source="FOXA2",
                    target="production",
                ),
                GraphEdge(
                    name="SHH_production",
                    type="gene-behavior",
                    source="SHH",
                    target="production",
                ),
                GraphEdge(
                    name="SHH_release",
                    type="node-behavior",
                    source="SHH",
                    target="release",
                ),
            ],
        )
    )

    return engine


def test_builder_creates_plan_from_graphs():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
            "floor_plate_progenitor",
        ],
    )

    assert plan.cell_id == "cell_B"

    assert plan.graph_ids == (
        "common_shh_signaling",
        "floor_plate_progenitor",
    )

    assert plan.candidate_nodes == (
        "PTCH1",
        "SMO",
        "GLI2",
        "SUFU",
        "ATP",
        "FOXA2",
        "SHH",
        "H3K27ac",
    )

    assert plan.candidate_genes == (
        "FOXA2",
        "SHH",
    )

    assert plan.candidate_behaviors == (
        "production",
        "release",
    )


def test_builder_preserves_graph_edges():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
            "floor_plate_progenitor",
        ],
    )

    assert [edge.name for edge in plan.edges] == [
        "PTCH1_SMO",
        "SMO_GLI2",
        "H3K27ac_FOXA2",
        "FOXA2_production",
        "SHH_production",
        "SHH_release",
    ]


def test_builder_deduplicates_candidates():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
            "floor_plate_progenitor",
        ],
    )

    assert plan.candidate_behaviors.count("production") == 1
    assert plan.candidate_behaviors.count("release") == 1


def test_builder_preserves_graph_order():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "floor_plate_progenitor",
            "common_shh_signaling",
        ],
    )

    assert plan.graph_ids == (
        "floor_plate_progenitor",
        "common_shh_signaling",
    )

    assert plan.candidate_nodes[:3] == (
        "FOXA2",
        "SHH",
        "H3K27ac",
    )


def test_builder_does_not_create_tick_execution_state():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
            "floor_plate_progenitor",
        ],
    )

    assert not hasattr(plan, "active_nodes")
    assert not hasattr(plan, "active_genes")
    assert not hasattr(plan, "active_behaviors")
    
def test_builder_resolves_node_execution_order():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
            "floor_plate_progenitor",
        ],
    )

    assert plan.node_execution_order.index("PTCH1") < \
        plan.node_execution_order.index("SMO")

    assert plan.node_execution_order.index("SMO") < \
        plan.node_execution_order.index("GLI2")


def test_builder_keeps_independent_nodes_in_execution_order():
    engine = make_graph_engine()
    builder = ComputePlanBuilder(engine)

    plan = builder.build(
        cell_id="cell_B",
        graph_ids=[
            "common_shh_signaling",
        ],
    )

    assert set(plan.node_execution_order) == {
        "PTCH1",
        "SMO",
        "GLI2",
        "SUFU",
        "ATP",
    }

    assert plan.node_execution_order.index("PTCH1") < \
        plan.node_execution_order.index("SMO")

    assert plan.node_execution_order.index("SMO") < \
        plan.node_execution_order.index("GLI2")


def test_builder_rejects_circular_node_dependency():
    engine = GraphEngine()

    engine.register(
        GraphDefinition(
            name="circular_graph",
            type="common",
            nodes=[
                "A",
                "B",
            ],
            edges=[
                GraphEdge(
                    name="A_B",
                    type="node-node",
                    source="A",
                    target="B",
                ),
                GraphEdge(
                    name="B_A",
                    type="node-node",
                    source="B",
                    target="A",
                ),
            ],
        )
    )

    builder = ComputePlanBuilder(engine)

    try:
        builder.build(
            cell_id="cell_test",
            graph_ids=["circular_graph"],
        )
        assert False
    except ValueError as exc:
        assert "Circular node dependency" in str(exc)
