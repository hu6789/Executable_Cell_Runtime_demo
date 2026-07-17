# inputbuilder/signalmap_translation.py

from semantic.world_to_cell_map import (
    WORLD_TO_CELL_SIGNAL_MAP
)

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
         
# =========================================
# world semantic
# →
# intracellular semantic
# =========================================

def translate_perception(
    target_id,
    events
):

    """
    translate standardized biological events
    into intracellular semantic inputs
    """

    translated = []

    for event in events:

        translated_event = translate_event(
            event
        )

        if translated_event is not None:

            translated.append(
                translated_event
            )

    return translated


# =========================================
# translate single event
# =========================================

def translate_event(
    event
):
    print(event)
    event_type = event.get(
        "event_type"
    )

    payload = event.get(
        "payload",
        {}
    )

    # =====================================
    # field event
    # =====================================

    if event_type in (
        "field_event",
        "field_exposure_event"
    ):

        signal = payload.get(
            "field_type"
        )
        
        debug_print(
            "[Translator] signal =",
            signal
        )

        internal_signal = (

            WORLD_TO_CELL_SIGNAL_MAP.get(
                signal
            )
        )
        
        debug_print(
            "[Translator] internal =",
            internal_signal
        )
        
        if internal_signal is None:

            return None

        return {

            "input_type": "field_signal",

            "interaction_mode": "field",

            "source_id": event.get(
                "source_id"
            ),

            "payload": {

                "internal_signal":
                    internal_signal,

                "strength": payload.get(
                    "field_strength",

                    payload.get(
                        "strength",
                        0.0
                    )
                ),

                "distance": payload.get(
                    "distance",
                    0.0
                )
            }
        }

    # =====================================
    # contact event
    # =====================================

    elif event_type == "contact_event":

        return {

            "input_type": "contact_signal",

            "source_id": event.get(
                "source_id"
            ),

            "source_type": event.get(
                "source_type"
            ),

            "payload": {

                "internal_signal": (

                    WORLD_TO_CELL_SIGNAL_MAP.get(
                        "contact_event"
                    )
                ),

                "strength": 1.0,
  
                "distance": payload.get(
                    "distance",
                    0.0
                )
            }
        }
    # =====================================
    # binding event
    # =====================================

    elif event_type == "binding_event":

        return {

            "input_type": "binding_signal",

            "source_id": event.get(
                "source_id"
            ),

            "payload": {

                "internal_signal": (

                    WORLD_TO_CELL_SIGNAL_MAP.get(
                        "binding_event"
                    )
                ),

                "strength": payload.get(
                    "binding_strength",
                    1.0
                ),

                "distance": payload.get(
                    "distance",
                    0.0
                )
            }
        }
    print(
        "[Translator] unknown event:",
        event_type
    )
    return None
