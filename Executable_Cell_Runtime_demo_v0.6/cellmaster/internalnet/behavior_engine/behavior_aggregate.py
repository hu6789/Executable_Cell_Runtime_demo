# cellmaster/internalnet/behavior_engine/behavior_aggregate.py

"""
Category Aggregation Layer

purpose:

    aggregate contributions
    within same semantic category

examples:

    activation:
        additive

    suppression:
        additive

    amplification:
        multiplicative

    resource:
        limiting

aggregation is category-level

behavior drive
is NOT computed here

final drive computation
belongs to behavior skeleton
"""
# =========================================
# Behavior Category Aggregation
# =========================================

def aggregate_behavior_groups(
    grouped_contributions
):

    """
    aggregate grouped behavior contributions

    responsibilities:
        - perform category-level aggregation
        - support different aggregation strategies
        - generate unified category runtime values

    DOES NOT:
        - compute final behavior drive
        - evaluate behavior gate
        - execute behaviors
    """

    aggregated = {}

    for category, contributions in (
        grouped_contributions.items()
    ):

        strategy = determine_strategy(
            category
        )

        aggregated[
            category
        ] = aggregate_category(

            contributions,
            strategy
        )

    return aggregated


# =========================================
# Aggregation Strategy
# =========================================
"""
Aggregation Strategy

category semantics
and aggregation semantics
are intentionally separated.

future versions may allow:

    graph-defined strategy

instead of
category-defined strategy.
"""
def determine_strategy(
    category
):

    """
    determine category aggregation logic
    """

    # additive signal accumulation
    if category in [

        "activation",
        "suppression",
        "damage"
    ]:

        return "additive"

    # multiplicative enhancement
    if category in [

        "amplification"
    ]:

        return "multiplicative"

    # limiting/saturation
    if category in [

        "resource",
        "stabilization"
    ]:

        return "limiting"

    # destabilization competition
    if category in [

        "destabilization"
    ]:

        return "saturation"

    return "additive"


# =========================================
# Aggregate Category
# =========================================

def aggregate_category(
    contributions,
    strategy
):

    values = [

        contribution.get(
            "transformed_value",
            0.0
        )

        for contribution
        in contributions
    ]

    if not values:

        if strategy == "multiplicative":
            return 1.0

        elif strategy == "limiting":
            return 1.0

        elif strategy == "saturation":
            return 0.0

        else:
            return 0.0

    # =====================================
    # additive
    # =====================================

    if strategy == "additive":

        return sum(values)

    # =====================================
    # multiplicative
    # =====================================

    if strategy == "multiplicative":

        result = 1.0

        for value in values:

            result *= (
                1.0 + value
            )

        return result

    # =====================================
    # limiting
    # =====================================

    if strategy == "limiting":

        return min(values)

    # =====================================
    # saturation
    # =====================================

    if strategy == "saturation":

        total = sum(values)

        return (
            total /
            (
                1.0 + total
            )
        )

    return sum(values)
