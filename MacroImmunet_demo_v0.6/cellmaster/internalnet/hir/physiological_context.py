# cellmaster/internalnet/hir/physiological_context.py


# =========================================
# Global Physiological Context Integration
# =========================================

def integrate_global_context(
    runtime_entity,
    runtime_state,
    modulation_runtime_state
):

    """
    integrate cell-level physiological state

    responsibilities:
        - collect cross-node physiology
        - summarize passive burden
        - summarize resource integrity
        - summarize systemic stress
        - generate global interpretation context

    DOES NOT:
        - determine fate
        - generate constraints
        - modify runtime state
    """
    # =====================================
    # aggregate node state
    # =====================================

    node_summary = summarize_node_state(
        runtime_state
    )
    
    modulation_summary = summarize_modulation_state(
        modulation_runtime_state
    )
    # =====================================
    # estimate integrity
    # =====================================

    integrity_summary = estimate_integrity(
        runtime_state
    )

    # =====================================
    # estimate survival tendency
    # =====================================

    survival_summary = estimate_survival_tendency(
        runtime_state,
        integrity_summary
    )
    
    identity = runtime_entity.identity
    
    return {

        "cell_id":
            runtime_entity.id,

        "cell_type":
            identity.get("cell_type"),

        "genotype":
            identity.get("genotype"),

        "runtime_state":
            runtime_state,

        "node_summary":
            node_summary,

        "modulation_summary":
            modulation_summary,

        "integrity_summary":
            integrity_summary,

        "survival_summary":
            survival_summary
    }


# =========================================
# Node State Summary
# =========================================

def summarize_node_state(
    runtime_state
):

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    ROS = runtime_state.get(
        "ROS",
        0.0
    )

    membrane_integrity = runtime_state.get(
        "membrane_integrity",
        1.0
    )

    stress = runtime_state.get(
        "stress",
        0.0
    )

    return {

        # legacy

        "ATP":
            ATP,

        "ROS":
            ROS,

        "membrane_integrity":
            membrane_integrity,

        "stress":
            stress,

        # structured

        "metabolism": {

            "ATP":
                ATP
        },

        "stress_summary": {

            "ROS":
                ROS,

            "stress":
                stress
        },

        "integrity": {

            "membrane_integrity":
                membrane_integrity
        }
    }

# =========================================
# Modulation Summary
# =========================================

def summarize_modulation_state(
    modulation_result
):

    if modulation_result is None:

        return {

            "active_modulations": [],
            "masked_signals": [],
            "override_flags": []
        }

    return {

        "active_modulations":
            modulation_result.get(
                "active_modulations",
                []
            ),

        "masked_signals":
            modulation_result.get(
                "masked_signals",
                []
            ),

        "override_flags":
            modulation_result.get(
                "override_flags",
                []
            )
    }


# =========================================
# Integrity Estimation
# =========================================

def estimate_integrity(
    runtime_state
):

    membrane_integrity = runtime_state.get(
        "membrane_integrity",
        1.0
    )

    integrity_score = membrane_integrity

    return {

        "integrity_score":
            membrane_integrity,

        "critical_integrity":
            membrane_integrity < 0.2
    }


# =========================================
# Survival Estimation
# =========================================

def estimate_survival_tendency(
    runtime_state,
    integrity_summary
):

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    integrity_score = integrity_summary.get(
        "integrity_score",
        0.0
    )

    survival_score = (
        ATP * integrity_score
    )

    return {

        "survival_score":
            survival_score,

        "survival_possible":
            survival_score > 0.5
    }
