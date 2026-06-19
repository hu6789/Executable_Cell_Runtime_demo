# substance/substance_master/request_generator.py


def generate_requests(

    substance_id,

    projected_effect
):

    """
    Convert projected effect
    into runtime requests.

    Returns:
        request list
    """

    effect_type = projected_effect.get(
        "effect_type"
    )

    target = projected_effect.get(
        "target"
    )

    amount = projected_effect.get(
        "amount",
        0.0
    )

    requests = []

    # ==========================
    # membrane damage
    # ==========================

    if effect_type == "membrane_damage":

        requests.append({

            "request_type":
                "targeted_directed",

            "operation":
                "membrane_damage",

            "source_id":
                substance_id,

            "target_id":
                target,

            "strength":
                amount
        })

    return requests
