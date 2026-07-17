# cellmaster/scheduler/runtime_trigger.py


# =========================================
# collect runtime triggers
# =========================================

def collect_runtime_triggers(
    node_inputs,
    runtime_records
):

    """
    build runtime trigger contexts

    sources:
        - external node inputs
        - persistent runtime memory
        - internal runtime continuation
    """

    contexts = []

    for item in node_inputs:

        context = build_trigger_context(

            item,
            runtime_records
        )

        if context is not None:

            contexts.append(
                context
            )

    return contexts


# =========================================
# build single trigger context
# =========================================

def build_trigger_context(
    node_input,
    runtime_records
):

    target_id = node_input.get(
        "target_id"
    )

    signals = node_input.get(
        "node_inputs",
        []
    )

    # -------------------------------------
    # empty input
    # -------------------------------------

    if not signals:

        return None

    # -------------------------------------
    # runtime record
    # -------------------------------------

    runtime_record = runtime_records.get(

        target_id,
        {}
    )

    # -------------------------------------
    # activation source
    # -------------------------------------

    activation_source = (
        determine_activation_source(
            signals
        )
    )

    # -------------------------------------
    # urgency estimation
    # -------------------------------------

    urgency = estimate_runtime_urgency(
        signals
    )

    # -------------------------------------
    # persistent runtime
    # -------------------------------------

    persistent = runtime_record.get(
        "persistent_runtime",
        False
    )

    # -------------------------------------
    # build context
    # -------------------------------------

    context = {

        "cell_id": target_id,

        "activation_source":
            activation_source,

        "signals": signals,

        "runtime_urgency":
            urgency,

        "persistent_runtime":
            persistent,

        "runtime_record":
            runtime_record
    }

    return context


# =========================================
# determine activation source
# =========================================

def determine_activation_source(
    signals
):

    if not signals:

        return "idle"

    signal_types = {

        s.get(
            "input_type"
        )

        for s in signals
    }

    # -------------------------------------
    # field driven
    # -------------------------------------

    if "field_signal" in signal_types:

        return "field_activation"

    # -------------------------------------
    # contact driven
    # -------------------------------------

    if "contact_signal" in signal_types:

        return "contact_activation"

    # -------------------------------------
    # binding driven
    # -------------------------------------

    if "binding_signal" in signal_types:

        return "binding_activation"

    return "generic_activation"


# =========================================
# urgency estimation
# =========================================

def estimate_runtime_urgency(
    signals
):

    if not signals:

        return 0.0

    strengths = []

    for signal in signals:

        strengths.append(

            signal.get(
                "strength",
                0.0
            )
        )

    if not strengths:

        return 0.0

    # simple max urgency
    return max(strengths)
