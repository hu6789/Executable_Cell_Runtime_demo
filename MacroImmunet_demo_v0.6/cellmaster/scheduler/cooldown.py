# cellmaster/scheduler/cooldown.py


# =========================================
# evaluate cooldown state
# =========================================

def evaluate_cooldown(
    runtime_context,
    runtime_records
):

    """
    runtime refractory evaluation

    prevents:
        - infinite activation loops
        - ultra-high-frequency runtime
        - unstable oscillation
    """

    cell_id = runtime_context.get(
        "cell_id"
    )

    runtime_record = runtime_records.get(

        cell_id,
        {}
    )

    cooldown_ticks = runtime_record.get(
        "cooldown_ticks",
        0
    )

    activation_count = runtime_record.get(
        "activation_count",
        0
    )

    updated = dict(runtime_context)

    # =====================================
    # active cooldown
    # =====================================

    if cooldown_ticks > 0:

        updated["cooldown_active"] = True

        updated["cooldown_ticks"] = (
            cooldown_ticks - 1
        )

        updated["runtime_allowed"] = False

        return updated

    # =====================================
    # adaptive refractory
    # =====================================

    adaptive_cooldown = (
        compute_adaptive_cooldown(
            activation_count
        )
    )

    updated["cooldown_active"] = False

    updated["cooldown_ticks"] = (
        adaptive_cooldown
    )

    updated["runtime_allowed"] = True

    return updated


# =========================================
# adaptive cooldown scaling
# =========================================

def compute_adaptive_cooldown(
    activation_count
):

    """
    simple runtime stabilization rule
    """

    # -------------------------------------
    # low activation
    # -------------------------------------

    if activation_count < 5:

        return 0

    # -------------------------------------
    # moderate activation
    # -------------------------------------

    if activation_count < 20:

        return 1

    # -------------------------------------
    # heavy activation
    # -------------------------------------

    return 2
