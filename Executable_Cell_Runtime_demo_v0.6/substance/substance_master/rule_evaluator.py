# substance/substance_master/rule_evaluator.py


def evaluate_interaction_rules(

    interaction_context,

    template
):

    """
    Evaluate available interaction rules.

    Passive substances:
        no active interaction.

    Active substances:
        expose declared rules.

    Does NOT:
        - validate targets
        - compute strengths
        - generate effects
    """

    interaction_mode = getattr(
        template,
        "interaction_mode",
        "passive"
    )

    if interaction_mode != "active":
        return []

    return list(
        getattr(
            template,
            "interaction_rules",
            []
        )
    )

    if interaction_mode != "active":

        return []

    return list(

        template.get(
            "interaction_rules",
            []
        )
    )
