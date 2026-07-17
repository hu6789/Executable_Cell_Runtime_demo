# aip/vml/infection_load.py


# =========================================
# Infection Load Estimator
# =========================================

def evaluate_infection_load(
    passive_runtime_state,
    viral_state_label=None
):

    viral_rna = (
        passive_runtime_state.get(
            "viral_RNA",
            0.0
        )
    )

    viral_protein = (
        passive_runtime_state.get(
            "viral_protein",
            0.0
        )
    )

    capsid = (
        passive_runtime_state.get(
            "capsid",
            0.0
        )
    )

    viral_particle = (
        passive_runtime_state.get(
            "viral_particle",
            0.0
        )
    )

    score = (

        viral_rna * 0.4 +

        viral_protein * 0.3 +

        capsid * 0.2 +

        viral_particle * 0.1
    )

    viral_load = min(
        score / 100.0,
        1.0
    )

    return {

        "viral_load":
            viral_load,

        "viral_RNA":
            viral_rna,

        "viral_protein":
            viral_protein,

        "capsid":
            capsid,

        "viral_particle":
            viral_particle,

        "viral_state":
            viral_state_label
    }
