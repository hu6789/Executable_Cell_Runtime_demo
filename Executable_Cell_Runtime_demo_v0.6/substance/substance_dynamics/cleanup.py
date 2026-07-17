# substance/substance_dynamics/cleanup.py


def cleanup_substances(
    substances
):

    """
    remove inactive substances
    """

    alive = []

    removed = []

    for entity in substances:

        if not entity.active:

            removed.append(
                entity
            )

            continue

        if entity.amount <= 0:

            removed.append(
                entity
            )

            continue

        alive.append(
            entity
        )

    return {

        "alive":
            alive,

        "removed":
            removed
    }
