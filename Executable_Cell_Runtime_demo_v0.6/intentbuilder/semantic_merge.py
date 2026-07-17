# intent_builder/semantic_merge.py

from collections import defaultdict


# =========================================
# lightweight semantic merge
# =========================================

def semantic_merge(
    intents
):

    """
    lightweight semantic merge

    IntentBuilder merge is NOT
    authoritative aggregation.

    only merges:
        - identical semantic intents
        - same source/target/signal/tick
    """

    grouped = defaultdict(float)

    meta = {}

    passthrough = []

    for intent in intents:

        write_mode = intent.get(
            "write_mode"
        )

        # =================================
        # field merge
        # =================================

        if write_mode == "field":

            payload = intent.get(
                "payload",
                {}
            )

            position = payload.get("position")

            if position is None:
                position = ()

            key = (
                write_mode,
                intent.get("source_id"),
                payload.get("field_type"),
                tuple(position)
            )

            amount = payload.get(
                "amount",
                0.0
            )

            grouped[key] += amount

            meta[key] = {

                "write_mode": write_mode,

                "source_id": intent.get(
                    "source_id"
                ),

                "field_type": payload.get(
                    "field_type"
                ),

                "position": payload.get(
                    "position"
                )
            }

        # =================================
        # passthrough
        # =================================

        else:

            passthrough.append(
                intent
            )

    merged = []

    # -------------------------------------
    # rebuild merged field intents
    # -------------------------------------

    for key, amount in grouped.items():

        info = meta[key]

        merged.append({

            "write_mode": "field",

            "operation": "add",

            "source_id": info[
                "source_id"
            ],

            "payload": {

                "field_type": info[
                    "field_type"
                ],

                "position": info[
                    "position"
                ],

                "amount": amount
            }
        })

    # passthrough
    merged.extend(
        passthrough
    )

    return merged
