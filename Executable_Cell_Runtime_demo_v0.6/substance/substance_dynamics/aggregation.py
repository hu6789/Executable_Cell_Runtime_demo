# substance/substance_dynamics/aggregation.py

from collections import defaultdict


def aggregate_substances(
    substances
):

    """
    merge substances with

    same type
    +
    same position
    """

    groups = defaultdict(list)

    for entity in substances:

        key = (

            entity.substance_type,

            entity.position
        )

        groups[key].append(
            entity
        )

    survivors = []

    removed = []

    for entities in groups.values():

        if len(entities) == 1:

            survivors.append(
                entities[0]
            )

            continue

        primary = entities[0]

        total_amount = sum(

            e.amount

            for e in entities
        )

        primary.amount = (
            total_amount
        )

        survivors.append(
            primary
        )

        removed.extend(
            entities[1:]
        )

    return {

        "survivors":
            survivors,

        "removed":
            removed
    }
