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
    
    identity = safe_get_identity(runtime_entity)
    cell_id = safe_get_id(runtime_entity)
    
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
    modulation_runtime_state
):

    if modulation_runtime_state is None:

        return {}

    payloads = (
        modulation_runtime_state.get(
            "payloads",
            []
        )
    )

    vml_payload = None

    for payload in payloads:

        if payload.get(
            "_payload_type"
        ) == "vml":

            vml_payload = payload.get(
                "payload"
            )

            break

    return {

        "vml_payload":
            vml_payload
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
    
def safe_get_identity(runtime_entity):
    if hasattr(runtime_entity, "identity"):
        return runtime_entity.identity

    if isinstance(runtime_entity, dict):
        return runtime_entity.get("identity", {})

    return {}
    
def safe_get_id(runtime_entity):
    if hasattr(runtime_entity, "id"):
        return runtime_entity.id
    if isinstance(runtime_entity, dict):
        return runtime_entity.get("id", None)
    return None
