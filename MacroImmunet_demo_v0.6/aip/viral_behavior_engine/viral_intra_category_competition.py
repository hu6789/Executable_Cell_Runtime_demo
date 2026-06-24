# cellmaster/internalnet/behavior_engine/viral_intra_category_competition.py


# =========================================
# Intra Category Competition
# =========================================

def perform_intra_category_competition(
    allocation_context
):

    """
    perform local program competition
    inside each behavior category

    responsibilities:
        - construct local category competition
        - allocate behavior-level runtime share
        - suppress weak competing programs
        - generate behavior competition weights

    DOES NOT:
        - compute graph contribution
        - compute final behavior drive
        - execute behaviors
    """

    behavior_defs = allocation_context.get(
        "behavior_defs",
        {}
    )

    category_allocation = (
        allocation_context.get(
            "category_allocation",
            {}
        )
    )

    competition_result = {}

    # =====================================
    # group behaviors by category
    # =====================================

    grouped = group_behaviors_by_category(
        behavior_defs
    )

    # =====================================
    # process category competition
    # =====================================

    for category, behaviors in (
        grouped.items()
    ):

        category_share = (
            category_allocation.get(
                category,
                0.0
            )
        )

        competition_result[
            category
        ] = compute_local_competition(

            behaviors,
            category_share
        )

    # =====================================
    # attach competition result
    # =====================================

    updated_context = dict(
        allocation_context
    )

    updated_context[
        "behavior_competition"
    ] = competition_result

    return updated_context


# =========================================
# Group Behaviors By Category
# =========================================

def group_behaviors_by_category(
    behavior_defs
):

    grouped = {}

    for behavior_name, behavior_def in (
        behavior_defs.items()
    ):

        category = behavior_def.get(
            "behavior_category",
            "misc"
        )

        grouped.setdefault(
            category,
            []
        ).append({

            "behavior_name":
                behavior_name,

            "behavior_def":
                behavior_def
        })

    return grouped


# =========================================
# Local Competition
# =========================================

def compute_local_competition(
    behaviors,
    category_share,
    viral_bias=None
):

    result = {}

    total_priority = 0.0

    boost_map = (viral_bias or {}).get("boost", {})
    suppress_map = (viral_bias or {}).get("suppress", {})

    # =====================================
    # compute total priority (clean, no mutation)
    # =====================================

    weighted_priorities = []

    for item in behaviors:

        name = item.get("behavior_name")
        behavior_def = item.get("behavior_def", {})

        priority = behavior_def.get("runtime_priority", 1.0)

        # apply viral influence ON READ ONLY
        if name in boost_map:
            priority *= (1.0 + boost_map[name])

        if name in suppress_map:
            priority *= (1.0 - suppress_map[name])

        weighted_priorities.append((name, priority))
        total_priority += priority

    if total_priority <= 0:
        total_priority = 1.0

    # =====================================
    # allocate
    # =====================================

    for name, priority in weighted_priorities:

        local_share = priority / total_priority
        final_share = local_share * category_share

        result[name] = {
            "category_share": category_share,
            "local_share": local_share,
            "competition_weight": final_share
        }

    return result
