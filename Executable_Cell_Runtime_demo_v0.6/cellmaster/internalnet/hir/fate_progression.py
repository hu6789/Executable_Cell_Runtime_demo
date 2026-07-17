# cellmaster/internalnet/hir/fate_progression.py

"""
HIR Fate Progression

Position

    downstream of
    physiological constraint

Purpose

    evaluate fate decision

    update fate progression

    evaluate completion

Produces

    fate runtime context

Does NOT

    execute death

    remove cell

    modify runtime state
"""

# =========================================
# Fate Progression
# =========================================

def compute_fate_progression(
    adjusted_context,
    runtime_entity
):
    """
    evaluate runtime fate progression

    responsibilities

        - evaluate fate decision

        - update progression

        - evaluate completion

        - generate fate runtime

    DOES NOT

        - execute fate

        - remove entity

        - modify runtime state
    """

    runtime_state = adjusted_context.get(
        "runtime_state",
        {}
    )

    current_fate = runtime_state.get(
        "fate_state",
        "stable"
    )

    next_fate = evaluate_fate_decision(
        adjusted_context,
        current_fate
    )

    progression_context = update_fate_progress(
        next_fate,
        runtime_state,
        adjusted_context
    )

    completion_context = evaluate_completion(
        progression_context
    )

    return {

        "current_fate":
            current_fate,

        "next_fate":
            next_fate,

        "progression_context":
            progression_context,

        "completion_context":
            completion_context
    }


# =========================================
# Fate Decision
# =========================================

def evaluate_fate_decision(
    adjusted_context,
    current_fate
):
    """
    determine next fate

    future versions may include

        lineage

        viral modulation

        differentiation

        aging
    """

    survival = adjusted_context.get(
        "survival_summary",
        {}
    )

    integrity = adjusted_context.get(
        "integrity_summary",
        {}
    )

    interpretation = adjusted_context.get(
        "interpretation_labels",
        []
    )

    if current_fate != "stable":

        return current_fate

    if integrity.get(
        "critical_integrity",
        False
    ):

        return "necrosis"

    if not survival.get(
        "survival_possible",
        True
    ):

        return "apoptosis"

    return "stable"


# =========================================
# Progress Update
# =========================================

def update_fate_progress(
    fate,
    runtime_state,
    adjusted_context
):
    """
    update fate progression
    """

    if fate == "stable":

        return {

            "fate":
                "stable",

            "progression":
                0.0,

            "progress_rate":
                0.0,

            "progressing":
                False
        }

    previous = runtime_state.get(
        "fate_progression",
        0.0
    )

    progress_rate = calculate_progress_rate(
        adjusted_context,
        fate
    )

    progression = min(
        previous + progress_rate,
        1.0
    )

    return {

        "fate":
            fate,

        "progression":
            progression,

        "progress_rate":
            progress_rate,

        "progressing":
            True
    }


# =========================================
# Progress Rate
# =========================================

def calculate_progress_rate(
    adjusted_context,
    fate
):
    """
    calculate progression speed

    future versions

        ATP

        ROS

        viral payload

        lineage

        immune intervention
    """

    survival = adjusted_context.get(
        "survival_summary",
        {}
    )

    survival_score = survival.get(
        "survival_score",
        1.0
    )

    integrity = adjusted_context.get(
        "integrity_summary",
        {}
    )

    integrity_score = integrity.get(
        "integrity_score",
        1.0
    )

    base_rate = 0.25

    if fate == "necrosis":

        base_rate = 0.40

    elif fate == "apoptosis":

        base_rate = 0.25

    # poorer physiology
    # accelerates progression

    modifier = max(

        0.5,

        1.5 - (
            survival_score +
            integrity_score
        ) / 2.0
    )

    return min(
        base_rate * modifier,
        1.0
    )


# =========================================
# Completion
# =========================================

def evaluate_completion(
    progression_context
):
    """
    evaluate whether
    fate reaches completion
    """

    fate = progression_context.get(
        "fate",
        "stable"
    )

    progression = progression_context.get(
        "progression",
        0.0
    )

    threshold = get_completion_threshold(
        fate
    )

    completed = (
        progression >= threshold
    )

    return {

        "completed":
            completed,

        "completion_ready":
            completed,

        "completion_threshold":
            threshold
    }


# =========================================
# Completion Threshold
# =========================================

def get_completion_threshold(
    fate
):
    """
    configurable completion threshold

    future versions may load
    from schema
    """

    thresholds = {

        "stable":
            1.0,

        "apoptosis":
            1.0,

        "necrosis":
            0.8
    }

    return thresholds.get(
        fate,
        1.0
    )
