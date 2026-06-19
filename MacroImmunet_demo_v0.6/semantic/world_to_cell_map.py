# semantic/world_to_cell_map.py


# =========================================
# world semantic
# →
# cell internal semantic
# =========================================

WORLD_TO_CELL_SIGNAL_MAP = {

    "IFN":
        "IFNGR_activation",

    "IFN_gamma":
        "IFNGR_activation",

    "IL2":
        "IL2R_activation",

    "TNF_alpha":
        "TNFR_activation",

    "contact_event":
        "membrane_contact",

    "binding_event":
        "binding_detected",

    "persistent_event":
        "persistent_interaction",

    "directed_event":
        "directed_threat"
}
