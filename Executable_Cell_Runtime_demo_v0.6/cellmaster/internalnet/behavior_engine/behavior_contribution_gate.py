# cellmaster/internalnet/behavior/behavior_contribution_gate.py

# =========================================
# TODO (v0.6)
# =========================================
#
# 1.
# participation_requirement
# currently not enforced.
#
# supported semantics:
#
#     all_required
#     any_required
#     optional
#
# current implementation only performs
# edge-level eligibility filtering.
#
# category-level participation validation
# will be added later.
#
#
# 2.
# source currently resolves directly from
# runtime_state[source].
#
# future versions may support:
#
#     node outputs
#     passive outputs
#     viral behavior outputs
#     runtime_state
#
# through a unified:
#
#     resolve_contribution_source()
#
#
# 3.
# contribution source type is currently
# assumed to be node/runtime variable.
#
# future graph edges may define:
#
#     source_type
#
# to support heterogeneous contribution
# providers.
#
# =========================================
# =========================================
# Behavior Contribution Gate
# =========================================

def evaluate_behavior_contribution_gate(
    behavior_name,
    competition_context,
    graph_context
):

    """
    evaluate behavior contribution eligibility

    responsibilities:
        - evaluate edge-level gates
        - determine contribution participation
        - filter invalid contributions
        - construct gated contribution context

    DOES NOT:
        - compute final behavior strength
        - aggregate contributions
        - evaluate final behavior gate
    """

    runtime_state = (
        competition_context.get(
            "runtime_state",
            {}
        )
    )

    behavior_edges = graph_context.get_runtime_edges()
    
    accepted = []

    # =====================================
    # iterate edges
    # =====================================

    for edge in behavior_edges:

        if edge.get("edge_type") != "node_to_behavior":
            continue

        # -----------------------------
        # behavior target filtering
        # -----------------------------

        target = edge.get(
            "target"
        )

        if target != behavior_name:

            continue

        # -----------------------------
        # evaluate edge gate
        # -----------------------------

        allowed = evaluate_edge_gate(

            edge,
            runtime_state
        )

        if not allowed:

            continue

        # -----------------------------
        # build contribution
        # -----------------------------

        source_node = edge.get(
            "source"
        )

        node_value = runtime_state.get(
            source_node,
            0.0
        )

        contribution = {

            "source":
                source_node,

            "target":
                behavior_name,

            "raw_value":
                node_value,

            "weight":
                edge.get(
                    "weight",
                    1.0
                ),

            "transform":
                edge.get(
                    "transform",
                    "linear"
                ),

            "category":
                edge.get(
                    "contribution_category",
                    "activation"
                ),

            "participation_requirement":
                edge.get(
                    "participation_requirement",
                    "optional"
                ),

            "edge":
                edge
        }

        accepted.append(
            contribution
        )

    return accepted


# =========================================
# Edge Gate Evaluation
# =========================================

def evaluate_edge_gate(
    edge,
    runtime_state
):

    """
    evaluate contribution eligibility gate
    """

    gate = edge.get(
        "contribution_gate"
    )

    if gate is None:

        return True

    node = gate.get(
        "node"
    )

    operator = gate.get(
        "operator"
    )

    threshold = gate.get(
        "value"
    )

    runtime_value = runtime_state.get(
        node,
        0.0
    )

    # =====================================
    # comparison operators
    # =====================================

    if operator == ">":

        return runtime_value > threshold

    if operator == "<":

        return runtime_value < threshold

    if operator == ">=":

        return runtime_value >= threshold

    if operator == "<=":

        return runtime_value <= threshold

    if operator == "==":

        return runtime_value == threshold

    if operator == "range":

        lower = gate.get(
            "min",
            float("-inf")
        )

        upper = gate.get(
            "max",
            float("inf")
        )

        return (
            lower <= runtime_value <= upper
        )

    return True
