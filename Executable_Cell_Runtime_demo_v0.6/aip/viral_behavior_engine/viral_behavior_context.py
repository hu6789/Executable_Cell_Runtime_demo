# aip/viral_behavior_engine/viral_behavior_context.py

# =========================================
# Viral Behavior Execution Context
# Overlay Layer (NOT decision layer)
# =========================================

def build_viral_behavior_context(
    runtime_entity,
    passive_runtime_state,
    behavior_graph,
    viral_cycle_state=None,
    vml_payload=None
):

    """
    viral-only execution context

    responsibilities:
        - build abstract viral execution frame
        - apply VML interpretation layer
        - inject viral cycle bias

    DOES NOT:
        - expose full host state
        - expose raw physiology
        - decide behavior
    """

    # =====================================
    # VML bias
    # =====================================

    vml_bias = extract_vml_bias(vml_payload)

    # =====================================
    # viral resource abstraction (NOT raw ATP)
    # =====================================

    resource_projection = {
        "availability": compute_resource_availability(runtime_state),
        "stress_proxy": runtime_state.get("stress", 0.0) * 0.3
    }

    # =====================================
    # execution frame (CLEANED)
    # =====================================

    execution_frame = {

        "viral_id": runtime_entity.id,
        "viral_surface_type": runtime_entity.identity.get("cell_type"),

        "viral_cycle_state": viral_cycle_state or "entry",

        "behavior_graph_ref": behavior_graph,

        # viral interpretation layer only
        "vml_bias": vml_bias,

        # abstracted, NOT raw host state
        "resource_projection": resource_projection,

        # cycle bias
        "viral_cycle_bias": compute_viral_cycle_bias(viral_cycle_state)
    }

    return execution_frame

# =========================================
# VML extraction (safe view only)
# =========================================

def extract_vml_bias(vml_payload):

    if not vml_payload:
        return {}

    deception = vml_payload.get("deception_context", {})

    return {

        "signal_masking": deception.get("signal_masking", {}),
        "fake_resource_map": deception.get("fake_resource_map", {}),
        "interpretation_weights": deception.get("interpretation_weights", {})
    }


# =========================================
# viral cycle bias
# =========================================

def compute_resource_availability(runtime_state):

    atp = runtime_state.get("ATP", 0.0)
    membrane = runtime_state.get("cell_membrane", 0.0)

    # compress into non-biological proxy
    return (atp * 0.6 + membrane * 0.4)
