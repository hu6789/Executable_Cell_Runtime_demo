# cellmaster/scheduler/budget_allocator.py


# =========================================
# allocate runtime execution budget
# =========================================

def allocate_runtime_budget(
    runtime_contexts,
    scheduler_config=None
):

    """
    runtime budget allocator

    used for:
        - large-scale simulation
        - throttling
        - ROI-first execution
        - GPU batching
    """

    if scheduler_config is None:

        scheduler_config = {}

    max_runtime_per_tick = scheduler_config.get(
        "max_runtime_per_tick",
        128
    )

    # =====================================
    # filter executable runtime
    # =====================================

    executable = []

    blocked = []

    for context in runtime_contexts:

        if context.get(
            "execute_runtime",
            False
        ):

            executable.append(
                context
            )

        else:

            blocked.append(
                context
            )

    # =====================================
    # sort by priority
    # =====================================

    executable.sort(

        key=lambda x: x.get(
            "runtime_priority",
            0.0
        ),

        reverse=True
    )

    # =====================================
    # allocate runtime budget
    # =====================================

    accepted = executable[
        :max_runtime_per_tick
    ]

    deferred = executable[
        max_runtime_per_tick:
    ]

    # =====================================
    # annotate accepted
    # =====================================

    for context in accepted:

        context["budget_status"] = (
            "accepted"
        )

    # =====================================
    # annotate deferred
    # =====================================

    for context in deferred:

        context["budget_status"] = (
            "deferred"
        )

        context["execute_runtime"] = False

    # =====================================
    # annotate blocked
    # =====================================

    for context in blocked:

        context["budget_status"] = (
            "blocked"
        )

    return accepted
