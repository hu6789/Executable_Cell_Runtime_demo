# aip/vml/hir_bridge.py


# =========================================
# VML → HIR Interpretation Bridge
# =========================================

def build_hir_interpretation_delta(
    vml_payload
):

    """
    translate VML deception output
    into HIR-compatible interpretation delta

    responsibilities:

        - convert deception_context
          into HIR perception modifiers

        - convert infection concealment
          into masking signals

        - convert fake resource support
          into interpretation modulation

    DOES NOT:

        - modify physiology

        - determine fate

        - suppress behaviors

        - execute HIR logic
    """

    if not vml_payload:

        return {}

    deception_context = (
        vml_payload.get(
            "deception_context",
            {}
        )
    )

    interpretation_delta = {

        "masked_signals":
            [],

        "active_modulations":
            [],

        "override_flags":
            []
    }

    # =====================================
    # infection concealment
    # =====================================

    infection_concealment = (
        deception_context.get(
            "infection_concealment",
            {}
        )
    )

    if infection_concealment:

        interpretation_delta[
            "masked_signals"
        ].append(
            "infection"
        )

    # =====================================
    # signal masking
    # =====================================

    signal_masking = (
        deception_context.get(
            "signal_masking",
            {}
        )
    )

    if signal_masking.get(
        "viral_signal",
        1.0
    ) < 1.0:

        interpretation_delta[
            "masked_signals"
        ].append(
            "viral_signal"
        )

    if signal_masking.get(
        "IFN",
        1.0
    ) < 1.0:

        interpretation_delta[
            "masked_signals"
        ].append(
            "IFN"
        )

    # =====================================
    # fake resource support
    # =====================================

    fake_resource_map = (
        deception_context.get(
            "fake_resource_map",
            {}
        )
    )

    if fake_resource_map:

        interpretation_delta[
            "active_modulations"
        ].append(
            "fake_resource_support"
        )

    # =====================================
    # concealment strength
    # =====================================

    concealment_strength = (
        deception_context.get(
            "concealment_strength",
            0.0
        )
    )

    if concealment_strength > 0.1:

        interpretation_delta[
            "override_flags"
        ].append(
            "infection_hidden"
        )

    return interpretation_delta
