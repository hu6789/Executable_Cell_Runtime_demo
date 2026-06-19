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
    apply final runtime scaling

    responsibilities:
        - apply resource share scaling
        - apply execution efficiency
        - apply physiological limitation
        - apply late-stage runtime modifiers

    DOES NOT:
        - perform ecological shaping
        - compute graph contributions
        - evaluate behavior gate
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

    ecology_bias = (
        competition_context.get(
            "ecology_bias",
            {}
        )
    )

    hir_constraints = (
        competition_context.get(
            "hir_constraints",
            {}
        )
    )

    # =====================================
    # initialize scaling
    # =====================================

    scaled_drive = raw_drive

    scaling_breakdown = {}

    # =====================================
    # competition scaling
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
    # execution efficiency
    # =====================================

    execution_efficiency = (
        hir_constraints.get(
            "execution_efficiency",
            1.0
        )
    )

    scaled_drive *= (
        execution_efficiency
    )

    scaling_breakdown[
        "execution_efficiency"
    ] = execution_efficiency

    # =====================================
    # secretion limitation
    # =====================================

    secretion_limit = (
        hir_constraints.get(
            "secretion_limit",
            1.0
        )
    )

    scaled_drive *= secretion_limit

    scaling_breakdown[
        "secretion_limit"
    ] = secretion_limit

    # =====================================
    # mobility limitation
    # =====================================

    mobility_limit = (
        hir_constraints.get(
            "mobility_limit",
            1.0
        )
    )

    scaled_drive *= mobility_limit

    scaling_breakdown[
        "mobility_limit"
    ] = mobility_limit

    # =====================================
    # global suppression
    # =====================================

    suppression = hir_constraints.get(
        "global_behavior_suppression",
        0.0
    )

    suppression_scale = (
        1.0 - suppression
    )

    scaled_drive *= suppression_scale

    scaling_breakdown[
        "suppression_scale"
    ] = suppression_scale

    # =====================================
    # ecology stabilization
    # =====================================

    stabilization_scale = (
        ecology_bias.get(
            "survival_bias",
            1.0
        )
    )

    scaled_drive *= stabilization_scale

    scaling_breakdown[
        "stabilization_scale"
    ] = stabilization_scale

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

        "skeleton_result":
            skeleton_result
    }

# =========================================
# Behavior Competition Weight
# =========================================

def extract_behavior_competition_weight(
    behavior_name,
    behavior_competition
):

    """
    extract competition weight
    for current behavior

    competition is computed
    during intra-category competition

    each behavior should consume
    its own competition result

    instead of using a global average
    """

    for category_result in (
        behavior_competition.values()
    ):

        if behavior_name not in category_result:

            continue

        behavior_result = (
            category_result[
                behavior_name
            ]
        )

        return behavior_result.get(
            "competition_weight",
            1.0
        )

    return 1.0
