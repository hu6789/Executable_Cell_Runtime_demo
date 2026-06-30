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

    raw_drive = skeleton_result.get("raw_drive", 0.0)

    scaled_drive = raw_drive
    scaling_breakdown = {}

    # =====================================
    # competition scaling
    # =====================================

    behavior_competition = (
        competition_context.get("competition", {})
    )

    competition_scale = extract_behavior_competition_weight(
        behavior_name,
        behavior_competition
    )

    scaled_drive *= competition_scale
    scaling_breakdown["competition_scale"] = competition_scale

    # =====================================
    # execution profile scaling
    # =====================================

    execution_profile = (viral_context or {}).get("execution_profile", {})

    execution_scale = execution_profile.get("execution_scale", 1.0)

    scaled_drive *= execution_scale
    scaling_breakdown["execution_scale"] = execution_scale

    # =====================================
    # 🧬 VIRAL NONLINEARITY LAYER (NEW)
    # =====================================

    cycle_state = (viral_context or {}).get("cycle_state", "entry")
    infection_load = (viral_context or {}).get("infection_load", 0.0)
    resource_pressure = (viral_context or {}).get("resource_projection", {})

    ribosome = resource_pressure.get("ribosome", 1.0)

    # 1. entry burst amplification
    if cycle_state == "entry":
        scaled_drive *= 1.15

    # 2. replication runaway
    if cycle_state == "replication":
        scaled_drive *= (1.0 + infection_load)

    # 3. ribosome hijack nonlinear boost
    # (key viral signature)
    scaled_drive *= (1.0 + (1.0 - ribosome) * 0.8)

    # 4. saturation curve (prevents explosion but keeps nonlinearity)
    scaled_drive = scaled_drive / (1.0 + scaled_drive)

    scaling_breakdown["viral_nonlinearity"] = {
        "cycle_state": cycle_state,
        "infection_load": infection_load,
        "ribosome": ribosome
    }

    # =====================================
    # clamp
    # =====================================

    scaled_drive = max(0.0, scaled_drive)

    return {
        "scaled_drive": scaled_drive,
        "raw_drive": raw_drive,
        "scaling_breakdown": scaling_breakdown,
        "competition_weight": competition_scale,
        "execution_scale": execution_scale,
        "skeleton_result": skeleton_result
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
