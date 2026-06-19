# cellmaster/internalnet/hir/physiological_constraint.py


# =========================================
# Physiological Constraint Generation
# =========================================

def compute_physiological_constraints(
    adjusted_context,
    fate_progression,
    runtime_entity
):

    """
    generate physiological constraints

    responsibilities:
        - generate resource limitation
        - generate mobility suppression
        - generate secretion suppression
        - generate proliferation suppression
        - generate repair prioritization
        - generate unified constraint context

    DOES NOT:
        - directly suppress behaviors
        - directly modify runtime state
        - directly execute fate
    """

    runtime_state = adjusted_context.get(
        "runtime_state",
        {}
    )

    interpretation_labels = adjusted_context.get(
        "interpretation_labels",
        []
    )

    progression_context = fate_progression.get(
        "progression_context",
        {}
    )

    resource_profile = build_resource_profile(
        runtime_state
    )

    damage_profile = build_damage_profile(
        runtime_state,
        interpretation_labels
    )

    fate_profile = build_fate_profile(
        progression_context
    )
    constraints = {

        "resource_profile":
            resource_profile,

        "damage_profile":
            damage_profile,

        "fate_profile":
            fate_profile,

        "translation_limit":
            compute_translation_limit(
                runtime_state,
                interpretation_labels
            ),

        "mobility_limit":
            compute_mobility_limit(
                runtime_state,
                interpretation_labels
            ),

        "secretion_limit":
            compute_secretion_limit(
                runtime_state,
                interpretation_labels
            ),

        "proliferation_limit":
            compute_proliferation_limit(
                runtime_state,
                interpretation_labels
            ),

        "repair_priority":
            compute_repair_priority(
                runtime_state,
                interpretation_labels,
                progression_context
            )
    }
    # =====================================
    # generate global suppression
    # =====================================

    constraints[
        "global_behavior_suppression"
    ] = evaluate_global_suppression(
        progression_context
    )

    return constraints


# =========================================
# Translation Limitation
# =========================================

def compute_translation_limit(
    runtime_state,
    interpretation_labels
):

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    if ATP <= 0.0:

        return 0.0

    # =====================================
    # metabolic suppression
    # =====================================

    if "metabolic_stress" in interpretation_labels:

        return 0.4

    return 1.0


# =========================================
# Mobility Limitation
# =========================================

def compute_mobility_limit(
    runtime_state,
    interpretation_labels
):

    membrane_integrity = runtime_state.get(
        "membrane_integrity",
        1.0
    )

    if membrane_integrity < 0.3:

        return 0.2

    if "oxidative_stress" in interpretation_labels:

        return 0.5

    return 1.0


# =========================================
# Secretion Limitation
# =========================================

def compute_secretion_limit(
    runtime_state,
    interpretation_labels
):

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    if ATP < 1.0:

        return 0.2

    if "survival_collapse" in interpretation_labels:

        return 0.1

    return 1.0


# =========================================
# Proliferation Limitation
# =========================================

def compute_proliferation_limit(
    runtime_state,
    interpretation_labels
):

    if "integrity_collapse" in interpretation_labels:

        return 0.0

    if "metabolic_stress" in interpretation_labels:

        return 0.3

    return 1.0


# =========================================
# Repair Priority
# =========================================

def compute_repair_priority(
    runtime_state,
    interpretation_labels,
    progression_context
):

    repair_priority = 0.0

    # =====================================
    # integrity repair
    # =====================================

    membrane_integrity = runtime_state.get(
        "membrane_integrity",
        1.0
    )

    if membrane_integrity < 0.7:

        repair_priority += 0.5

    # =====================================
    # oxidative repair
    # =====================================

    if "oxidative_stress" in interpretation_labels:

        repair_priority += 0.3

    # =====================================
    # fate-stage suppression
    # =====================================

    if progression_context.get(
        "progressing",
        False
    ):

        repair_priority *= 0.5

    return min(
        repair_priority,
        1.0
    )


# =========================================
# Global Suppression
# =========================================

def evaluate_global_suppression(
    progression_context
):

    fate = progression_context.get(
        "fate",
        "stable"
    )

    progression = progression_context.get(
        "progression",
        0.0
    )

    # =====================================
    # apoptosis suppression
    # =====================================

    if fate == "apoptosis":

        return min(
            progression,
            1.0
        )

    # =====================================
    # necrosis suppression
    # =====================================

    if fate == "necrosis":

        return min(
            progression * 1.5,
            1.0
        )

    return 0.0
# =========================================
# Resource Profile
# =========================================
def build_resource_profile(
    runtime_state
):

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    if ATP < 2.0:

        state = "depleted"

    elif ATP < 20.0:

        state = "limited"

    else:

        state = "normal"

    return {

        "ATP":
            ATP,

        "resource_state":
            state
    }
# =========================================
# Damage Profile
# =========================================
def build_damage_profile(
    runtime_state,
    interpretation_labels
):

    return {

        "ROS":
            runtime_state.get(
                "ROS",
                0.0
            ),

        "membrane_integrity":
            runtime_state.get(
                "membrane_integrity",
                1.0
            ),

        "damage_labels":
            interpretation_labels
    }
# =========================================
# Fate Profile
# =========================================
def build_fate_profile(
    progression_context
):

    return {

        "fate":
            progression_context.get(
                "fate",
                "stable"
            ),

        "progression":
            progression_context.get(
                "progression",
                0.0
            ),

        "progressing":
            progression_context.get(
                "progressing",
                False
            )
    }
