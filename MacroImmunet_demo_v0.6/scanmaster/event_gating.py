# scanmaster/event_gating.py


# =========================================
# biological event gating
# =========================================

def gate_events(
    interaction_events
):

    """
    interaction semantics
    →
    biological events
    """

    gated = []

    for event in interaction_events:

        biological_event = gate_single_event(
            event
        )

        if biological_event is not None:

            gated.append(
                biological_event
            )

    return gated


# =========================================
# gate single interaction
# =========================================

def gate_single_event(
    event
):

    interaction_mode = event.get(
        "interaction_mode"
    )

    # =====================================
    # contact
    # =====================================

    if interaction_mode == "contact":

        return build_contact_event(
            event
        )

    elif interaction_mode == "field":

        return build_field_event(
            event
        )

    return None


# =========================================
# contact biological event
# =========================================

def build_contact_event(
    interaction
):

    return {

        "event_type": "contact_event",

        "interaction_mode": "contact",

        "source_id": interaction.get(
            "source_id"
        ),

        "target_id": interaction.get(
            "target_id"
        ),

        "source_type": interaction.get(
            "source_type"
        ),

        "target_type": interaction.get(
            "target_type"
        ),

        "payload": {

            "distance": interaction.get(
                "distance"
            ),
        "tick":
            interaction.get(
                "tick"
            )
        }
    }
    
# =========================================
# field exposure event
# =========================================

def build_field_event(
    interaction
):

    return {

        "event_type":
            "field_exposure_event",

        "interaction_mode":
            "field",

        "target_id":
            interaction.get(
                "target_id"
            ),

        "target_type":
            interaction.get(
                "target_type"
            ),

        "payload": {

            "field_type":
                interaction.get(
                    "field_type"
                ),

            "field_strength":
                interaction.get(
                    "field_strength",
                    0.0
                ),
        "tick":
            interaction.get(
                "tick"
            )
        }
    }
    
