# semantic/cell_to_world_map.py


# =========================================
# cell internal semantic
# →
# world semantic
# =========================================

CELL_TO_WORLD_SIGNAL_MAP = {

    # -------------------------------------
    # cytokine release
    # -------------------------------------

    "IFN_release":
        "IFN",

    "IL2_release":
        "IL2",

    "TNF_release":
        "TNF_alpha",

    # -------------------------------------
    # directed attack
    # -------------------------------------

    "perforin_release":
        "perforin"
}
