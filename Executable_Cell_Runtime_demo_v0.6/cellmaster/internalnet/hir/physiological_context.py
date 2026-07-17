# cellmaster/internalnet/hir/physiological_context.py

"""
Global Physiological Context

Runtime State
        │
        ▼
Physiology Summary
        │
        ▼
HIR

HIR should never directly interpret
runtime nodes.

Instead, HIR consumes a unified
physiology summary.

This file is therefore the SSOT
between RuntimeGraph and HIR.
"""

# =========================================
# Global Physiological Context Integration
# =========================================

def integrate_global_context(
    runtime_entity,
    runtime_state,
    modulation_runtime_state
):
    """
    integrate cell-level physiology

    responsibilities

        - summarize runtime physiology
        - summarize modulation payload
        - estimate integrity
        - estimate survival tendency

    DOES NOT

        - determine fate
        - regulate behaviors
        - modify runtime state
    """

    physiology_summary = summarize_physiology(
        runtime_state
    )

    modulation_summary = summarize_modulation_state(
        modulation_runtime_state
    )

    integrity_summary = estimate_integrity(
        physiology_summary
    )

    survival_summary = estimate_survival_tendency(
        physiology_summary,
        integrity_summary
    )

    identity = safe_get_identity(
        runtime_entity
    )

    return {

        "cell_id":
            safe_get_id(runtime_entity),

        "cell_type":
            identity.get(
                "cell_type"
            ),

        "genotype":
            identity.get(
                "genotype"
            ),

        # reality
        "runtime_state":
            runtime_state,

        # HIR SSOT
        "physiology_summary":
            physiology_summary,

        # modulation payloads
        "modulation_summary":
            modulation_summary,

        # global estimations
        "integrity_summary":
            integrity_summary,

        "survival_summary":
            survival_summary
    }


# =========================================
# Physiology Summary
# =========================================

def summarize_physiology(
    runtime_state
):
    """
    convert runtime nodes into
    physiological abstractions
    """

    return {

        "resources":
            summarize_resource(
                runtime_state
            ),

        "stress":
            summarize_stress(
                runtime_state
            ),

        "damage":
            summarize_damage(
                runtime_state
            ),

        "signal":
            summarize_signal(
                runtime_state
            ),

        "viral":
            summarize_viral(
                runtime_state
            )
    }


# =========================================
# Resource Summary
# =========================================

def summarize_resource(
    runtime_state
):

    return {

        "ATP":
            runtime_state.get(
                "ATP",
                0.0
            ),

        "glucose":
            runtime_state.get(
                "glucose",
                0.0
            ),

        "protein":
            runtime_state.get(
                "protein",
                0.0
            ),

        "amino_acid":
            runtime_state.get(
                "amino_acid",
                0.0
            )
    }


# =========================================
# Stress Summary
# =========================================

def summarize_stress(
    runtime_state
):

    return {

        "ROS":
            runtime_state.get(
                "ROS",
                0.0
            ),

        "stress":
            runtime_state.get(
                "stress",
                0.0
            )
    }


# =========================================
# Damage Summary
# =========================================

def summarize_damage(
    runtime_state
):

    return {

        "membrane_integrity":
            runtime_state.get(
                "membrane_integrity",
                1.0
            ),

        "damage":
            runtime_state.get(
                "damage",
                0.0
            )
    }


# =========================================
# Signal Summary
# =========================================

def summarize_signal(
    runtime_state
):

    return {

        "IFN":
            runtime_state.get(
                "IFN",
                0.0
            ),

        "CXCL10":
            runtime_state.get(
                "CXCL10",
                0.0
            ),

        "IL2":
            runtime_state.get(
                "IL2",
                0.0
            )
    }


# =========================================
# Viral Summary
# =========================================

def summarize_viral(
    runtime_state
):

    return {

        "viral_signal":
            runtime_state.get(
                "viral_signal",
                0.0
            ),

        "viral_load":
            runtime_state.get(
                "viral_load",
                runtime_state.get(
                    "infection_burden",
                    0.0
                )
            )
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
    physiology_summary
):

    damage = physiology_summary.get(
        "damage",
        {}
    )

    membrane = damage.get(
        "membrane_integrity",
        1.0
    )

    return {

        "integrity_score":
            membrane,

        "critical_integrity":
            membrane < 20
    }


# =========================================
# Survival Estimation
# =========================================

def estimate_survival_tendency(
    physiology_summary,
    integrity_summary
):

    resource = physiology_summary.get(
        "resources",
        {}
    )

    ATP = resource.get(
        "ATP",
        0.0
    )

    integrity = integrity_summary.get(
        "integrity_score",
        0.0
    )

    survival_score = min(
        ATP,
        integrity
    )

    return {

        "survival_score":
            survival_score,

        "survival_possible":
            survival_score > 20
    }


# =========================================
# Runtime Entity Helpers
# =========================================

def safe_get_identity(
    runtime_entity
):

    if hasattr(
        runtime_entity,
        "identity"
    ):

        return runtime_entity.identity

    if isinstance(
        runtime_entity,
        dict
    ):

        return runtime_entity.get(
            "identity",
            {}
        )

    return {}


def safe_get_id(
    runtime_entity
):

    if hasattr(
        runtime_entity,
        "id"
    ):

        return runtime_entity.id

    if isinstance(
        runtime_entity,
        dict
    ):

        return runtime_entity.get(
            "id"
        )

    return None
