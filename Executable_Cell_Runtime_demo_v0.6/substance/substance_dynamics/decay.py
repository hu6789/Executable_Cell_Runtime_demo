# substance/substance_dynamics/decay.py

def decay_substance(

    entity,

    decay_fraction=0.05
):

    """
    simple first-order decay

    amount(t+1)
        =
    amount(t)
        *
    (1-decay_fraction)
    """

    if not entity.active:

        return

    if entity.amount <= 0:

        return

    entity.amount *= (

        1.0 - decay_fraction
    )

    if entity.amount <= 0:

        entity.amount = 0.0

        entity.active = False
