# cellmaster/scheduler/scheduling_policy.py


# =========================================
# apply scheduling policy
# =========================================

def apply_scheduling_policy(
    runtime_context,
    scheduler_config=None
):

    """
    orchestration-level runtime policy

    determines whether runtime
    is actually executed this tick
    """

    if scheduler_config is None:

        scheduler_config = {}

    policy = scheduler_config.get(
        "policy",
        "event_driven"
    )

    tick = runtime_context.get(
        "tick",
        0
    )

    persistent_runtime = runtime_context.get(
        "persistent_runtime",
        False
    )

    runtime_priority = runtime_context.get(
        "runtime_priority",
        0.0
    )

    runtime_allowed = runtime_context.get(
        "runtime_allowed",
        True
    )

    updated = dict(runtime_context)

    # =====================================
    # hard blocked
    # =====================================

    if not runtime_allowed:

        updated["execute_runtime"] = False

        updated["schedule_reason"] = (
            "cooldown_block"
        )

        return updated

    # =====================================
    # always run
    # =====================================

    if policy == "always_run":

        updated["execute_runtime"] = True

        updated["schedule_reason"] = (
            "always_run"
        )

        return updated

    # =====================================
    # persistent runtime
    # =====================================

    if policy == "persistent":

        updated["execute_runtime"] = (
            persistent_runtime
        )

        updated["schedule_reason"] = (
            "persistent_runtime"
        )

        return updated

    # =====================================
    # periodic execution
    # =====================================

    if policy == "periodic":

        interval = scheduler_config.get(
            "period_interval",
            5
        )

        updated["execute_runtime"] = (
            tick % interval == 0
        )

        updated["schedule_reason"] = (
            "periodic_runtime"
        )

        return updated

    # =====================================
    # budget-limited mode
    # =====================================

    if policy == "budget_limited":

        threshold = scheduler_config.get(
            "priority_threshold",
            0.5
        )

        updated["execute_runtime"] = (
            runtime_priority >= threshold
        )

        updated["schedule_reason"] = (
            "budget_priority_gate"
        )

        return updated

    # =====================================
    # default:
    # event-driven
    # =====================================

    has_signals = bool(

        runtime_context.get(
            "signals",
            []
        )
    )

    updated["execute_runtime"] = (
        has_signals
        or persistent_runtime
    )

    updated["schedule_reason"] = (
        "event_driven"
    )

    return updated
