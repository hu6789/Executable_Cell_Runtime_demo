# cellmaster/internalnet/runtime_modulation/modulation_runtime_state.py


# =========================================
# Build Modulation Runtime State
# =========================================

def build_modulation_runtime_state(
    aggregated_modulations
):

    """
    build runtime-effective modulation state

    responsibilities:
        - organize modulation by semantic layer
        - expose downstream-compatible runtime state
        - provide unified modulation lookup
        - preserve runtime-effective modulation semantics

    DOES NOT:
        - execute modulation
        - mutate runtime state
        - apply world writes
    """

    runtime_state = {

        # =================================
        # node-level modulation
        # =================================

        "node_modulations":
            {},

        # =================================
        # passive-level modulation
        # =================================

        "passive_modulations":
            {},

        # =================================
        # behavior-level modulation
        # =================================

        "behavior_modulations":
            {},

        # =================================
        # HIR-level modulation
        # =================================

        "hir_modulations":
            {},

        # =================================
        # global runtime modulation
        # =================================

        "global_modulations":
            {}
    }

    # =====================================
    # classify modulation targets
    # =====================================

    for target, modulation in (
        aggregated_modulations.items()
    ):

        modulation_type = detect_modulation_type(
            target,
            modulation
        )

        # =================================
        # node modulation
        # =================================

        if modulation_type == "node":

            runtime_state[
                "node_modulations"
            ][target] = modulation

        # =================================
        # passive modulation
        # =================================

        elif modulation_type == "passive":

            runtime_state[
                "passive_modulations"
            ][target] = modulation

        # =================================
        # behavior modulation
        # =================================

        elif modulation_type == "behavior":

            runtime_state[
                "behavior_modulations"
            ][target] = modulation

        # =================================
        # HIR modulation
        # =================================

        elif modulation_type == "hir":

            runtime_state[
                "hir_modulations"
            ][target] = modulation

        # =================================
        # fallback global
        # =================================

        else:

            runtime_state[
                "global_modulations"
            ][target] = modulation

    return runtime_state


# =========================================
# Detect Modulation Type
# =========================================

def detect_modulation_type(
    target,
    modulation
):

    """
    semantic modulation classification

    current heuristic version

    future:
        may use explicit modulation_type
        from modulation_result
    """

    target_lower = str(
        target
    ).lower()

    # =====================================
    # node
    # =====================================

    if "node" in target_lower:

        return "node"

    # =====================================
    # passive
    # =====================================

    if "passive" in target_lower:

        return "passive"

    # =====================================
    # behavior
    # =====================================

    if "behavior" in target_lower:

        return "behavior"

    # =====================================
    # HIR
    # =====================================

    if "hir" in target_lower:

        return "hir"

    # =====================================
    # fallback
    # =====================================

    return "global"
