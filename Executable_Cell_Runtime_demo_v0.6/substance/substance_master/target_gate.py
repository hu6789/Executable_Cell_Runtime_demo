# substance/substance_master/target_gate.py


def evaluate_target_gate(

    interaction_context,

    interaction_rule
):

    """
    Select candidate targets.

    Does NOT:
        - compute strength
        - apply effects

    Only chooses
    potential targets.
    """

    target_type = (

        interaction_rule.get(
            "target_type"
        )
    )
    
    source_id = interaction_context.get("source_id")

    # ==========================
    # cell targets
    # ==========================

    if target_type == "cell":

        source_id = interaction_context.get("source_id")

        return [
            cell.id
            for cell in interaction_context.get(
                "candidate_cells",
               []
           )
        ]

    # ==========================
    # substance targets
    # ==========================

    if target_type == "substance":

        return list(

            interaction_context.get(
                "candidate_substances",
                []
            )
        )

    return []
