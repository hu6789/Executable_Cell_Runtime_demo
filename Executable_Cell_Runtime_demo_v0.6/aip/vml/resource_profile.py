# aip/vml/resource_profile.py


def evaluate_resource_profile(
    runtime_state,
    infection_load
):

    atp = runtime_state.get(
        "ATP",
        0.0
    )

    membrane = runtime_state.get(
        "cell_membrane",
        0.0
    )

    translation_capacity = (
        atp / 100.0
    )

    membrane_capacity = (
        membrane / 100.0
    )

    metabolic_capacity = (
        atp / 100.0
    )

    resource_limit = min(

        translation_capacity,

        membrane_capacity,

        metabolic_capacity
    )

    return {

        "translation_capacity":
            translation_capacity,

        "membrane_capacity":
            membrane_capacity,

        "metabolic_capacity":
            metabolic_capacity,

        "resource_limit":
            resource_limit
    }
