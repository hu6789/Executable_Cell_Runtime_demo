# aip/vml/viral_cycle.py


# =========================================
# Viral Lifecycle State Determination
# =========================================

"""
responsibilities:

    - determine viral lifecycle phase

    - use REAL physiological state

    - provide truth-state for VML

DOES NOT:

    - generate deception

    - modify runtime state

    - execute viral behaviors

outputs:

    viral_state_label
"""


# =========================================
# state labels
# =========================================

ENTRY = "entry"

REPLICATION = "replication"

ASSEMBLY = "assembly"

RELEASE = "release"

STRESS = "stress"

COLLAPSE = "collapse"


# =========================================
# main entry
# =========================================

def determine_viral_cycle_state(

    runtime_state
):

    """
    runtime_state:

        passive_runtime_state

    returns:

        viral_state_label
    """

    capsid = runtime_state.get(
        "capsid",
        0.0
    )

    viral_rna = runtime_state.get(
        "viral_RNA",
        0.0
    )

    viral_protein = runtime_state.get(
        "viral_protein",
        0.0
    )

    atp = runtime_state.get(
        "ATP",
        0.0
    )

    membrane = runtime_state.get(
        "cell_membrane",
        100.0
    )

    # =====================================
    # collapse
    # =====================================

    if atp <= 1.0:

        return COLLAPSE

    # =====================================
    # release
    # =====================================

    if (

        viral_protein >= 50.0
        and membrane <= 20.0

    ):

        return RELEASE

    # =====================================
    # assembly
    # =====================================

    if (

        viral_rna >= 50.0
        and viral_protein >= 20.0

    ):

        return ASSEMBLY

    # =====================================
    # replication
    # =====================================

    if viral_rna >= 10.0:

        return REPLICATION

    # =====================================
    # entry
    # =====================================

    if capsid > 0.0:

        return ENTRY

    # =====================================
    # stress
    # =====================================

    return STRESS

# =========================================
# helper
# =========================================

def build_viral_cycle_snapshot(

    runtime_state
):

    return {

        "capsid":

            runtime_state.get(
                "capsid",
                0.0
            ),

        "viral_RNA":

            runtime_state.get(
                "viral_RNA",
                0.0
            ),

        "viral_protein":

            runtime_state.get(
                "viral_protein",
                0.0
            ),

        "ATP":

            runtime_state.get(
                "ATP",
                0.0
            ),

        "cell_membrane":

            runtime_state.get(
                "cell_membrane",
                0.0
            )
    }
