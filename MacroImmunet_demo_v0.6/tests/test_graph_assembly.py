# tests/test_graph_assembly.py

from pprint import pprint

from cellinstance.templates.template_loader import (
    TemplateLoader
)

from cellmaster.internalnet.runtime_graph.graph_loader import (
    RuntimeGraphLoader
)

from cellinstance.factory.cell_factory import (
    CellFactory
)


# =========================================
# Graph Assembly Test
# =========================================

def test_graph_assembly():

    print()
    print("============================")
    print("GRAPH ASSEMBLY TEST")
    print("============================")

    # =====================================
    # build factory
    # =====================================

    template_loader = TemplateLoader()

    template_loader.load_template_directory(
        "cellinstance/cells"
    )

    factory = CellFactory(

        template_loader=
            template_loader,

        runtime_graph_loader=
            RuntimeGraphLoader()
    )

    # =====================================
    # create entity
    # =====================================

    entity = factory.create_runtime_entity(

        template_id=
            "host_cell",

        cell_id=
            "test_cell"
    )

    graph_context = entity.runtime_graph

    # =====================================
    # nodes
    # =====================================

    nodes = graph_context.get_runtime_nodes()

    print()
    print("NODES")
    pprint(nodes)

    # =====================================
    # behaviors
    # =====================================

    behaviors = (
        graph_context.get_runtime_behaviors()
    )

    print()
    print("BEHAVIORS")
    pprint(behaviors)

    # =====================================
    # edges
    # =====================================

    edges = (
        graph_context.get_runtime_edges()
    )

    print()
    print("EDGE COUNT")
    print(len(edges))

    # =====================================
    # node->behavior edges
    # =====================================

    node_behavior_edges = (
        graph_context.get_edges_by_type(
            "node_to_behavior"
        )
    )

    print()
    print("NODE_TO_BEHAVIOR EDGE COUNT")
    print(len(node_behavior_edges))

    # =====================================
    # behavior defs
    # =====================================

    behavior_defs = (
        graph_context.get_behavior_defs()
    )

    print()
    print("BEHAVIOR DEFINITIONS")
    print(
        list(
            behavior_defs.keys()
        )
    )

    # =====================================
    # assertions
    # =====================================

    assert len(nodes) > 0, (
        "no runtime nodes loaded"
    )

    assert len(behaviors) > 0, (
        "no runtime behaviors loaded"
    )

    assert len(edges) > 0, (
        "no runtime edges loaded"
    )

    assert len(node_behavior_edges) > 0, (
        "no node_to_behavior edges loaded"
    )

    assert len(behavior_defs) > 0, (
        "no behavior definitions loaded"
    )

    # =====================================
    # optional sanity checks
    # =====================================

    print()
    print("GRAPH SUMMARY")

    print(
        "node_count =",
        len(nodes)
    )

    print(
        "behavior_count =",
        len(behaviors)
    )

    print(
        "edge_count =",
        len(edges)
    )

    print()
    print("PASS")


# =========================================

if __name__ == "__main__":

    test_graph_assembly()
