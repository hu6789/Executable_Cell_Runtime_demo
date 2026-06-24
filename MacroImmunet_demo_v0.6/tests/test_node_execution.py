# test_node_execution.py

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

from cellmaster.internalnet.node_engine.node_engine import (
    NodeEngine
)


# =========================================
# TEST
# =========================================

def test_node_execution():

    print()
    print("============================")
    print("NODE EXECUTION TEST")
    print("============================")

    # ---------------------------------
    # build entity
    # ---------------------------------

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

    entity = factory.create_runtime_entity(

        template_id=
            "host_cell",

        cell_id=
            "test_cell"
    )

    graph_context = entity.runtime_graph

    # ---------------------------------
    # runtime context
    # ---------------------------------

    runtime_context = {

        "runtime_state": {

            "ATP": 10.0,

            "ROS": 5.0,

            "cell_membrane": 0.8,

            "IFN": 2.0,

            "viral_signal": 3.0,

            "viral_RNA": 1.0,

            "viral_protein": 1.0,

            "capsid": 1.0,

            "Ca": 0.5
        }
    }

    # ---------------------------------
    # run node engine
    # ---------------------------------

    engine = NodeEngine()

    results = engine.evaluate_nodes(

        node_definitions=
            graph_context.get_runtime_nodes(),

        runtime_context=
            runtime_context,

        graph_context=
            graph_context
    )

    # ---------------------------------
    # output
    # ---------------------------------

    print()
    print("NODE RESULT COUNT")

    print(
        len(results)
    )

    print()

    for result in results:

        print("===================")

        print(
            result["node_id"]
        )

        pprint(
            result
        )

        print()

    # ---------------------------------
    # assertions
    # ---------------------------------

    assert len(results) > 0

    for result in results:

        assert "node_id" in result

        assert "runtime_value" in result

        assert "gate_result" in result

        assert "clamp_result" in result

        assert (
            "node_runtime_result"
            in result
        )

    print()
    print("PASS")


# =========================================

if __name__ == "__main__":

    test_node_execution()
