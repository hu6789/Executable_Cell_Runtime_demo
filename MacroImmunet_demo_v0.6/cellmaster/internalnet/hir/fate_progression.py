# cellmaster/internalnet/hir/fate_progression.py


# =========================================
# Fate Progression Engine
# =========================================

def compute_fate_progression(
    adjusted_context,
    runtime_entity
):

    """
    compute progressive fate execution

    responsibilities:
        - evaluate fate initiation
        - evaluate fate progression
        - evaluate fate completion
        - generate fate runtime context

    DOES NOT:
        - remove cell
        - directly execute death
        - directly modify runtime state
    """

    interpretation_labels = adjusted_context.get(
        "interpretation_labels",
        []
    )
    integrity_summary = adjusted_context.get(
        "integrity_summary",
        {}
    )
    survival_summary = adjusted_context.get(
        "survival_summary",
        {}
    )

    runtime_state = adjusted_context.get(
        "runtime_state",
        {}
    )

    # =====================================
    # current fate state
    # =====================================

    current_fate = runtime_state.get(
        "fate_state",
        "stable"
    )

    # =====================================
    # evaluate initiation
    # =====================================

    initiated_fate = evaluate_fate_initiation(

        current_fate,
        survival_summary,
        integrity_summary
    )

    # =====================================
    # evaluate progression
    # =====================================

    progression_context = (
        evaluate_fate_progression(

            initiated_fate,
            runtime_state
        )
    )

    # =====================================
    # evaluate completion
    # =====================================

    completion_context = (
        evaluate_fate_completion(

            progression_context
        )
    )

    return {

        "current_fate":
            current_fate,

        "initiated_fate":
            initiated_fate,

        "progression_context":
            progression_context,

        "completion_context":
            completion_context
    }


# =========================================
# Fate Initiation
# =========================================

def evaluate_fate_initiation(
    current_fate,
    survival_summary,
    integrity_summary
):

    survival_possible = (
        survival_summary.get(
            "survival_possible",
            True
        )
    )

    critical_integrity = (
        integrity_summary.get(
            "critical_integrity",
            False
        )
    )
    if not survival_possible:

        return "apoptosis"

    if critical_integrity:

        return "necrosis"

    return "stable"


# =========================================
# Fate Progression
# =========================================

def evaluate_fate_progression(
    initiated_fate,
    runtime_state
):

    progression_value = runtime_state.get(
        "fate_progression",
        0.0
    )

    # =====================================
    # stable state
    # =====================================

    if initiated_fate == "stable":

        return {

            "fate":
                "stable",

            "progression":
                0.0,

            "progressing":
                False
        }

    # =====================================
    # progressing fate
    # =====================================

    progression_value += 0.25

    return {

        "fate":
            initiated_fate,

        "progression":
            progression_value,

        "progressing":
            True
    }


# =========================================
# Fate Completion
# =========================================

def evaluate_fate_completion(
    progression_context
):

    progression = progression_context.get(
        "progression",
        0.0
    )

    completed = (
        progression >= 1.0
    )

    return {

        "completed":
            completed,

        "completion_ready":
            completed
    }
