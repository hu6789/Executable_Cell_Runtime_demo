# cellmaster/internalnet/node_engine/contribution_gate.py


# =========================================
# Edge Contribution Gate
# =========================================

def evaluate_edge_gate(
    edge,
    runtime_context
):

    """
    evaluate whether
    current edge contribution
    can participate in runtime

    gate types:
        - >
        - <
        - >=
        - <=
        - ==
        - range
    """

    gate = edge.get(
        "contribution_gate"
    )

    # no gate
    if gate is None:

        return True

    source_name = gate.get(
        "source"
    )

    operator = gate.get(
        "operator"
    )

    threshold = gate.get(
        "threshold"
    )

    current_value = (
        resolve_runtime_value(
            runtime_context,
            source_name
        )
    )

    if current_value is None:

        return False

    # =====================================
    # comparison operators
    # =====================================

    if operator == ">":

        return (
            current_value > threshold
        )

    if operator == "<":

        return (
            current_value < threshold
        )

    if operator == ">=":

        return (
            current_value >= threshold
        )

    if operator == "<=":

        return (
            current_value <= threshold
        )

    if operator == "==":

        return (
            current_value == threshold
        )

    # =====================================
    # range operator
    # =====================================

    if operator == "range":

        minimum = gate.get(
            "minimum"
        )

        maximum = gate.get(
            "maximum"
        )

        if minimum is None:

            minimum = float("-inf")

        if maximum is None:

            maximum = float("inf")

        return (
            minimum <= current_value <= maximum
        )

    # unknown operator
    return False


# =========================================
# Resolve Runtime Value
# =========================================

def resolve_runtime_value(
    runtime_context,
    source_name
):

    """
    resolve runtime variable
    from runtime context
    """

    if source_name is None:

        return None

    runtime_state = runtime_context.get(
        "runtime_state",
        {}
    )

    # -------------------------------------
    # runtime state
    # -------------------------------------

    if source_name in runtime_state:

        return runtime_state[
            source_name
        ]

    # -------------------------------------
    # runtime labels
    # -------------------------------------

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    if source_name in runtime_labels:

        return runtime_labels[
            source_name
        ]

    # -------------------------------------
    # runtime metadata
    # -------------------------------------

    if source_name in runtime_context:

        return runtime_context[
            source_name
        ]

    return None
