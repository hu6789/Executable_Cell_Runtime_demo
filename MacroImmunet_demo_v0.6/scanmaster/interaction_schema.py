# scanmaster/interaction_schema.py


# =========================================
# interaction schema library
# =========================================

INTERACTION_SCHEMAS = {

    # =====================================
    # cell-cell contact
    # =====================================

    "cell_cell_contact": {

        "interaction_mode": "contact",

        "allowed_events": [

            "contact_event"
        ]
    },

    # =====================================
    # persistent contact
    # =====================================

    "persistent_contact": {

        "interaction_mode": "persistent",

        "allowed_events": [

            "immune_synapse_event"
        ]
    },

    # =====================================
    # field exposure
    # =====================================

    "field_exposure": {

        "interaction_mode": "field",

        "allowed_events": [

            "field_exposure_event"
        ]
    }
}
