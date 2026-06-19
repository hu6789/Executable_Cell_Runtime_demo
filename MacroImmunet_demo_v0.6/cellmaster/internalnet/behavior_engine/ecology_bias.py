# cellmaster/internalnet/behavior_engine/ecology_bias.py


# =========================================
# Behavior Ecology Bias
# =========================================

def apply_ecology_bias(
    behavior_context
):

    """
    apply high-level ecological shaping

    responsibilities:
        - apply fate-derived ecology bias
        - apply stress ecology shaping
        - apply activation ecology shaping
        - apply infection ecology shaping
        - generate behavior ecology tendency

    DOES NOT:
        - compute concrete behavior strength
        - evaluate graph contributions
        - execute behaviors
    """

    ecology_context = behavior_context.get(
        "ecology_context",
        {}
    )

    fate_progression = behavior_context.get(
        "fate_progression",
        {}
    )

    state_labels = behavior_context.get(
        "state_labels",
        []
    )

    # =====================================
    # initialize ecology bias
    # =====================================

    ecology_bias = {

        "survival_bias":
            1.0,

        "proliferation_bias":
            1.0,

        "secretion_bias":
            1.0,

        "mobility_bias":
            1.0,

        "repair_bias":
            1.0,

        "category_bias": {

            "activation":
                1.0,

            "suppression":
                1.0,

            "amplification":
                1.0,

            "resource":
                1.0,

            "damage":
                1.0,

            "stabilization":
                1.0,

            "destabilization":
                1.0
        }
    }

    # =====================================
    # apply fate shaping
    # =====================================

    apply_fate_bias(
        ecology_bias,
        fate_progression
    )

    # =====================================
    # apply stress shaping
    # =====================================

    apply_stress_bias(
        ecology_bias,
        ecology_context,
        state_labels,
        behavior_context
    )

    # =====================================
    # apply infection shaping
    # =====================================

    apply_infection_bias(
        ecology_bias,
        ecology_context
    )

    # =====================================
    # apply activation shaping
    # =====================================

    apply_activation_bias(
        ecology_bias,
        ecology_context
    )

    # =====================================
    # attach ecology bias
    # =====================================

    updated_context = dict(
        behavior_context
    )

    updated_context[
        "ecology_bias"
    ] = ecology_bias

    return updated_context


# =========================================
# Fate Bias
# =========================================

def apply_fate_bias(
    ecology_bias,
    fate_progression
):

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

    progression = (
        progression_context.get(
            "progression",
            0.0
        )
    )

    # apoptosis ecology
    if current_fate == "apoptosis":

        ecology_bias[
            "survival_bias"
        ] *= (
            1.0 - progression
        )

        ecology_bias[
            "proliferation_bias"
        ] *= 0.1

        ecology_bias[
            "mobility_bias"
        ] *= 0.5

    # necrosis ecology
    if current_fate == "necrosis":

        ecology_bias[
            "secretion_bias"
        ] *= 0.3

        ecology_bias[
            "mobility_bias"
        ] *= 0.2


# =========================================
# Stress Bias
# =========================================

def apply_stress_bias(
    ecology_bias,
    ecology_context,
    state_labels,
    behavior_context
):

    stress_ecology = ecology_context.get(
        "stress_ecology",
        {}
    )

    suppression = stress_ecology.get(
        "global_suppression",
        0.0
    )
    hir_constraints = (
        behavior_context.get(
            "hir_constraints",
            {}
        )
    )

    repair_priority = (
        hir_constraints.get(
            "repair_priority",
            0.0
        )
    )

    # global suppression
    ecology_bias[
        "secretion_bias"
    ] *= (
        1.0 - suppression
    )

    ecology_bias[
        "mobility_bias"
    ] *= (
        1.0 - suppression
    )

    # metabolic stress
    if "metabolic_stress" in state_labels:

        ecology_bias[
            "proliferation_bias"
        ] *= 0.4

        ecology_bias[
            "repair_bias"
        ] *= 1.5

    # critical damage
    if "critical_damage" in state_labels:

        ecology_bias[
            "survival_bias"
        ] *= 0.3

        ecology_bias[
            "mobility_bias"
        ] *= 0.2

    ecology_bias[
        "repair_bias"
    ] *= (
        1.0 + repair_priority
    )

# =========================================
# Infection Bias
# =========================================

def apply_infection_bias(
    ecology_bias,
    ecology_context
):

    infection_ecology = ecology_context.get(
        "infection_ecology",
        {}
    )

    infection_burden = (
        infection_ecology.get(
            "infection_burden",
            0.0
        )
    )

    # infected ecology
    if infection_burden > 0.3:

        ecology_bias[
            "repair_bias"
        ] *= 1.3

    # highly infected
    if infection_burden > 0.7:

        ecology_bias[
            "proliferation_bias"
        ] *= 0.2

        ecology_bias[
            "mobility_bias"
        ] *= 0.5


# =========================================
# Activation Bias
# =========================================

def apply_activation_bias(
    ecology_bias,
    ecology_context
):

    activation_ecology = (
        ecology_context.get(
            "activation_ecology",
            {}
        )
    )

    activation_level = (
        activation_ecology.get(
            "activation_level",
            0.0
        )
    )

    # activated state
    if activation_level > 0.5:

        ecology_bias[
            "secretion_bias"
        ] *= (
            1.0 + activation_level
        )

        ecology_bias[
            "mobility_bias"
        ] *= (
            1.0 + (
                activation_level * 0.5
            )
        )
