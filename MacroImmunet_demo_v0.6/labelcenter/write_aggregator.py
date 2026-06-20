# labelcenter/write_aggregator.py

from collections import defaultdict


# =========================================
# aggregate intents
# =========================================

def aggregate_intents(write_mode, intents):

    if write_mode == "cell_state":
        return aggregate_cell_state(intents)

    elif write_mode == "label_flag":
        return aggregate_label_flags(intents)

    elif write_mode == "field":
        return aggregate_fields(intents)

    elif write_mode == "entity_lifecycle":
        return aggregate_lifecycle(intents)
    
    elif write_mode == "runtime_state":
        return aggregate_runtime_state(intents)

    else:
        return intents


# =========================================
# cell_state aggregation
# =========================================

def aggregate_cell_state(intents):

    merged = {}

    for intent in intents:

        target_id = intent.get(
            "target_id"
        )

        payload = intent.get(
            "payload",
            {}
        )

        state = payload.get(
            "state"
        )

        if not target_id or not state:
            continue

        merged[target_id] = state

    aggregated = []

    for target_id, state in merged.items():

        aggregated.append({

            "target_id": target_id,

            "state": state
        })

    return aggregated


# =========================================
# runtime_state aggregation
# =========================================

def aggregate_runtime_state(
    intents
):

    merged = {}

    for intent in intents:

        target_id = intent.get(
            "target_id"
        )

        payload = intent.get(
            "payload",
            {}
        )

        if not target_id:
            continue

        merged[target_id] = payload

    aggregated = []

    for target_id, payload in merged.items():

        aggregated.append({

            "target_id":
                target_id,

            "payload":
                payload
        })

    return aggregated

# =========================================
# label_flag aggregation
# =========================================

def aggregate_label_flags(intents):

    merged = {}

    for intent in intents:

        target_id = intent.get("target_id")

        payload = intent.get("payload", {})

        label = payload.get("label")

        value = payload.get("value")

        if not target_id or not label:
            continue

        key = (target_id, label)

        merged[key] = value

    aggregated = []

    for (target_id, label), value in merged.items():

        aggregated.append({

            "target_id": target_id,

            "label": label,

            "value": value
        })

    return aggregated


# =========================================
# field aggregation
# =========================================

def aggregate_fields(intents):

    acc = defaultdict(float)

    meta = {}

    for intent in intents:

        payload = intent.get("payload", {})

        field_type = payload.get("field_type")

        position = payload.get("position")

        amount = payload.get("amount")

        if amount is None:
            amount = payload.get("strength", 0.0)
 
        if not field_type or position is None:
            continue

        key = (
            field_type,
            tuple(position)
        )

        acc[key] += amount

        meta[key] = {
            "field_type": field_type,
            "position": tuple(position)
        }

    aggregated = []

    for key, value in acc.items():

        info = meta[key]

        aggregated.append({

            "field_type": info["field_type"],

            "position": info["position"],

            "amount": value
        })

    return aggregated


# =========================================
# lifecycle aggregation
# =========================================

def aggregate_lifecycle(intents):

    # lifecycle 不建议强聚合
    # 先保持原样

    return intents
