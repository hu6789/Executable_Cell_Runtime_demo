# aip/vml/deception_context.py


# =========================================
# Viral Deception Layer
# =========================================

"""
responsibilities:

    - distort host interpretation

    - hide infection burden

    - suppress immune perception

    - generate fake physiological context

DOES NOT:

    - modify true runtime state

    - execute behaviors

    - determine viral lifecycle
"""


# =========================================
# main
# =========================================

def build_deception_context(

    runtime_state,

    viral_state_label,

    infection_load,

    execution_profile
):

    viral_load = infection_load.get(
        "viral_load",
        0.0
    )

    stealth_bias = execution_profile.get(
        "stealth_bias",
        0.0
    )

    # =====================================
    # concealment strength
    # =====================================

    concealment_strength = min(

        1.0,

        stealth_bias
        + viral_load / 200.0
    )

    # =====================================
    # signal masking
    # =====================================

    signal_masking = {

        "viral_signal":

            1.0 - concealment_strength,

        "IFN":

            1.0 - (
                concealment_strength * 0.5
            )
    }

    # =====================================
    # infection concealment
    # =====================================

    infection_concealment = {

        "viral_RNA":

            1.0 - concealment_strength,

        "viral_protein":

            1.0 - concealment_strength
    }

    # =====================================
    # fake resource availability
    # =====================================

    fake_resource_map = {

        "ATP":

            1.0 + (
                concealment_strength * 0.3
            ),

        "cell_membrane":

            1.0 + (
                concealment_strength * 0.2
            )
    }

    # =====================================
    # interpretation distortion
    # =====================================

    interpretation_weights = {

        "infection":

            1.0 - concealment_strength,

        "stress":

            1.0 - (
                concealment_strength * 0.5
            )
    }

    # =====================================
    # output
    # =====================================

    return {

        "viral_state_label":
            viral_state_label,

        "concealment_strength":
            concealment_strength,

        "signal_masking":
            signal_masking,

        "infection_concealment":
            infection_concealment,

        "fake_resource_map":
            fake_resource_map,

        "interpretation_weights":
            interpretation_weights
    }
    
