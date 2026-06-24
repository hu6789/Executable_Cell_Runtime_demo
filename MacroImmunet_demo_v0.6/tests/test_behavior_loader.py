# test_behavior_loader.py

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


def test_behavior_loader():

    print()
    print("============================")
    print("BEHAVIOR LOADER TEST")
    print("============================")

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

    behavior_defs = (
        graph_context.get_behavior_defs()
    )

    print()
    print("LOADED BEHAVIORS")
    print(
        list(
            behavior_defs.keys()
        )
    )

    print()

    for behavior_name, behavior_def in (
        behavior_defs.items()
    ):

        print("================================")
        print(behavior_name)
        print("================================")

        pprint(behavior_def)

        assert (
            "behavior_type"
            in behavior_def
        )

        assert (
            "behavior_category"
            in behavior_def
        )

        assert (
            "behavior_skeleton"
            in behavior_def
        )

        assert (
            "behavior_gate"
            in behavior_def
        )

    print()
    print("PASS")


if __name__ == "__main__":

    test_behavior_loader()
