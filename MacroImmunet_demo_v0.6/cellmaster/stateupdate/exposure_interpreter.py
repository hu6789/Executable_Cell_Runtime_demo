# cellmaster/stateupdate/exposure_interpreter.py


# =========================================
# Exposure Interpretation Layer
# =========================================

def interpret_exposure(
    runtime_context
):

    """
    convert internal runtime physiology
    into outward-readable semantic exposure

    responsibilities:
        - physiology interpretation
        - danger interpretation
        - membrane/interface meaning
        - exposure semantic abstraction

    DOES NOT:
        - write world
        - generate intents
    """

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    behavior_packages = runtime_context.get(
        "behavior_packages",
        []
    )

    fate_state = runtime_context.get(
        "fate_state",
        "stable"
    )

    # =====================================
    # exposure package
    # =====================================

    exposure = {

        "surface_markers": [],

        "danger_signals": [],

        "secreted_signals": [],

        "membrane_state":
            "stable",

        "exposure_labels": []
    }

    # =====================================
    # metabolic stress
    # =====================================

    if runtime_labels.get(
        "metabolic_stress",
        False
    ):

        exposure[
            "danger_signals"
        ].append(
            "metabolic_stress"
        )

        exposure[
            "exposure_labels"
        ].append(
            "stressed"
        )

        exposure[
            "membrane_state"
        ] = "stressed"

    # =====================================
    # infection exposure
    # =====================================

    if runtime_labels.get(
        "infected",
        False
    ):

        exposure[
            "surface_markers"
        ].append(
            "infected_surface"
        )

        exposure[
            "danger_signals"
        ].append(
            "viral_pattern"
        )

    # =====================================
    # activated phenotype
    # =====================================

    if runtime_labels.get(
        "activated",
        False
    ):

        exposure[
            "surface_markers"
        ].append(
            "activation_marker"
        )

    # =====================================
    # behavior package exposure
    # =====================================

    for package in behavior_packages:

        behavior_type = package.get(
            "behavior_type"
        )

        # ---------------------------------
        # IFN secretion
        # ---------------------------------

        if behavior_type == (
            "secrete_IFN_gamma"
        ):

            exposure[
                "secreted_signals"
            ].append({

                "signal_type":
                    "IFN_gamma",

                "strength":
                    package.get(
                        "behavior_strength",
                        0.0
                    )
            })

        # ---------------------------------
        # contact phenotype
        # ---------------------------------

        elif behavior_type == (
            "maintain_contact"
        ):

            exposure[
                "surface_markers"
            ].append(
                "contact_interface"
            )

    # =====================================
    # fate exposure
    # =====================================

    if fate_state == "stressed":

        exposure[
            "danger_signals"
        ].append(
            "fate_stress"
        )

    return exposure
