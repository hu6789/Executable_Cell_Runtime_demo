# test/test_graph.py
# python3 -m pytest test/test_graph.py -v

from internalnet.graph_engine.schema import (
    GraphDefinition,
    GraphEdge,
)


# ============================================================
# Schema
# ============================================================


def test_graph_edge_creation():
    edge = GraphEdge(
        name="PTCH1_SMO",
        type="node-node",
        source="PTCH1",
        target="SMO",
    )

    assert edge.name == "PTCH1_SMO"
    assert edge.type == "node-node"
    assert edge.source == "PTCH1"
    assert edge.target == "SMO"
    assert edge.required is True


def test_graph_edge_required_can_be_set():
    edge = GraphEdge(
        name="SHH_release",
        type="node-behavior",
        source="SHH",
        target="release",
        required=False,
    )

    assert edge.required is False


def test_graph_edge_is_frozen():
    edge = GraphEdge(
        name="PTCH1_SMO",
        type="node-node",
        source="PTCH1",
        target="SMO",
    )

    try:
        edge.name = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("GraphEdge should be immutable.")


def test_graph_definition_creation():
    edge = GraphEdge(
        name="PTCH1_SMO",
        type="node-node",
        source="PTCH1",
        target="SMO",
    )

    graph = GraphDefinition(
        name="common_shh_signaling",
        type="common",
        nodes=["PTCH1", "SMO", "GLI2"],
        genes=[],
        behaviors=["production", "release"],
        edges=[edge],
    )

    assert graph.name == "common_shh_signaling"
    assert graph.type == "common"
    assert graph.nodes == ["PTCH1", "SMO", "GLI2"]
    assert graph.genes == []
    assert graph.behaviors == ["production", "release"]
    assert graph.edges == [edge]


def test_graph_definition_defaults():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
    )

    assert graph.nodes == []
    assert graph.genes == []
    assert graph.behaviors == []
    assert graph.edges == []


def test_graph_definition_lists_are_independent():
    graph_a = GraphDefinition(
        name="graph_a",
        type="common",
    )

    graph_b = GraphDefinition(
        name="graph_b",
        type="common",
    )

    graph_a.nodes.append("PTCH1")

    assert graph_a.nodes == ["PTCH1"]
    assert graph_b.nodes == []
    
    
# ============================================================
# Repository
# ============================================================

from internalnet.graph_engine.repository import GraphRepository


def make_test_graph(name="test_graph"):
    return GraphDefinition(
        name=name,
        type="common",
        nodes=["PTCH1", "SMO"],
    )


def test_repository_register_and_get():
    repository = GraphRepository()
    graph = make_test_graph()

    repository.register(graph)

    assert repository.get("test_graph") is graph


def test_repository_has():
    repository = GraphRepository()
    graph = make_test_graph()

    repository.register(graph)

    assert repository.has("test_graph") is True
    assert repository.has("missing_graph") is False


def test_repository_names():
    repository = GraphRepository()

    graph_a = make_test_graph("graph_a")
    graph_b = make_test_graph("graph_b")

    repository.register(graph_a)
    repository.register(graph_b)

    assert repository.names() == ("graph_a", "graph_b")


def test_repository_all():
    repository = GraphRepository()

    graph_a = make_test_graph("graph_a")
    graph_b = make_test_graph("graph_b")

    repository.register(graph_a)
    repository.register(graph_b)

    assert repository.all() == (graph_a, graph_b)


def test_repository_rejects_duplicate_graph():
    repository = GraphRepository()
    graph = make_test_graph()

    repository.register(graph)

    try:
        repository.register(graph)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Repository should reject duplicate graph names."
        )


def test_repository_get_missing_graph():
    repository = GraphRepository()

    try:
        repository.get("missing_graph")
    except KeyError:
        pass
    else:
        raise AssertionError(
            "Repository.get() should raise KeyError for missing graph."
        )


def test_repository_remove():
    repository = GraphRepository()
    graph = make_test_graph()

    repository.register(graph)

    removed = repository.remove("test_graph")

    assert removed is graph
    assert repository.has("test_graph") is False
    assert len(repository) == 0


def test_repository_remove_missing_graph():
    repository = GraphRepository()

    try:
        repository.remove("missing_graph")
    except KeyError:
        pass
    else:
        raise AssertionError(
            "Repository.remove() should raise KeyError for missing graph."
        )


def test_repository_clear():
    repository = GraphRepository()

    repository.register(make_test_graph("graph_a"))
    repository.register(make_test_graph("graph_b"))

    repository.clear()

    assert len(repository) == 0
    assert repository.names() == ()
    assert repository.all() == ()


def test_repository_contains():
    repository = GraphRepository()
    graph = make_test_graph()

    repository.register(graph)

    assert "test_graph" in repository
    assert "missing_graph" not in repository
    

# ============================================================
# Validator
# ============================================================

from internalnet.graph_engine.validator import (
    GraphValidationError,
    GraphValidator,
)


def test_validator_accepts_valid_graph():
    graph = GraphDefinition(
        name="common_shh_signaling",
        type="common",
        nodes=["PTCH1", "SMO", "GLI2"],
        genes=[],
        behaviors=["production", "release"],
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

    validator = GraphValidator()

    validator.validate(graph)


def test_validator_accepts_valid_cell_specific_graph():
    graph = GraphDefinition(
        name="floor_plate_progenitor",
        type="cell_specific",
        nodes=["FOXA2", "SHH", "H3K27ac"],
        genes=["FOXA2", "SHH"],
        behaviors=["production", "release"],
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

    validator = GraphValidator()

    validator.validate(graph)


def test_validator_rejects_empty_graph_name():
    graph = GraphDefinition(
        name="",
        type="common",
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject an empty graph name."
        )


def test_validator_rejects_invalid_graph_type():
    graph = GraphDefinition(
        name="test_graph",
        type="invalid",
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject an invalid graph type."
        )


def test_validator_rejects_empty_node_name():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
        nodes=["PTCH1", ""],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject an empty node name."
        )


def test_validator_rejects_duplicate_node():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
        nodes=["PTCH1", "PTCH1"],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject duplicate nodes."
        )


def test_validator_rejects_duplicate_gene():
    graph = GraphDefinition(
        name="test_graph",
        type="cell_specific",
        genes=["FOXA2", "FOXA2"],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject duplicate genes."
        )


def test_validator_rejects_duplicate_behavior():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
        behaviors=["production", "production"],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject duplicate behaviors."
        )


def test_validator_rejects_duplicate_edge_name():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
        nodes=["PTCH1", "SMO", "GLI2"],
        edges=[
            GraphEdge(
                name="same_edge",
                type="node-node",
                source="PTCH1",
                target="SMO",
            ),
            GraphEdge(
                name="same_edge",
                type="node-node",
                source="SMO",
                target="GLI2",
            ),
        ],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject duplicate edge names."
        )


def test_validator_rejects_invalid_edge_type():
    graph = GraphDefinition(
        name="test_graph",
        type="common",
        nodes=["PTCH1", "SMO"],
        edges=[
            GraphEdge(
                name="invalid_edge",
                type="gene-gene",
                source="PTCH1",
                target="SMO",
            ),
        ],
    )

    validator = GraphValidator()

    try:
        validator.validate(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Validator should reject invalid edge types."
        )



def test_validator_collects_multiple_issues():
    graph = GraphDefinition(
        name="",
        type="invalid",
        nodes=["PTCH1", "PTCH1", ""],
    )

    validator = GraphValidator()

    issues = validator.collect_issues(graph)

    assert len(issues) >= 3
    
    
# ============================================================
# Composer
# ============================================================

from internalnet.graph_engine.composer import GraphComposer


def test_composer_returns_requested_graphs():
    repository = GraphRepository()

    common_graph = make_test_graph("common_shh_signaling")
    cell_graph = make_test_graph("floor_plate_progenitor")

    repository.register(common_graph)
    repository.register(cell_graph)

    composer = GraphComposer(repository)

    composed = composer.compose([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert composed == (
        common_graph,
        cell_graph,
    )


def test_composer_preserves_requested_order():
    repository = GraphRepository()

    graph_a = make_test_graph("graph_a")
    graph_b = make_test_graph("graph_b")

    repository.register(graph_a)
    repository.register(graph_b)

    composer = GraphComposer(repository)

    composed = composer.compose([
        "graph_b",
        "graph_a",
    ])

    assert composed == (
        graph_b,
        graph_a,
    )


def test_composer_accepts_single_graph():
    repository = GraphRepository()

    graph = make_test_graph("single_graph")
    repository.register(graph)

    composer = GraphComposer(repository)

    composed = composer.compose(["single_graph"])

    assert composed == (graph,)


def test_composer_accepts_empty_graph_list():
    repository = GraphRepository()

    composer = GraphComposer(repository)

    composed = composer.compose([])

    assert composed == ()


def test_composer_raises_for_missing_graph():
    repository = GraphRepository()

    composer = GraphComposer(repository)

    try:
        composer.compose(["missing_graph"])
    except KeyError:
        pass
    else:
        raise AssertionError(
            "Composer should raise KeyError for a missing graph."
        )
        
# ============================================================
# Resolver
# ============================================================

from internalnet.graph_engine.resolver import GraphResolver

def make_common_shh_graph():
    return GraphDefinition(
        name="common_shh_signaling",
        type="common",
        nodes=[
            "PTCH1",
            "SMO",
            "GLI2",
            "SUFU",
            "ATP",
            "enzyme",
            "molecule",
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


def make_floor_plate_graph():
    return GraphDefinition(
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


def test_resolver_returns_all_edges():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.all_edges()

    assert len(edges) == 6


def test_resolver_edges_from_source():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.edges_from("SMO")

    assert len(edges) == 1
    assert edges[0].name == "SMO_GLI2"
    assert edges[0].source == "SMO"
    assert edges[0].target == "GLI2"


def test_resolver_edges_to_target():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.edges_to("FOXA2")

    assert len(edges) == 1
    assert edges[0].name == "H3K27ac_FOXA2"
    assert edges[0].source == "H3K27ac"
    assert edges[0].target == "FOXA2"


def test_resolver_filters_edges_by_type():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.edges_by_type("node-node")

    assert len(edges) == 2

    assert edges[0].name == "PTCH1_SMO"
    assert edges[1].name == "SMO_GLI2"


def test_resolver_filters_edges_from_source_by_type():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.edges_from_by_type(
        "SHH",
        "node-behavior",
    )

    assert len(edges) == 1
    assert edges[0].name == "SHH_release"


def test_resolver_filters_edges_to_target_by_type():
    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    resolver = GraphResolver([
        common_graph,
        cell_graph,
    ])

    edges = resolver.edges_to_by_type(
        "production",
        "gene-behavior",
    )

    assert len(edges) == 2

    assert edges[0].name == "FOXA2_production"
    assert edges[1].name == "SHH_production"


def test_resolver_has_source():
    resolver = GraphResolver([
        make_common_shh_graph(),
        make_floor_plate_graph(),
    ])

    assert resolver.has_source("PTCH1") is True
    assert resolver.has_source("SMO") is True
    assert resolver.has_source("FOXA2") is True
    assert resolver.has_source("missing") is False


def test_resolver_has_target():
    resolver = GraphResolver([
        make_common_shh_graph(),
        make_floor_plate_graph(),
    ])

    assert resolver.has_target("SMO") is True
    assert resolver.has_target("GLI2") is True
    assert resolver.has_target("production") is True
    assert resolver.has_target("missing") is False


def test_resolver_returns_empty_for_unknown_source():
    resolver = GraphResolver([
        make_common_shh_graph(),
        make_floor_plate_graph(),
    ])

    assert resolver.edges_from("missing") == ()


def test_resolver_returns_empty_for_unknown_target():
    resolver = GraphResolver([
        make_common_shh_graph(),
        make_floor_plate_graph(),
    ])

    assert resolver.edges_to("missing") == ()
    
# ============================================================
# Engine
# ============================================================

from internalnet.graph_engine.engine import GraphEngine


def test_engine_registers_valid_graph():
    engine = GraphEngine()

    graph = make_test_graph("test_graph")

    engine.register(graph)

    assert engine.has("test_graph") is True
    assert engine.get("test_graph") is graph


def test_engine_rejects_invalid_graph():
    engine = GraphEngine()

    graph = GraphDefinition(
        name="invalid_graph",
        type="common",
        nodes=["PTCH1", "PTCH1"],
    )

    try:
        engine.register(graph)
    except GraphValidationError:
        pass
    else:
        raise AssertionError(
            "Engine should reject an invalid graph during registration."
        )

    assert engine.has("invalid_graph") is False


def test_engine_composes_graphs():
    engine = GraphEngine()

    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    engine.register(common_graph)
    engine.register(cell_graph)

    composed = engine.compose([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert composed == (
        common_graph,
        cell_graph,
    )


def test_engine_creates_resolver_for_graphs():
    engine = GraphEngine()

    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    engine.register(common_graph)
    engine.register(cell_graph)

    resolver = engine.resolver([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert isinstance(resolver, GraphResolver)

    edges = resolver.edges_from("SMO")

    assert len(edges) == 1
    assert edges[0].name == "SMO_GLI2"


def test_engine_returns_all_composed_edges():
    engine = GraphEngine()

    engine.register(make_common_shh_graph())
    engine.register(make_floor_plate_graph())

    edges = engine.all_edges([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert len(edges) == 6


# ============================================================
# Integration
# ============================================================


def test_graph_engine_full_shh_path():
    """Test the complete Graph Engine path for the v0.7 SHH demo."""

    engine = GraphEngine()

    common_graph = make_common_shh_graph()
    cell_graph = make_floor_plate_graph()

    # Register graph definitions.
    engine.register(common_graph)
    engine.register(cell_graph)

    # Compose the graphs required by the cell.
    composed = engine.compose([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert composed == (
        common_graph,
        cell_graph,
    )

    # Resolve structural relationships.
    resolver = engine.resolver([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    # Common SHH signaling.
    assert [
        edge.name
        for edge in resolver.edges_by_type("node-node")
    ] == [
        "PTCH1_SMO",
        "SMO_GLI2",
    ]

    # Cell-specific regulatory relationship.
    assert [
        edge.name
        for edge in resolver.edges_by_type("node-gene")
    ] == [
        "H3K27ac_FOXA2",
    ]

    # Gene → behavior relationships.
    assert [
        edge.name
        for edge in resolver.edges_by_type("gene-behavior")
    ] == [
        "FOXA2_production",
        "SHH_production",
    ]

    # Node → behavior relationship.
    assert [
        edge.name
        for edge in resolver.edges_by_type("node-behavior")
    ] == [
        "SHH_release",
    ]
    
def test_engine_accepts_cross_graph_behavior_reference():
    """A cell-specific graph may reference a behavior provided by a common graph."""

    engine = GraphEngine()

    common_graph = GraphDefinition(
        name="common_shh_signaling",
        type="common",
        behaviors=["production", "release"],
    )

    cell_graph = GraphDefinition(
        name="floor_plate_progenitor",
        type="cell_specific",
        genes=["FOXA2"],
        edges=[
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ],
    )

    engine.register(common_graph)

    # The behavior "production" belongs to the common graph.
    # The cell-specific graph references it without declaring it locally.
    engine.register(cell_graph)

    composed = engine.compose([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    assert composed == (
        common_graph,
        cell_graph,
    )

    resolver = engine.resolver([
        "common_shh_signaling",
        "floor_plate_progenitor",
    ])

    edges = resolver.edges_to_by_type(
        "production",
        "gene-behavior",
    )

    assert len(edges) == 1
    assert edges[0].source == "FOXA2"
    assert edges[0].target == "production"
    
    
def test_validator_accepts_external_behavior_reference():
    """A cell-specific graph may reference a behavior provided by another graph."""

    graph = GraphDefinition(
        name="floor_plate_progenitor",
        type="cell_specific",
        genes=["FOXA2"],
        edges=[
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ],
    )

    validator = GraphValidator()

    validator.validate(graph)
