# cellmaster/internalnet/node_engine/node_gate.py


# =========================================
# Evaluate Node Runtime Gate
# =========================================

def evaluate_node_runtime_gate(
    node_definition,
    runtime_context,
    aggregated_contributions,
    node_value
):

    """
    node-level runtime gate

    unlike edge contribution gate,
    this evaluates whether the
    final node activation is allowed

    supported gate types:
        - minimum_activation
        - minimum_resource
        - maximum_damage
        - maximum_stress
        - custom_condition
    """

    runtime_gates = node_definition.get(
        "runtime_gates",
        []
    )

    if len(runtime_gates) == 0:

        return {

            "passed":
                True,

            "failed_gate":
                None,

            "gate_type":
                None
        }

    for gate in runtime_gates:

        gate_passed = evaluate_single_gate(

            gate=
                gate,

            runtime_context=
                runtime_context,

            aggregated_contributions=
                aggregated_contributions,

            node_value=
                node_value
        )

        if not gate_passed:

            return {

                "passed":
                    False,

                "failed_gate":
                    gate,

                "gate_type":
                    gate.get(
                        "gate_type"
                    )
            }

    return {

        "passed":
            True,

        "failed_gate":
            None,

        "gate_type":
            None
}


# =========================================
# Evaluate Single Gate
# =========================================

def evaluate_single_gate(
    gate,
    runtime_context,
    aggregated_contributions,
    node_value
):

    gate_type = gate.get(
        "gate_type"
    )

    # =====================================
    # minimum activation
    # =====================================

    if gate_type == "minimum_activation":

        threshold = gate.get(
            "threshold",
            0.0
        )

        activation = get_category_value(

            aggregated_contributions,
            "activation"
        )

        return (
            activation >= threshold
        )

    # =====================================
    # minimum resource
    # =====================================

    if gate_type == "minimum_resource":

        threshold = gate.get(
            "threshold",
            0.0
        )

        resource = get_category_value(

            aggregated_contributions,
            "resource"
        )

        return (
            resource >= threshold
        )

    # =====================================
    # maximum damage
    # =====================================

    if gate_type == "maximum_damage":

        threshold = gate.get(
            "threshold",
            9999.0
        )

        damage = get_category_value(

            aggregated_contributions,
            "damage"
        )

        return (
            damage <= threshold
        )

    # =====================================
    # maximum stress
    # =====================================

    if gate_type == "maximum_stress":

        stress_source = gate.get(
            "source",
            "stress"
        )

        threshold = gate.get(
            "threshold",
            9999.0
        )

        stress_value = resolve_runtime_value(

            runtime_context,
            stress_source
        )

        if stress_value is None:

            return True

        return (
            stress_value <= threshold
        )

    # =====================================
    # minimum node value
    # =====================================

    if gate_type == "minimum_node_value":

        threshold = gate.get(
            "threshold",
            0.0
        )

        return (
            node_value >= threshold
        )

    # =====================================
    # custom condition
    # =====================================

    if gate_type == "custom_condition":

        # placeholder
        return True

    return True


# =========================================
# Get Category Value
# =========================================

def get_category_value(
    aggregated,
    category
):

    category_data = aggregated.get(
        category,
        {}
    )

    if not category_data.get(
        "active",
        False
    ):

        return 0.0

    return category_data.get(
        "value",
        0.0
    )


# =========================================
# Resolve Runtime Value
# =========================================

def resolve_runtime_value(
    runtime_context,
    source_name
):

    runtime_state = runtime_context.get(
        "runtime_state",
        {}
    )

    if source_name in runtime_state:

        return runtime_state[
            source_name
        ]

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    if source_name in runtime_labels:

        return runtime_labels[
            source_name
        ]

    if source_name in runtime_context:

        return runtime_context[
            source_name
        ]

    return None
