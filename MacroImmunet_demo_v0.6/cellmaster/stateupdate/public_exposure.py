# cellmaster/stateupdate/public_exposure.py

"""
Public Exposure Builder

Consumes:

    interpreted_exposure

Produces:

    outward-readable
    membrane/interface representation

Does NOT:

    interpret physiology
    evaluate fate
    consume runtime_state
"""
# =========================================
# Public Exposure Builder
# =========================================

def build_public_exposure(
    interpreted_exposure
):

    """
    build outward-readable
    PublicExposure layer

    PublicExposure:
        membrane/interface abstraction
        visible to external systems

    readable by:
        - ScanMaster
        - receptor interaction
        - immune recognition
        - environment sensing
    """

    # =====================================
    # extract interpreted exposure
    # =====================================

    surface_markers = interpreted_exposure.get(
        "surface_markers",
        []
    )

    danger_signals = interpreted_exposure.get(
        "danger_signals",
        []
    )

    secreted_signals = interpreted_exposure.get(
        "secreted_signals",
        []
    )

    membrane_state = interpreted_exposure.get(
        "membrane_state",
        "stable"
    )

    exposure_labels = interpreted_exposure.get(
        "exposure_labels",
        []
    )

    # =====================================
    # build exposure visibility
    # =====================================

    visibility = evaluate_visibility(

        membrane_state,
        exposure_labels
    )

    # =====================================
    # outward exposure package
    # =====================================

    public_exposure = {

        # ---------------------------------
        # membrane/interface phenotype
        # ---------------------------------

        "surface_markers":
            surface_markers,

        # ---------------------------------
        # outward danger representation
        # ---------------------------------

        "danger_signals":
            danger_signals,

        # ---------------------------------
        # outward secreted molecules
        # ---------------------------------

        "secreted_signals":
            secreted_signals,

        # ---------------------------------
        # membrane condition
        # ---------------------------------

        "membrane_state":
            membrane_state,

        # ---------------------------------
        # semantic exposure tags
        # ---------------------------------

        "exposure_labels":
            exposure_labels,

        # ---------------------------------
        # visibility/accessibility
        # ---------------------------------

        "exposure_visibility":
            visibility
    }

    return public_exposure


# =========================================
# Visibility Evaluation
# =========================================

def evaluate_visibility(
    membrane_state,
    exposure_labels
):

    """
    evaluate how strongly
    outward state is exposed

    future:
        membrane integrity
        cloaking
        viral masking
        stealth modulation
    """

    # =====================================
    # stressed cells
    # =====================================

    if membrane_state == "stressed":

        return "high"

    # =====================================
    # activated exposure
    # =====================================

    if "activated" in exposure_labels:

        return "medium"

    # =====================================
    # default
    # =====================================

    return "low"
