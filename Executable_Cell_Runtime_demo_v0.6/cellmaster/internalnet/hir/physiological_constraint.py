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

        convert interpreted physiology
        into executable behavior limits

    DOES NOT:

        directly modify runtime state
        directly suppress behaviors
        execute fate
    """

    physiology_summary = adjusted_context.get(
        "physiology_summary",
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
        physiology_summary
    )

    damage_profile = build_damage_profile(
        physiology_summary,
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

        "metabolism_limit":
            compute_metabolism_limit(
                physiology_summary
            ),

        "translation_limit":
            compute_translation_limit(
                physiology_summary,
                interpretation_labels
            ),

        "mobility_limit":
            compute_mobility_limit(
                physiology_summary
            ),

        "secretion_limit":
            compute_secretion_limit(
                physiology_summary
            ),

        "repair_priority":
            compute_repair_priority(
                physiology_summary,
                progression_context
            ),

        "proliferation_limit":
            compute_proliferation_limit(
                physiology_summary,
                progression_context
            )
    }

    constraints[
        "global_behavior_suppression"
    ] = evaluate_global_suppression(
        progression_context
    )

    return constraints


# =========================================
# Metabolism Limitation
# =========================================

def compute_metabolism_limit(
    physiology_summary
):

    resources = physiology_summary.get(
        "resources",
        {}
    )

    ATP = resources.get(
        "ATP",
        0.0
    )

    if ATP <= 0.0:

        return 0.0

    if ATP < 2.0:

        return 0.2

    if ATP < 10.0:

        return 0.5

    return 1.0


# =========================================
# Translation Limitation
# =========================================

def compute_translation_limit(
    physiology_summary,
    interpretation_labels
):

    resources = physiology_summary.get(
        "resources",
        {}
    )

    ATP = resources.get(
        "ATP",
        0.0
    )

    if ATP <= 0.0:

        return 0.0

    if ATP < 2.0:

        return 0.2

    if ATP < 10.0:

        return 0.5

    if "metabolic_stress" in interpretation_labels:

        return 0.6

    return 1.0


# =========================================
# Mobility Limitation
# =========================================

def compute_mobility_limit(
    physiology_summary
):

    damage = physiology_summary.get(
        "damage",
        {}
    )

    membrane_integrity = damage.get(
        "membrane_integrity",
        1.0
    )

    ROS = damage.get(
        "ROS",
        0.0
    )

    if membrane_integrity < 0.2:

        return 0.1

    if membrane_integrity < 0.5:

        return 0.4

    if ROS > 10:

        return 0.5

    return 1.0


# =========================================
# Secretion Limitation
# =========================================

def compute_secretion_limit(
    physiology_summary
):

    resources = physiology_summary.get(
        "resources",
        {}
    )

    survival_score = physiology_summary.get(
        "survival_score",
        1.0
    )

    ATP = resources.get(
        "ATP",
        0.0
    )

    if survival_score < 0.2:

        return 0.1

    if ATP < 1.0:

        return 0.2

    if ATP < 5.0:

        return 0.5

    return 1.0


# =========================================
# Repair Priority
# =========================================

def compute_repair_priority(
    physiology_summary,
    progression_context
):

    damage = physiology_summary.get(
        "damage",
        {}
    )

    membrane_integrity = damage.get(
        "membrane_integrity",
        1.0
    )

    ROS = damage.get(
        "ROS",
        0.0
    )

    priority = 0.0

    if membrane_integrity < 0.8:

        priority += 0.4

    if membrane_integrity < 0.5:

        priority += 0.3

    if ROS > 5.0:

        priority += 0.2

    if progression_context.get(
        "progressing",
        False
    ):

        priority *= 0.5

    return min(
        priority,
        1.0
    )


# =========================================
# Proliferation Limitation
# =========================================

def compute_proliferation_limit(
    physiology_summary,
    progression_context
):

    survival_score = physiology_summary.get(
        "survival_score",
        1.0
    )

    if survival_score < 0.2:

        return 0.0

    if survival_score < 0.5:

        return 0.3

    if progression_context.get(
        "progressing",
        False
    ):

        return 0.2

    return 1.0
    
# =========================================
# Global Behavior Suppression
# =========================================

def evaluate_global_suppression(
    progression_context
):

    """
    convert fate progression
    into a global behavior suppression factor
    """

    fate = progression_context.get(
        "fate",
        "stable"
    )

    progression = progression_context.get(
        "progression",
        0.0
    )

    if fate == "apoptosis":

        return min(
            progression,
            1.0
        )

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
    physiology_summary
):

    resources = physiology_summary.get(
        "resources",
        {}
    )

    ATP = resources.get(
        "ATP",
        0.0
    )

    if ATP < 2.0:

        state = "depleted"

    elif ATP < 10.0:

        state = "limited"

    else:

        state = "normal"

    return {

        "ATP":
            ATP,

        "resource_state":
            state,

        "resource_ratio":
            min(
                ATP / 20.0,
                1.0
            )
    }


# =========================================
# Damage Profile
# =========================================

def build_damage_profile(
    physiology_summary,
    interpretation_labels
):

    damage = physiology_summary.get(
        "damage",
        {}
    )

    return {

        "ROS":
            damage.get(
                "ROS",
                0.0
            ),

        "membrane_integrity":
            damage.get(
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


# =========================================
# Constraint Snapshot
# =========================================

def build_constraint_snapshot(
    constraints
):

    """
    lightweight runtime snapshot

    convenient for logging,
    debugging and visualization
    """

    return {

        "metabolism":
            constraints.get(
                "metabolism_limit",
                1.0
            ),

        "translation":
            constraints.get(
                "translation_limit",
                1.0
            ),

        "mobility":
            constraints.get(
                "mobility_limit",
                1.0
            ),

        "secretion":
            constraints.get(
                "secretion_limit",
                1.0
            ),

        "repair":
            constraints.get(
                "repair_priority",
                0.0
            ),

        "proliferation":
            constraints.get(
                "proliferation_limit",
                1.0
            ),

        "suppression":
            constraints.get(
                "global_behavior_suppression",
                0.0
            )
    }
