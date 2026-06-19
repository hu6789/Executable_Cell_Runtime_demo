# scanmaster/event_lib.py


# =========================================
# biological event templates
# =========================================

EVENT_LIBRARY = {

    # =====================================
    # contact
    # =====================================

    "contact_event": {

        "event_type": "contact_event",

        "interaction_mode": "contact",

        "description": (

            "generic cell-cell contact"
        ),

        "default_payload": {

            "distance": None
        }
    },

    # =====================================
    # immune synapse
    # =====================================

    "immune_synapse_event": {

        "event_type": (

            "immune_synapse_event"
        ),

        "interaction_mode": (

            "persistent"
        ),

        "description": (

            "persistent immune contact"
        ),

        "default_payload": {

            "duration": 0
        }
    },

    # =====================================
    # field exposure
    # =====================================

    "field_exposure_event": {

        "event_type": (

            "field_exposure_event"
        ),

        "interaction_mode": "field",

        "description": (

            "cell exposed to field"
        ),

        "default_payload": {

            "field_type": None,

            "field_strength": 0.0
        }
    }
}
