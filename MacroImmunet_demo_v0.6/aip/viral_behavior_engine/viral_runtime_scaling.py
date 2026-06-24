# aip/viral_behavior_engine/viral_runtime_scaling.py


# =========================================
# Runtime Scaling
# =========================================

def apply_runtime_scaling(
    behavior_name,
    skeleton_result,
    competition_context,
    viral_context=None
):

    """
    apply final runtime scaling

    responsibilities:

        - consume competition result

        - consume execution profile

        - generate final scaled drive

    DOES NOT:

        - evaluate gates

        - perform category allocation

        - perform competition

        - compute graph contribution

        - execute behavior
    """

    raw_drive = skeleton_result.get(
        "raw_drive",
        0.0
    )

    scaled_drive = raw_drive

    scaling_breakdown = {}

    # =====================================
    # competition scaling
    # =====================================

    behavior_competition = (
        competition_context.get(
            "behavior_competition",
            {}
        )
    )

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
    # execution profile scaling
    # =====================================

    execution_profile = (
        (viral_context or {}).get(
            "execution_profile",
            {}
        )
    )

    execution_scale = (
        execution_profile.get(
            "execution_scale",
            1.0
        )
    )

    scaled_drive *= execution_scale

    scaling_breakdown[
        "execution_scale"
    ] = execution_scale

    # =====================================
    # clamp
    # =====================================

    scaled_drive = max(
        0.0,
        scaled_drive
    )

    return {

        "scaled_drive":
            scaled_drive,

        "raw_drive":
            raw_drive,

        "scaling_breakdown":
            scaling_breakdown,

        "competition_weight":
            competition_scale,

        "execution_scale":
            execution_scale,

        "skeleton_result":
            skeleton_result
    }


# =========================================
# Competition Weight Lookup
# =========================================

def extract_behavior_competition_weight(
    behavior_name,
    behavior_competition
):

    """
    find behavior-specific
    competition weight
    """

    for category_result in (
        behavior_competition.values()
    ):

        behavior_result = (
            category_result.get(
                behavior_name
            )
        )

        if not behavior_result:
            continue

        return behavior_result.get(
            "competition_weight",
            1.0
        )

    return 1.0
