# substance/substance_master/effect_projection.py


def project_effect(

    interaction_rule,

    strength_result
):

    """
    Convert strength
    into biological effect.

    Does NOT:
        generate requests

    Returns:
        projected effect
    """

    return {

        "target":

            strength_result.get(
                "target"
            ),

        "effect_type":

            interaction_rule.get(
                "effect_type"
            ),

        "amount":

            strength_result.get(
                "strength",
                0.0
            )
    }
