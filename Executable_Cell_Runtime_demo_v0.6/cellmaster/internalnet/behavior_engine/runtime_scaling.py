# cellmaster/internalnet/behavior_engine/runtime_scaling.py

# =========================================
# Runtime Scaling
# =========================================

def apply_runtime_scaling(
    behavior_name,
    skeleton_result,
    competition_context
):

    """
    Apply final runtime scaling.

    responsibilities
    ----------------
    - apply competition result
    - apply HIR behavior budget
    - apply global physiological suppression
    - apply ecology stabilization
    - generate final runtime drive

    DOES NOT
    --------
    - evaluate behavior legality
    - allocate behavior budget
    - compute behavior competition
    """

    raw_drive = skeleton_result.get(
        "raw_drive",
        0.0
    )

    behavior_competition = (
        competition_context.get(
            "behavior_competition",
            {}
        )
    )

    behavior_budget = (
        competition_context.get(
            "behavior_budget",
            {}
        )
    )

    physiological_constraints = (
        competition_context.get(
            "physiological_constraints",
            {}
        )
    )

    ecology_bias = (
        competition_context.get(
            "ecology_bias",
            {}
        )
    )

    scaled_drive = raw_drive

    scaling_breakdown = {}

    # =====================================
    # Competition
    # =====================================

    competition_scale = (
        extract_behavior_competition_weight(
            behavior_name,
            behavior_competition
        )
    )

    scaled_drive *= competition_scale

    scaling_breakdown[
        "competition_scale"
    ] = competition_scale

    # =====================================
    # Behavior Budget
    # =====================================

    budget = behavior_budget.get(
        behavior_name,
        {}
    )

    execution_limit = budget.get(
        "execution_limit",
        1.0
    )

    scaled_drive *= execution_limit

    scaling_breakdown[
        "execution_limit"
    ] = execution_limit

    # =====================================
    # Global Physiological Suppression
    # =====================================

    suppression = physiological_constraints.get(
        "global_behavior_suppression",
        0.0
    )

    suppression_scale = max(
        0.0,
        1.0 - suppression
    )

    scaled_drive *= suppression_scale

    scaling_breakdown[
        "suppression_scale"
    ] = suppression_scale

    # =====================================
    # Ecology Stabilization
    # =====================================

    stabilization_scale = ecology_bias.get(
        "survival_bias",
        1.0
    )

    scaled_drive *= stabilization_scale

    scaling_breakdown[
        "stabilization_scale"
    ] = stabilization_scale

    # =====================================
    # Clamp
    # =====================================

    scaled_drive = max(
        0.0,
        scaled_drive
    )
    
    return {

        "raw_drive":
            raw_drive,

        "scaled_drive":
            scaled_drive,

        "scaling_breakdown":
            scaling_breakdown,

        "execution_budget":
            budget,

        "skeleton_result":
            skeleton_result
    }


# =========================================
# Competition Weight
# =========================================

def extract_behavior_competition_weight(
    behavior_name,
    behavior_competition
):
    """
    Extract competition weight
    for current behavior.
    """

    for category_result in (
        behavior_competition.values()
    ):

        behavior_result = (
            category_result.get(
                behavior_name
            )
        )

        if behavior_result is None:

            continue

        return behavior_result.get(
            "competition_weight",
            1.0
        )

    return 1.0
