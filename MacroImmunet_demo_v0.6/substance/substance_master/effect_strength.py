# substance/substance_master/effect_strength.py


def compute_effect_strength(

    interaction_context,

    interaction_rule,

    target
):

    """
    Compute interaction strength.

    First version:

        amount
        ×
        base_strength

    Future:

        amount
        × affinity
        × distance
        × resistance
    """

    amount = interaction_context.get(
        "amount",
        0.0
    )

    base_strength = interaction_rule.get(
        "base_strength",
        1.0
    )

    strength = (
        amount
        *
        base_strength
    )

    return {

        "target": target,

        "strength": strength
    }
