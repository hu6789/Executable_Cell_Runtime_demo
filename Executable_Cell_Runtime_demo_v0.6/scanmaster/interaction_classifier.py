# scanmaster/interaction_classifier.py


# =========================================
# classify interaction modes
# =========================================

def classify_interactions(
    topology_events
):

    """
    topology relation
    →
    interaction mode
    """

    classified = []

    for event in topology_events:

        interaction = classify_single_event(
            event
        )

        if interaction is not None:

            classified.append(
                interaction
            )

    return classified


# =========================================
# classify single event
# =========================================

def classify_single_event(
    event
):

    topology_type = event.get(
        "topology_type"
    )

    # =====================================
    # cell-cell contact
    # =====================================

    if topology_type == "cell_cell_contact":

        classified = dict(event)

        classified[
            "interaction_mode"
        ] = "contact"
    elif topology_type == "field_exposure":

        classified = dict(event)

        classified[
            "interaction_mode"
        ] = "field"

        return classified

    # =====================================
    # unknown
    # =====================================

    return None
