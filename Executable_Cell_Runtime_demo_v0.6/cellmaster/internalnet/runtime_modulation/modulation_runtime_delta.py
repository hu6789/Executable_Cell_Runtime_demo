# cellmaster/internalnet/runtime_modulation/modulation_runtime_delta.py


# =========================================
# Build Runtime Modulation Delta
# =========================================

def build_modulation_runtime_delta(
    modulation_runtime_state
):

    """
    build runtime-effective modulation delta

    responsibilities:
        - convert modulation state
          into downstream runtime patches
        - expose runtime intervention layer
        - provide runtime-compatible modulation effects

    DOES NOT:
        - mutate runtime state
        - apply world writes
        - execute behaviors
    """

    runtime_delta = {

        "node_runtime_delta":
            {},

        "passive_runtime_delta":
            {},

        "behavior_runtime_delta":
            {},

        "hir_runtime_delta":
            {},

        "global_runtime_delta":
            {},
        
        "payloads":
            modulation_runtime_state.get(
                "payloads",
                []
            )
    }

    # =====================================
    # node modulation
    # =====================================

    for target, modulation in (
        modulation_runtime_state.get(
            "node_modulations",
            {}
        ).items()
    ):

        runtime_delta[
            "node_runtime_delta"
        ][target] = extract_runtime_effect(
            modulation
        )

    # =====================================
    # passive modulation
    # =====================================

    for target, modulation in (
        modulation_runtime_state.get(
            "passive_modulations",
            {}
        ).items()
    ):

        runtime_delta[
            "passive_runtime_delta"
        ][target] = extract_runtime_effect(
            modulation
        )

    # =====================================
    # behavior modulation
    # =====================================

    for target, modulation in (
        modulation_runtime_state.get(
            "behavior_modulations",
            {}
        ).items()
    ):

        runtime_delta[
            "behavior_runtime_delta"
        ][target] = extract_runtime_effect(
            modulation
        )

    # =====================================
    # HIR modulation
    # =====================================

    for target, modulation in (
        modulation_runtime_state.get(
            "hir_modulations",
            {}
        ).items()
    ):

        runtime_delta[
            "hir_runtime_delta"
        ][target] = extract_runtime_effect(
            modulation
        )

    # =====================================
    # global modulation
    # =====================================

    for target, modulation in (
        modulation_runtime_state.get(
            "global_modulations",
            {}
        ).items()
    ):

        runtime_delta[
            "global_runtime_delta"
        ][target] = extract_runtime_effect(
            modulation
        )

    return runtime_delta


# =========================================
# Extract Runtime Effect
# =========================================

def extract_runtime_effect(
    modulation
):

    """
    normalize runtime modulation effect
    into downstream-compatible structure
    """

    return {

        "multiply":
            modulation.get(
                "multiply",
                1.0
            ),

        "add":
            modulation.get(
                "add",
                0.0
            ),

        "override":
            modulation.get(
                "override"
            ),

        "blocked":
            modulation.get(
                "blocked",
                False
            ),

        "sources":
            modulation.get(
                "sources",
                []
            )
    }
