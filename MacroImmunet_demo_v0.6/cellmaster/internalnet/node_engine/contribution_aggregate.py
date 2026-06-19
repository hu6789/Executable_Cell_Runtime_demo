# cellmaster/internalnet/node_engine/contribution_aggregate.py


# =========================================
# Aggregate Contribution Categories
# =========================================

def aggregate_contribution_groups(
    grouped_contributions
):

    """
    aggregate contributions
    within each semantic category

    responsibilities:
        - intra-category aggregation
        - participation requirement handling
        - category statistics generation

    DOES NOT:
        - apply node skeleton
        - apply runtime gates
        - perform cross-category logic
    """

    aggregated = {}

    for category, contributions in (
        grouped_contributions.items()
    ):

        aggregated[category] = (

            aggregate_single_category(
                category,
                contributions
            )
        )

    return aggregated


# =========================================
# Aggregate Single Category
# =========================================

def aggregate_single_category(
    category,
    contributions
):

    if len(contributions) == 0:

        return build_empty_category(
            category
        )

    # =====================================
    # participation evaluation
    # =====================================

    participation_ok = (
        evaluate_participation_requirements(
            contributions
        )
    )

    if not participation_ok:

        return build_empty_category(
            category
        )

    # =====================================
    # collect values
    # =====================================

    values = []

    for contribution in contributions:

        values.append(

            contribution.get(
                "value",
                0.0
            )
        )

    # =====================================
    # aggregate statistics
    # =====================================

    total = sum(values)

    maximum = max(values)

    minimum = min(values)

    average = (
        total / len(values)
    )

    # =====================================
    # source tracking
    # =====================================

    sources = [

        contribution.get("source")

        for contribution in contributions
    ]

    return {

        "category":
            category,

        "active":
            True,

        "value":
            total,

        "average":
            average,

        "maximum":
            maximum,

        "minimum":
            minimum,

        "count":
            len(values),

        "sources":
            sources
    }


# =========================================
# Participation Requirement Evaluation
# =========================================

def evaluate_participation_requirements(
    contributions
):

    """
    participation modes:
        - all_required
        - any_required
        - optional
    """

    all_required = []

    any_required = []

    optional = []

    for contribution in contributions:

        requirement = contribution.get(
            "participation_requirement",
            "optional"
        )

        value = contribution.get(
            "value",
            0.0
        )

        active = (
            value > 0.0
        )

        if requirement == "all_required":

            all_required.append(
                active
            )

        elif requirement == "any_required":

            any_required.append(
                active
            )

        else:

            optional.append(
                active
            )

    # =====================================
    # all_required
    # =====================================

    if len(all_required) > 0:

        if not all(all_required):

            return False

    # =====================================
    # any_required
    # =====================================

    if len(any_required) > 0:

        if not any(any_required):

            return False

    return True


# =========================================
# Empty Category
# =========================================

def build_empty_category(
    category
):

    return {

        "category":
            category,

        "active":
            False,

        "value":
            0.0,

        "average":
            0.0,

        "maximum":
            0.0,

        "minimum":
            0.0,

        "count":
            0,

        "sources":
            []
    }
