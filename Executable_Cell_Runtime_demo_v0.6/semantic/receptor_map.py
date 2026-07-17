# semantic/receptor_map.py

SIGNAL_RECEPTOR_MAP = {

    # cytokine receptors

    "IL2R_activation":
        "IL2R",

    "CXCR3_activation":
        "CXCR3",

    # antigen receptor

    "TCR_activation":
        "TCR",

    # interaction receptors

    "binding_detected":
        "binding_receptor",

    "membrane_contact":
        "contact_sensor",

    "persistent_interaction":
        "adhesion_sensor",

    "directed_threat":
        "damage_sensor"

}
