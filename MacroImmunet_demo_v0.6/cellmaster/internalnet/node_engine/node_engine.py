# cellmaster/internalnet/node_engine/node_engine.py


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

from cellmaster.internalnet.node_engine.skeleton_formula import (
    apply_node_skeleton_formula
)

from cellmaster.internalnet.node_engine.node_gate import (
    evaluate_node_runtime_gate
)

from cellmaster.internalnet.node_engine.runtime_clamp import (
    apply_runtime_clamp
)

from cellmaster.internalnet.node_engine.node_runtime_result import (
    build_node_runtime_result
)

from cellmaster.internalnet.runtime_graph.node_definition_loader import (
    NodeDefinitionLoader
)

# =========================================
# Node Runtime Engine
# =========================================

class NodeEngine:

    """
    runtime node calculation layer

    responsibilities:
        - evaluate graph contributions
        - aggregate contribution categories
        - execute node skeleton
        - apply node runtime gates
        - apply runtime clamp
        - generate node delta

    DOES NOT:
        - write runtime state
        - execute behaviors
        - apply HIR
    """

    def __init__(self):

        pass

    # =====================================
    # evaluate all runtime nodes
    # =====================================

    def evaluate_nodes(

        self,
        node_definitions,
        runtime_context,
        graph_context
    ):

        node_results = []

        loader = NodeDefinitionLoader()

        for node_name in node_definitions:

            node_definition = loader.load(
                node_name
            )

            result = self.evaluate_node(

                node_definition,
                runtime_context,
                graph_context
            )

            if result is not None:

                node_results.append(
                    result
                )

        return node_results

    # =====================================
    # single node runtime
    # =====================================

    def evaluate_node(

        self,
        node_definition,
        runtime_context,
        graph_context
    ):

        node_id = node_definition.get(
            "node_id"
        )

        if node_id is None:

            return None

        # =================================
        # collect incoming graph edges
        # =================================

        incoming_edges = (
            graph_context.get_incoming(
                node_id
            )
        )

        valid_contributions = []

        # =================================
        # evaluate graph contributions
        # =================================

        for edge in incoming_edges:

            # -----------------------------
            # edge runtime gate
            # -----------------------------

            gate_allowed = (
                evaluate_edge_gate(

                    edge=edge,
                    runtime_context=
                        runtime_context
                )
            )

            if not gate_allowed:

                continue

            # -----------------------------
            # contribution transform
            # -----------------------------

            transformed = (
                apply_contribution_transform(

                    edge=edge,

                    runtime_context=
                        runtime_context
                )
            )

            if transformed is None:

                continue

            valid_contributions.append(
                transformed
            )

        # =================================
        # group by category
        # =================================

        grouped_contributions = (
            group_contributions_by_category(
                valid_contributions
            )
        )

        # =================================
        # aggregate category contributions
        # =================================

        aggregated_contributions = (
            aggregate_contribution_groups(
                grouped_contributions
            )
        )

        # =================================
        # apply node skeleton
        # =================================

        skeleton_result = (
            apply_node_skeleton_formula(

                node_definition=
                    node_definition,

                aggregated_contributions=
                    aggregated_contributions
            )
        )

        runtime_value = skeleton_result[
            "raw_value"
        ]

        # =================================
        # evaluate node runtime gate
        # =================================

        gate_result = (
            evaluate_node_runtime_gate(

                node_definition=
                    node_definition,

                aggregated_contributions=
                    aggregated_contributions,

                runtime_context=
                    runtime_context,

                node_value=
                    runtime_value
            )
        )

        if not gate_result["passed"]:

            runtime_value = 0.0

        # =================================
        # apply runtime clamp
        # =================================

        clamp_result = (
            apply_runtime_clamp(

                value=
                    runtime_value,

                clamp_config=
                    node_definition,

                runtime_context=
                    runtime_context
            )
        )

        clamped_value = clamp_result[
            "clamped_value"
        ]

        # =================================
        # generate node delta
        # =================================

        node_runtime_result = (
            build_node_runtime_result(

                node_definition=
                    node_definition,

                previous_value=
                    runtime_context.get(
                        "runtime_state",
                        {}
                    ).get(
                        node_id,
                        0.0
                    ),

                computed_value=
                    skeleton_result[
                        "raw_value"
                    ],

                final_value=
                    clamped_value,

                gate_passed=
                    gate_result[
                        "passed"
                    ],

                aggregated_contributions=
                    aggregated_contributions,

                runtime_metadata=
                    {

                        "skeleton_result":
                            skeleton_result,

                        "gate_result":
                            gate_result,

                        "clamp_result":
                            clamp_result
                    }
            )
        )

        return {

            "node_id":
                node_id,

            "runtime_value":
                clamped_value,

            "skeleton_result":
                skeleton_result,

            "gate_result":
                gate_result,

            "clamp_result":
                clamp_result,

            "aggregated_contributions":
                aggregated_contributions,

            "node_runtime_result":
                node_runtime_result
        }
