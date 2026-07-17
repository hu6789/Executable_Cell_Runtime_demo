# aip/viral_behavior_engine/viral_behavior_gate.py

# =========================================
# Viral Behavior Gate
# =========================================

def evaluate_viral_behavior_gate(
    behavior_def,
    skeleton_result,
    viral_cycle_state
):

    """
    final viral behavior gate

    responsibilities:

        - minimum activation threshold

        - lifecycle phase restriction

        - runtime enable check

    DOES NOT:

        - evaluate physiology

        - evaluate resources

        - evaluate competition

        - evaluate deception

    all resource effects should already
    be reflected by:

        category allocation

        competition

        runtime scaling
    """

    # =====================================
    # runtime enabled
    # =====================================

    if not behavior_def.get(
        "runtime_enabled",
        True
    ):
        return False

    # =====================================
    # gate config
    # =====================================

    gate = behavior_def.get(
        "viral_gate",
        {}
    )

    # =====================================
    # minimum drive
    # =====================================

    raw_drive = skeleton_result.get(
        "raw_drive",
        0.0
    )

    minimum_drive = gate.get(
        "minimum_drive",
        0.0
    )

    if raw_drive < minimum_drive:
        return False

    # =====================================
    # required phase
    # =====================================

    required_phase = gate.get(
        "required_phase"
    )

    if (
        required_phase
        and
        required_phase != viral_cycle_state
    ):
        return False

    # =====================================
    # pass
    # =====================================

    return True
