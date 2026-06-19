# cellmaster/scheduler/priority.py


# =========================================
# compute runtime priority
# =========================================

def compute_runtime_priority(
    runtime_context
):

    """
    compute scheduler runtime priority

    used for:
        - budget allocation
        - ROI-first execution
        - critical runtime dispatch
    """

    urgency = runtime_context.get(
        "runtime_urgency",
        0.0
    )

    persistent_runtime = runtime_context.get(
        "persistent_runtime",
        False
    )

    activation_source = runtime_context.get(
        "activation_source"
    )

    signals = runtime_context.get(
        "signals",
        []
    )

    # =====================================
    # base priority
    # =====================================

    priority = urgency

    # =====================================
    # persistence bonus
    # =====================================

    if persistent_runtime:

        priority += 0.3

    # =====================================
    # activation-source weighting
    # =====================================

    source_bonus = {

        "contact_activation": 0.5,

        "binding_activation": 0.7,

        "field_activation": 0.2,

        "generic_activation": 0.1
    }

    priority += source_bonus.get(
        activation_source,
        0.0
    )

    # =====================================
    # danger signal amplification
    # future:
    # damage / stress / death signals
    # =====================================

    for signal in signals:

        internal_signal = signal.get(
            "internal_signal"
        )

        if internal_signal in [

            "damage_detected",
            "stress_response",
            "death_signal"
        ]:

            priority += 1.0

    # =====================================
    # runtime class
    # =====================================

    runtime_class = classify_runtime(
        priority
    )

    updated = dict(runtime_context)

    updated["runtime_priority"] = (
        priority
    )

    updated["runtime_class"] = (
        runtime_class
    )

    return updated


# =========================================
# classify runtime class
# =========================================

def classify_runtime(
    priority
):

    """
    runtime execution tier
    """

    if priority >= 1.5:

        return "critical_runtime"

    if priority >= 0.7:

        return "active_runtime"

    return "background_runtime"
