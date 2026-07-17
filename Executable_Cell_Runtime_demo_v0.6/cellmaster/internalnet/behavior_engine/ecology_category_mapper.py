# cellmaster/internalnet/behavior_engine/ecology_category_mapper.py


# =========================================
# Ecology → Behavior Category Mapping
# =========================================

ECOLOGY_TO_BEHAVIOR_CATEGORY = {

    "survival": [
        "metabolism"
    ],

    "repair": [
        "repair"
    ],

    "secretion": [
        "communication",
        "secretion"
    ],

    "mobility": [
        "migration"
    ],

    "proliferation": [
        "cytotoxicity",
        "misc"
    ]
}


# =========================================
# Ecology → Behavior Allocation
# =========================================

def map_ecology_to_behavior_categories(
    ecology_allocation
):

    """
    translate ecology-level allocation
    into behavior-category allocation
    """

    behavior_allocation = {}

    # -------------------------------------
    # distribute ecology allocation
    # -------------------------------------

    for ecology_category, behavior_categories in (
        ECOLOGY_TO_BEHAVIOR_CATEGORY.items()
    ):

        ecology_share = ecology_allocation.get(
            ecology_category,
            0.0
        )

        if not behavior_categories:
            continue

        share = (
            ecology_share /
            len(behavior_categories)
        )

        for category in behavior_categories:

            behavior_allocation[
                category
            ] = share

    # -------------------------------------
    # normalize
    # -------------------------------------

    total = sum(
        behavior_allocation.values()
    )

    if total > 0:

        for category in behavior_allocation:

            behavior_allocation[
                category
            ] /= total

    return behavior_allocation
