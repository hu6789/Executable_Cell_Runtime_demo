# semantic/world_to_cell_map.py

WORLD_TO_CELL_SIGNAL_MAP = {

    # cytokines

    "IL2":
        "IL2R_activation",

    # chemokines

    "CXCL10":
        "CXCR3_activation",

    # antigen presentation

    "pMHC":
        "TCR_activation",

    # pathogen

    "influenza":
        "pathogen_signal_activation",

    # physical interaction

    "contact_event":
        "membrane_contact",

    "binding_event":
        "binding_detected",

    "persistent_event":
        "persistent_interaction",

    "directed_event":
        "directed_threat"

}
