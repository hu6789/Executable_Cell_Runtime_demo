# test_node_contribution_flow.py

from pprint import pprint

from cellinstance.templates.template_loader import (
    TemplateLoader
)

from cellinstance.factory.cell_factory import (
    CellFactory
)

from cellmaster.internalnet.runtime_graph.graph_loader import (
    RuntimeGraphLoader
)

from cellmaster.internalnet.node_engine.contribution_gate import (
    evaluate_edge_gate
)

from cellmaster.internalnet.node_engine.contribution_transform import (
    apply_contribution_transform
)

from cellmaster.internalnet.node_engine.contribution_group import (
    group_contributions_by_category
)

from cellmaster.internalnet.node_engine.contribution_aggregate import (
    aggregate_contribution_groups
)

from cellmaster.internalnet.runtime_graph.node_definition_loader import (
    NodeDefinitionLoader
)

from cellmaster.internalnet.node_engine.skeleton_formula import (
    apply_node_skeleton_formula
)


# =========================================
# TEST
# =========================================

def test_node_contribution_flow():

    print()
    print("====================================")
    print("NODE CONTRIBUTION FLOW TEST")
    print("====================================")
    print()

    # -------------------------------------
    # build factory
    # -------------------------------------

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

        cell_id="debug_node"
    )

    graph_context = entity.runtime_graph

    runtime_context = {

        "runtime_state":
            entity.runtime_state.snapshot(),

        "runtime_labels":
            {},

        "tick":
            1
    }

    # =====================================
    # runtime state
    # =====================================

    print("RUNTIME STATE")
    pprint(
        runtime_context["runtime_state"]
    )

    print()

    # =====================================
    # ATP incoming edges
    # =====================================

    incoming_edges = (
        graph_context.get_incoming(
            "ATP"
        )
    )

    print("ATP INCOMING EDGES")
    print(
        f"count = {len(incoming_edges)}"
    )

    print()

    valid_contributions = []

    # =====================================
    # edge by edge
    # =====================================

    for idx, edge in enumerate(
        incoming_edges,
        start=1
    ):

        print("--------------------------------")
        print(
            f"EDGE {idx}"
        )
        print("--------------------------------")

        pprint(edge)

        print()

        # -----------------------------
        # gate
        # -----------------------------

        gate_allowed = (
            evaluate_edge_gate(
                edge,
                runtime_context
            )
        )

        print(
            "gate_allowed =",
            gate_allowed
        )

        print()

        # -----------------------------
        # transform
        # -----------------------------

        transformed = (
            apply_contribution_transform(
                edge,
                runtime_context
            )
        )

        print(
            "transformed ="
        )

        pprint(
            transformed
        )

        print()

        if transformed is not None:

            valid_contributions.append(
                transformed
            )

    # =====================================
    # grouped
    # =====================================

    print()
    print("GROUPED CONTRIBUTIONS")

    grouped = (
        group_contributions_by_category(
            valid_contributions
        )
    )

    pprint(grouped)

    print()

    # =====================================
    # aggregated
    # =====================================

    print("AGGREGATED CONTRIBUTIONS")

    aggregated = (
        aggregate_contribution_groups(
            grouped
        )
    )

    pprint(aggregated)

    print()

    # =====================================
    # ATP node definition
    # =====================================

    loader = NodeDefinitionLoader()

    atp_def = loader.load(
        "ATP"
    )

    print("ATP NODE DEFINITION")

    pprint(atp_def)

    print()

    # =====================================
    # skeleton
    # =====================================

    skeleton_result = (
        apply_node_skeleton_formula(

            node_definition=
                atp_def,

            aggregated_contributions=
                aggregated
        )
    )

    print("SKELETON RESULT")

    pprint(
        skeleton_result
    )

    print()

    print("PASS")


# =========================================

if __name__ == "__main__":

    test_node_contribution_flow()
