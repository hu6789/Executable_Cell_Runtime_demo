# scanmaster/event_standardizer.py

import uuid


# =========================================
# standardize biological events
# =========================================

def standardize_events(
    events
):

    standardized = []

    for event in events:

        standard = standardize_single_event(
            event
        )

        if standard is not None:

            standardized.append(
                standard
            )

    return standardized


# =========================================
# standardize single event
# =========================================

def standardize_single_event(
    event
):

    return {

        "event_id": str(
            uuid.uuid4()
        ),

        "event_type": event.get(
            "event_type"
        ),

        "interaction_mode": event.get(
            "interaction_mode"
        ),

        "source_id": event.get(
            "source_id"
        ),

        "target_id": event.get(
            "target_id"
        ),

        "source_type": event.get(
            "source_type"
        ),

        "target_type": event.get(
            "target_type"
        ),

        "payload": event.get(
            "payload",
            {}
        ),

        "tick": event.get(
            "tick"
        )
    }
