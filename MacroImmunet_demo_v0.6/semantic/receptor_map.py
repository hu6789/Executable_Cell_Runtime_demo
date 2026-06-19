# semantic/receptor_map.py


# =========================================
# internal signal
# →
# receptor mapping
# =========================================

SIGNAL_RECEPTOR_MAP = {

    # -------------------------------------
    # cytokine receptors
    # -------------------------------------

    "IFNGR_activation":
        "IFNGR",

    "IL2R_activation":
        "IL2R",

    "TNFR_activation":
        "TNFR",

    # -------------------------------------
    # interaction receptors
    # -------------------------------------

    "binding_detected":
        "binding_receptor",

    "membrane_contact":
        "contact_sensor",

    "persistent_interaction":
        "adhesion_sensor",

    "directed_threat":
        "damage_sensor"
}
