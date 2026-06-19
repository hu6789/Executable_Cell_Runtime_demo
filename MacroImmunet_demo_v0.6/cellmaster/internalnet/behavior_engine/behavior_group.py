# cellmaster/internalnet/behavior_engine/behavior_group.py

"""
Semantic Grouping Layer

purpose:

    contribution category
    is defined by graph edge semantics

grouping only performs:

    activation
    suppression
    amplification
    resource
    damage
    stabilization
    destabilization

no numerical computation
is performed here

this stage only preserves
functional meaning
for downstream aggregation
"""
# =========================================
# Behavior Contribution Grouping
# =========================================

def group_behavior_contributions(
    transformed_contributions
):

    """
    group contributions
    by predefined semantic category

    responsibilities:
        - semantic grouping
        - preserve category separation
        - prepare category aggregation

    DOES NOT:
        - aggregate category values
        - compute behavior drive
        - evaluate behavior gate
    """

    grouped = {

        "activation": [],
        "suppression": [],
        "amplification": [],
        "resource": [],
        "damage": [],
        "stabilization": [],
        "destabilization": []
    }

    for contribution in (
        transformed_contributions
    ):

        category = contribution.get(
            "category",
            "activation"
        )

        if category not in grouped:

            grouped[
                category
            ] = []

        grouped[
            category
        ].append(
            contribution
        )

    return grouped
