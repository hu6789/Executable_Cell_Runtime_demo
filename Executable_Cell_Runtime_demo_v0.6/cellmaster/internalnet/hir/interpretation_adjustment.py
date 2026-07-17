# cellmaster/internalnet/hir/interpretation_adjustment.py

import copy

# =========================================
# Physiological Interpretation Adjustment
# =========================================
#
# Reality
#     ↓
# physiology_summary
#
# Interpretation
#     ↓
# perceived_physiology
#
# Constraint / Behavior / Fate
#
# Interpretation never modifies runtime_state.
# Only perception is adjusted.
#
# =========================================


def adjust_physiological_interpretation(
    perceived_context,
    hir_interpretation_delta,
    runtime_entity
):

    """
    Construct perceived physiological context.

    responsibilities

        - apply perception-level modulation
        - apply signal masking
        - apply resource deception
        - apply damage deception
        - apply viral deception
        - generate interpretation labels

    DOES NOT

        - modify runtime state
        - modify physiology summary
        - determine fate
    """

    adjusted_context = copy.deepcopy(perceived_context)

    physiology = copy.deepcopy(

        adjusted_context.get(
            "physiology_summary",
            {}
        )
    )

    deception_context = extract_deception_context(
        adjusted_context,
        hir_interpretation_delta
    )

    physiology = apply_signal_masking(
        physiology,
        deception_context
    )

    physiology = apply_resource_deception(
        physiology,
        deception_context
    )

    physiology = apply_damage_deception(
        physiology,
        deception_context
    )

    physiology = apply_viral_deception(
        physiology,
        deception_context
    )

    adjusted_context[
        "perceived_physiology"
    ] = physiology

    adjusted_context[
        "interpretation_labels"
    ] = generate_interpretation_labels(
        physiology
    )

    return adjusted_context


# =========================================
# Deception Context
# =========================================

def extract_deception_context(
    perceived_context,
    hir_interpretation_delta
):

    if hir_interpretation_delta:

        return hir_interpretation_delta.get(
            "deception_context",
            {}
        )

    modulation_summary = perceived_context.get(
        "modulation_summary",
        {}
    )

    vml_payload = modulation_summary.get(
        "vml_payload"
    )

    if not vml_payload:

        return {}

    return vml_payload.get(
        "deception_context",
        {}
    )


# =========================================
# Signal Masking
# =========================================

def apply_signal_masking(
    physiology,
    deception_context
):

    signal_mask = deception_context.get(
        "signal_masking",
        {}
    )

    signals = physiology.get(
        "signals",
        {}
    )

    for signal, scale in signal_mask.items():

        if signal in signals:

            signals[signal] *= scale

    physiology["signals"] = signals

    return physiology


# =========================================
# Resource Deception
# =========================================

def apply_resource_deception(
    physiology,
    deception_context
):

    resource_map = deception_context.get(
        "fake_resource_map",
        {}
    )

    resources = physiology.get(
        "resources",
        {}
    )

    for resource, scale in resource_map.items():

        if resource in resources:

            resources[resource] *= scale

    physiology["resources"] = resources

    return physiology


# =========================================
# Damage Deception
# =========================================

def apply_damage_deception(
    physiology,
    deception_context
):

    damage_mask = deception_context.get(
        "damage_masking",
        {}
    )

    damage = physiology.get(
        "damage",
        {}
    )

    for item, scale in damage_mask.items():

        if item in damage:

            damage[item] *= scale

    physiology["damage"] = damage

    return physiology


# =========================================
# Viral Deception
# =========================================

def apply_viral_deception(
    physiology,
    deception_context
):

    viral_mask = deception_context.get(
        "viral_masking",
        {}
    )

    viral = physiology.get(
        "viral",
        {}
    )

    for item, scale in viral_mask.items():

        if item in viral:

            viral[item] *= scale

    physiology["viral"] = viral

    return physiology


# =========================================
# Interpretation Labels
# =========================================

def generate_interpretation_labels(
    physiology
):

    labels = []

    resources = physiology.get(
        "resources",
        {}
    )

    stress = physiology.get(
        "stress",
        {}
    )

    damage = physiology.get(
        "damage",
        {}
    )

    viral = physiology.get(
        "viral",
        {}
    )

    # -------------------------------------

    ATP = resources.get(
        "ATP",
        100.0
    )

    if ATP < 20:

        labels.append(
            "metabolic_stress"
        )

    # -------------------------------------

    ROS = stress.get(
        "ROS",
        0.0
    )

    if ROS > 50:

        labels.append(
            "oxidative_stress"
        )

    # -------------------------------------

    membrane = damage.get(
        "membrane_integrity",
        100.0
    )

    if membrane < 20:

        labels.append(
            "integrity_collapse"
        )

    # -------------------------------------

    viral_load = viral.get(
        "viral_load",
        0.0
    )

    if viral_load > 20:

        labels.append(
            "viral_pressure"
        )

    # -------------------------------------

    survival = physiology.get(
        "survival_score",
        100.0
    )

    if survival < 20:

        labels.append(
            "survival_collapse"
        )

    return labels
