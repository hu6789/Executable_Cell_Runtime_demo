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

    modulation_summary = adjusted_context.get(
        "modulation_summary",
        {}
    )

    vml_payload = modulation_summary.get(
        "vml_payload"
    )


    adjusted_context = apply_vml_signal_masking(
        adjusted_context,
        vml_payload
    )

    adjusted_context = apply_vml_resource_deception(
        adjusted_context,
        vml_payload
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

# =========================================
# VML Signal Masking
# =========================================

def apply_vml_signal_masking(
    adjusted_context,
    vml_payload
):

    if not vml_payload:

        return adjusted_context

    deception_context = (
        vml_payload.get(
            "deception_context",
            {}
        )
    )

    signal_masking = (
        deception_context.get(
            "signal_masking",
            {}
        )
    )

    node_summary = adjusted_context.get(
        "node_summary",
        {}
    )

    # =====================================
    # IFN masking
    # =====================================

    if "IFN" in node_summary:

        node_summary["IFN"] *= (

            signal_masking.get(
                "IFN",
                1.0
            )
        )

    # =====================================
    # viral signal masking
    # =====================================

    if "viral_signal" in node_summary:

        node_summary["viral_signal"] *= (

            signal_masking.get(
                "viral_signal",
                1.0
            )
        )

    adjusted_context[
        "node_summary"
    ] = node_summary

    return adjusted_context
    
# =========================================
# VML Resource Deception
# =========================================

def apply_vml_resource_deception(
    adjusted_context,
    vml_payload
):

    if not vml_payload:

        return adjusted_context

    deception_context = (
        vml_payload.get(
            "deception_context",
            {}
        )
    )

    fake_resource_map = (
        deception_context.get(
            "fake_resource_map",
            {}
        )
    )

    node_summary = adjusted_context.get(
        "node_summary",
        {}
    )

    # =====================================
    # fake ATP
    # =====================================

    if "ATP" in node_summary:

        node_summary["ATP"] *= (

            fake_resource_map.get(
                "ATP",
                1.0
            )
        )

    # =====================================
    # fake membrane state
    # =====================================

    if "cell_membrane" in node_summary:

        node_summary["cell_membrane"] *= (

            fake_resource_map.get(
                "cell_membrane",
                1.0
            )
        )

    adjusted_context[
        "node_summary"
    ] = node_summary

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
