# labelcenter/write_aggregator.py

from collections import defaultdict


# ==========================================================
# LabelCenter Write Aggregator v0.7
# ==========================================================

"""
Responsibilities
----------------
Aggregate intents before apply.

Only write modes that benefit from aggregation are merged.

DOES NOT
--------
- execute writes
- modify world
- validate intents
"""


# ==========================================================
# Dispatcher
# ==========================================================

def aggregate_intents(write_mode, intents):

    if write_mode == "runtime_state":
        return aggregate_runtime_state(intents)

    elif write_mode == "field":
        return aggregate_fields(intents)

    elif write_mode == "entity":
        return aggregate_entity(intents)

    elif write_mode == "substance":
        return aggregate_substance(intents)

    else:
        # targeted_directed / link / event ...
        return intents


# ==========================================================
# Runtime State
# ==========================================================

def aggregate_runtime_state(intents):

    merged = {}

    for intent in intents:

        target_id = intent.get("target_id")

        if target_id is None:
            continue

        merged[target_id] = intent

    return list(merged.values())


# ==========================================================
# Field
# ==========================================================

def aggregate_fields(intents):

    accumulator = defaultdict(float)

    metadata = {}

    for intent in intents:

        payload = intent.get(
            "payload",
            {}
        )

        field_type = payload.get(
            "field_type"
        )

        position = payload.get(
            "position"
        )

        if field_type is None or position is None:
            continue

        amount = payload.get(
            "amount",
            payload.get(
                "strength",
                intent.get(
                    "strength",
                    0.0
                )
            )
        )

        key = (
            field_type,
            tuple(position)
        )

        accumulator[key] += amount

        metadata[key] = {
            "field_type": field_type,
            "position": tuple(position),
            "radius": payload.get("radius"),
            "region": payload.get("region")
        }

    aggregated = []

    for key, value in accumulator.items():

        info = metadata[key]

        aggregated.append({

            "operation": "emit_field",

            "write_mode": "field",

            "target_type": "field",

            "target_id": info["field_type"],

            "field_type": info["field_type"],

            "position": info["position"],

            "radius": info["radius"],

            "region": info["region"],

            "amount": value

        })

    return aggregated

# ==========================================================
# Entity
# ==========================================================

def aggregate_entity(intents):

    """
    Entity lifecycle should preserve ordering.

    Do NOT merge.
    """

    return intents


# ==========================================================
# Substance
# ==========================================================

def aggregate_substance(intents):

    """
    Substance spawn requests are currently not merged.

    Future:
        identical spawn at same location
        can be merged.
    """

    return intents
