# substance/substance_dynamics/diffusion.py

import uuid


def diffuse_substance(

    entity,

    diffusion_fraction=0.2
):

    """
    Simple diffusion model

    parent keeps:
        (1-f)

    neighbors receive:
        f / 4
    """

    if not entity.active:

        return []

    if entity.amount <= 0:

        return []

    amount = entity.amount

    spread_amount = (
        amount * diffusion_fraction
    )

    remain_amount = (
        amount - spread_amount
    )

    entity.amount = remain_amount

    x, y = entity.position

    neighbor_amount = (
        spread_amount / 4.0
    )

    offspring = []

    for dx, dy in [

        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]:

        offspring.append({

            "substance_id":
                str(uuid.uuid4()),

            "substance_type":
                entity.substance_type,

            "position":
                (x + dx, y + dy),

            "amount":
                neighbor_amount
        })

    return offspring
