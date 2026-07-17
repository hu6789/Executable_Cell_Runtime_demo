# cellmaster/scheduler/persistence.py


# =========================================
# evaluate runtime persistence
# =========================================

def evaluate_persistence(
    runtime_context,
    runtime_records
):

    """
    determine whether runtime
    should persist beyond
    transient event disappearance.

    examples:
        - translation
        - repair
        - secretion
        - viral replication
        - fate progression
    """

    cell_id = runtime_context.get(
        "cell_id"
    )

    signals = runtime_context.get(
        "signals",
        []
    )

    runtime_record = runtime_records.get(

        cell_id,
        {}
    )

    # -------------------------------------
    # existing persistence
    # -------------------------------------

    persistence_ticks = runtime_record.get(
        "persistence_ticks",
        0
    )

    persistent_runtime = runtime_record.get(
        "persistent_runtime",
        False
    )

    # =====================================
    # evaluate signal-driven persistence
    # =====================================

    detected = detect_persistent_runtime(
        signals
    )

    # -------------------------------------
    # persistent runtime triggered
    # -------------------------------------

    if detected:

        persistent_runtime = True

        persistence_ticks = max(
            persistence_ticks,
            detected
        )

    # -------------------------------------
    # decay persistence
    # -------------------------------------

    elif persistence_ticks > 0:

        persistence_ticks -= 1

        persistent_runtime = (
            persistence_ticks > 0
        )

    else:

        persistent_runtime = False

    # =====================================
    # update context
    # =====================================

    updated = dict(runtime_context)

    updated["persistent_runtime"] = (
        persistent_runtime
    )

    updated["persistence_ticks"] = (
        persistence_ticks
    )

    return updated


# =========================================
# detect persistent runtime
# =========================================

def detect_persistent_runtime(
    signals
):

    """
    estimate persistence duration
    from incoming signals
    """

    for signal in signals:

        internal_signal = signal.get(
            "internal_signal"
        )

        # ---------------------------------
        # secretion programs
        # ---------------------------------

        if internal_signal in [

            "IFNGR_activation",
            "IL2R_activation",
            "TNFR_activation"
        ]:

            return 5

        # ---------------------------------
        # contact persistence
        # ---------------------------------

        if internal_signal == (
            "membrane_contact"
        ):

            return 3

        # ---------------------------------
        # binding persistence
        # ---------------------------------

        if internal_signal == (
            "binding_detected"
        ):

            return 8

    return 0
