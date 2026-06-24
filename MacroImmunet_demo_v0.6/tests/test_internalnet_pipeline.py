# test_internalnet_pipeline.py

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

from cellmaster.internalnet.internalnet import (
    InternalNet
)


def test_internalnet_pipeline():

    print()
    print("============================")
    print("INTERNALNET PIPELINE TEST")
    print("============================")

    # -------------------------
    # build entity
    # -------------------------

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

        template_id="host_cell",

        cell_id="pipeline_test"
    )

    graph_context = entity.runtime_graph

    # -------------------------
    # initial state
    # -------------------------

    print()
    print("BASE STATE")

    base_state = (
        entity.runtime_state.snapshot()
    )

    pprint(base_state)

    # -------------------------
    # run internalnet
    # -------------------------

    internalnet = InternalNet()

    output = internalnet.run(

        runtime_entity=
            entity,

        graph_context=
            graph_context,

        node_inputs=
            {},

        runtime_context=
            {
                "runtime_state":
                    base_state
            },

        tick=1
    )

    # -------------------------
    # states
    # -------------------------

    print()
    print("NODE STATE")

    pprint(
        output[
            "node_runtime_state"
        ]
    )

    print()
    print("PASSIVE STATE")

    pprint(
        output[
            "passive_runtime_state"
        ]
    )

    print()
    print("MODULATED STATE")

    pprint(
        output[
            "modulated_runtime_state"
        ]
    )

    # -------------------------
    # identity check
    # -------------------------

    print()
    print("OBJECT IDS")

    print(
        "base      :",
        id(base_state)
    )

    print(
        "node      :",
        id(
            output[
                "node_runtime_state"
            ]
        )
    )

    print(
        "passive   :",
        id(
            output[
                "passive_runtime_state"
            ]
        )
    )

    print(
        "modulated :",
        id(
            output[
                "modulated_runtime_state"
            ]
        )
    )

    # -------------------------
    # assertions
    # -------------------------

    assert (
        "node_runtime_state"
        in output
    )

    assert (
        "passive_runtime_state"
        in output
    )

    assert (
        "modulated_runtime_state"
        in output
    )

    print()
    print("PASS")


if __name__ == "__main__":

    test_internalnet_pipeline()
