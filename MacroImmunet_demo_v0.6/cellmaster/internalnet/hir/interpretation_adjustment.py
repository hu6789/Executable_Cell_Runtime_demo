# cellmaster/internalnet/hir/interpretation_adjustment.py

import copy
# =========================================
# Physiological Interpretation Adjustment
# apply interpretation bias
#
# modulation_runtime_state:
#     real physiological changes
#
# hir_interpretation_delta:
#     perception-level deception
# =================================
def adjust_physiological_interpretation(
    global_context,
    hir_interpretation_delta,
    runtime_entity
):

    """
    adjust physiological interpretation

    responsibilities:
        - apply masking effects
        - apply survival compensation
        - apply viral deception
        - apply external intervention
        - generate adjusted interpretation context

    DOES NOT:
        - modify runtime state
        - directly determine fate
        - directly suppress behaviors
    """

    adjusted_context = copy.deepcopy(
        global_context
    )

    interpretation_delta = (
        hir_interpretation_delta
        or {}
    )

    # =====================================
    # apply masking
    # =====================================

    adjusted_context = apply_signal_masking(

        adjusted_context,
        interpretation_delta
    )

    # =====================================
    # apply compensation
    # =====================================

    adjusted_context = apply_survival_compensation(

        adjusted_context,
        interpretation_delta
    )

    # =====================================
    # apply override
    # =====================================

    adjusted_context = apply_override_flags(

        adjusted_context,
        interpretation_delta
    )

    # =====================================
    # generate interpretation labels
    # =====================================

    interpretation_labels = (
        generate_interpretation_labels(
            adjusted_context
        )
    )

    adjusted_context[
        "interpretation_labels"
    ] = interpretation_labels

    return adjusted_context


# =========================================
# Signal Masking
# =========================================

def apply_signal_masking(
    adjusted_context,
    interpretation_delta
):

    masked_signals = interpretation_delta.get(
        "masked_signals",
        []
    )

    node_summary = adjusted_context.get(
        "node_summary",
        {}
    )

    # =====================================
    # ROS masking
    # =====================================

    if (
        "ROS" in masked_signals
        and "ROS" in node_summary
    ):

        node_summary["ROS"] *= 0.5

    # =====================================
    # stress masking
    # =====================================

    if (
        "stress" in masked_signals
        and "stress" in node_summary
    ):

        node_summary["stress"] *= 0.5

    adjusted_context[
        "node_summary"
    ] = node_summary

    return adjusted_context


# =========================================
# Survival Compensation
# =========================================

def apply_survival_compensation(
    adjusted_context,
    interpretation_delta
):

    active_modulations = interpretation_delta.get(
        "active_modulations",
        []
    )

    survival_summary = adjusted_context.get(
        "survival_summary",
        {}
    )

    # =====================================
    # apoptosis suppression
    # =====================================

    if "apoptosis_suppression" in active_modulations:

        survival_summary[
            "survival_score"
        ] *= 1.5

    # =====================================
    # fake ATP compensation
    # =====================================

    if "fake_resource_support" in active_modulations:

        survival_summary[
            "survival_score"
        ] += 2.0

    adjusted_context[
        "survival_summary"
    ] = survival_summary

    return adjusted_context


# =========================================
# Override Flags
# =========================================

def apply_override_flags(
    adjusted_context,
    interpretation_delta
):

    override_flags = interpretation_delta.get(
        "override_flags",
        []
    )

    adjusted_context[
        "override_flags"
    ] = override_flags

    return adjusted_context


# =========================================
# Interpretation Labels
# =========================================

def generate_interpretation_labels(
    adjusted_context
):

    labels = []

    node_summary = adjusted_context.get(
        "node_summary",
        {}
    )

    integrity_summary = adjusted_context.get(
        "integrity_summary",
        {}
    )

    survival_summary = adjusted_context.get(
        "survival_summary",
        {}
    )

    # =====================================
    # metabolic stress
    # =====================================

    ATP = node_summary.get(
        "ATP",
        0.0
    )

    if ATP < 2.0:

        labels.append(
            "metabolic_stress"
        )

    # =====================================
    # oxidative stress
    # =====================================

    ROS = node_summary.get(
        "ROS",
        0.0
    )

    if ROS > 5.0:

        labels.append(
            "oxidative_stress"
        )

    # =====================================
    # integrity collapse
    # =====================================

    if integrity_summary.get(
        "critical_integrity",
        False
    ):

        labels.append(
            "integrity_collapse"
        )

    # =====================================
    # survival collapse
    # =====================================

    if not survival_summary.get(
        "survival_possible",
        True
    ):

        labels.append(
            "survival_collapse"
        )

    return labels
