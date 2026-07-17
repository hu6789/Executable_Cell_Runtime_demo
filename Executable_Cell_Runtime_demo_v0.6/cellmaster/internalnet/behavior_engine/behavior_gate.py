# cellmaster/internalnet/behavior_engine/behavior_gate.py

"""
Behavior Gate

Position:

    after skeleton

Purpose:

    determine whether
    a computed behavior
    is allowed to activate

Design Principle:

    HIR evaluates physiology

    Behavior Gate
    consumes HIR conclusions

    Behavior Gate
    should not re-evaluate
    physiology whenever possible
"""
# =========================================
# Final Behavior Runtime Gate
# =========================================

def evaluate_behavior_gate(
    behavior_def,
    skeleton_result,
    competition_context
):

    """
    final behavior activation gate

    responsibilities:
        - evaluate behavior-level activation
        - evaluate resource requirement
        - evaluate fate restriction
        - evaluate shutdown conditions

    DIFFERENT FROM:
        edge gate:
            controls individual contribution participation

        behavior gate:
            controls final behavior activation
    """

    runtime_state = (
        competition_context.get(
            "runtime_state",
            {}
        )
    )

    fate_progression = (
        competition_context.get(
            "fate_progression",
            {}
        )
    )

    progression_context = (
        fate_progression.get(
            "progression_context",
            {}
        )
    )

    current_fate = (
        progression_context.get(
            "fate",
            "stable"
        )
    )

    state_labels = (
        competition_context.get(
            "state_labels",
            []
        )
    )

    raw_drive = skeleton_result.get(
        "raw_drive",
        0.0
    )

    gate = behavior_def.get(
        "behavior_gate",
        {}
    )

    # =====================================
    # minimum activation requirement
    # =====================================

    minimum_drive = gate.get(
        "minimum_drive",
        0.0
    )

    if raw_drive < minimum_drive:

        return False

    # =====================================
    # minimum ATP requirement
    # =====================================

    minimum_ATP = gate.get(
        "minimum_ATP",
        0.0
    )

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    if ATP < minimum_ATP:

        return False

    # =====================================
    # state label restriction
    # =====================================

    blocked_labels = gate.get(
        "blocked_labels",
        []
    )

    for label in blocked_labels:

        if label in state_labels:

            return False

    # =====================================
    # required labels
    # =====================================
    # labels originate from HIR
    # behavior gate consumes HIR conclusions
    # instead of re-evaluating physiology
    required_labels = gate.get(
        "required_labels",
        []
    )

    for label in required_labels:

        if label not in state_labels:

            return False

    # =====================================
    # terminal fate restriction
    # =====================================

    blocked_fates = gate.get(
        "blocked_fates",
        []
    )

    if current_fate in blocked_fates:

        return False

    # =====================================
    # behavior gate passed
    # =====================================
    return True
    
