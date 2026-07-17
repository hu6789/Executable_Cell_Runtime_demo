# cellmaster/internalnet/behavior_engine/ecology_bias.py

"""
Behavior Ecology Bias

This layer only provides ecological preference.

It DOES NOT:

    - block behaviors
    - allocate budgets
    - apply physiological suppression

Those are HIR responsibilities.
"""


# ==========================================================
# Main
# ==========================================================

def apply_ecology_bias(
    behavior_context
):

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

    physiological_constraints = (
        behavior_context.get(
            "physiological_constraints",
            {}
        )
    )

    ecology_bias = initialize_ecology_bias()

    apply_fate_bias(
        ecology_bias,
        fate_progression
    )

    apply_stress_bias(
        ecology_bias,
        ecology_context,
        state_labels,
        physiological_constraints
    )

    apply_activation_bias(
        ecology_bias,
        ecology_context
    )

    apply_infection_bias(
        ecology_bias,
        ecology_context
    )

    apply_resource_bias(
        ecology_bias,
        ecology_context
    )

    apply_future_reserved_bias(
        ecology_bias,
        behavior_context
    )

    updated = dict(
        behavior_context
    )

    updated[
        "ecology_bias"
    ] = ecology_bias

    return updated


# ==========================================================
# Initialize
# ==========================================================

def initialize_ecology_bias():

    return {

        "survival_bias":1.0,

        "repair_bias":1.0,

        "mobility_bias":1.0,

        "secretion_bias":1.0,

        "proliferation_bias":1.0,

        "category_bias":{

            "metabolism":1.0,

            "translation":1.0,

            "repair":1.0,

            "mobility":1.0,

            "secretion":1.0,

            "proliferation":1.0,

            "immune":1.0,

            "viral":1.0
        }
    }


# ==========================================================
# Fate Bias
# ==========================================================

def apply_fate_bias(
    ecology_bias,
    fate_progression
):

    progression = fate_progression.get(
        "progression_context",
        {}
    )

    fate = progression.get(
        "fate",
        "stable"
    )

    p = progression.get(
        "progression",
        0.0
    )

    if fate == "apoptosis":

        ecology_bias[
            "survival_bias"
        ] *= max(
            0.0,
            1.0 - p
        )

        ecology_bias[
            "repair_bias"
        ] *= (
            1.0 + p
        )

        ecology_bias[
            "category_bias"
        ][
            "repair"
        ] *= (
            1.0 + p
        )

        ecology_bias[
            "category_bias"
        ][
            "proliferation"
        ] *= 0.2

    elif fate == "necrosis":

        ecology_bias[
            "mobility_bias"
        ] *= 0.2

        ecology_bias[
            "secretion_bias"
        ] *= 0.3

        ecology_bias[
            "category_bias"
        ][
            "repair"
        ] *= 0.5


# ==========================================================
# Stress Bias
# ==========================================================

def apply_stress_bias(

    ecology_bias,

    ecology_context,

    state_labels,

    physiological_constraints
):

    suppression = (

        ecology_context.get(
            "stress_ecology",
            {}
        ).get(
            "global_suppression",
            0.0
        )
    )

    repair_priority = (

        physiological_constraints.get(
            "repair_priority",
            0.0
        )
    )

    ecology_bias[
        "repair_bias"
    ] *= (
        1.0 + repair_priority
    )

    ecology_bias[
        "category_bias"
    ][
        "repair"
    ] *= (
        1.0 + repair_priority
    )

    ecology_bias[
        "mobility_bias"
    ] *= (
        1.0 - suppression
    )

    ecology_bias[
        "secretion_bias"
    ] *= (
        1.0 - suppression
    )

    if "metabolic_stress" in state_labels:

        ecology_bias[
            "category_bias"
        ][
            "metabolism"
        ] *= 1.3

        ecology_bias[
            "category_bias"
        ][
            "translation"
        ] *= 0.6

    if "oxidative_stress" in state_labels:

        ecology_bias[
            "category_bias"
        ][
            "repair"
        ] *= 1.5

    if "critical_damage" in state_labels:

        ecology_bias[
            "survival_bias"
        ] *= 0.3

        ecology_bias[
            "repair_bias"
        ] *= 1.8


# ==========================================================
# Activation Bias
# ==========================================================

def apply_activation_bias(
    ecology_bias,
    ecology_context
):

    activation = (

        ecology_context.get(
            "activation_ecology",
            {}
        ).get(
            "activation_level",
            0.0
        )
    )

    if activation <= 0:

        return

    ecology_bias[
        "category_bias"
    ][
        "immune"
    ] *= (
        1.0 + activation
    )

    ecology_bias[
        "secretion_bias"
    ] *= (
        1.0 + activation
    )

    ecology_bias[
        "mobility_bias"
    ] *= (
        1.0 + activation * 0.5
    )


# ==========================================================
# Infection Bias
# ==========================================================

def apply_infection_bias(
    ecology_bias,
    ecology_context
):

    infection = (

        ecology_context.get(
            "infection_ecology",
            {}
        ).get(
            "infection_burden",
            0.0
        )
    )

    if infection > 0.3:

        ecology_bias[
            "category_bias"
        ][
            "immune"
        ] *= 1.2

        ecology_bias[
            "repair_bias"
        ] *= 1.2

    if infection > 0.7:

        ecology_bias[
            "category_bias"
        ][
            "viral"
        ] *= 1.4

        ecology_bias[
            "category_bias"
        ][
            "proliferation"
        ] *= 0.3


# ==========================================================
# Resource Bias
# ==========================================================

def apply_resource_bias(
    ecology_bias,
    ecology_context
):

    ATP = (

        ecology_context.get(
            "resource_ecology",
            {}
        ).get(
            "ATP",
            0.0
        )
    )

    if ATP < 5:

        ecology_bias[
            "category_bias"
        ][
            "metabolism"
        ] *= 1.5

        ecology_bias[
            "category_bias"
        ][
            "translation"
        ] *= 0.5


# ==========================================================
# Reserved Future Bias
# ==========================================================

def apply_future_reserved_bias(
    ecology_bias,
    behavior_context
):
    """
    Reserved extension point.

    Future:

        - lineage bias

        - tissue preference

        - cytokine ecology

        - circadian rhythm

        - adaptive memory

        - virus-specific ecology

        - AI modulation
    """

    return
