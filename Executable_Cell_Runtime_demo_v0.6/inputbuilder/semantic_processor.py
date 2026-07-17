# inputbuilder/semantic_processor.py

import math


# =========================================
# semantic processing
# =========================================

def process_semantics(
    translated_inputs
):

    """
    grouped semantic processing

    input:
        {
            target_id: [...]
        }
    """

    processed = {}

    for target_id, inputs in translated_inputs.items():

        processed[target_id] = []

        for item in inputs:

            result = process_single_input(
                item
            )

            if result is not None:

                processed[target_id].append(
                    result
                )

    return processed


# =========================================
# single input processing
# =========================================

def process_single_input(
    item
):

    payload = item.get(
        "payload",
        {}
    )

    strength = payload.get(
        "strength",
        0.0
    )

    distance = payload.get(
        "distance",
        0.0
    )

    # -------------------------------------
    # distance attenuation
    # -------------------------------------

    attenuated = apply_distance_decay(

        strength,
        distance
    )

    # -------------------------------------
    # threshold
    # -------------------------------------

    if attenuated < 0.01:

        return None

    # -------------------------------------
    # saturation
    # -------------------------------------

    normalized = min(
        attenuated,
        1.0
    )

    processed = dict(item)

    payload = dict(payload)

    payload["processed_strength"] = (
        normalized
    )

    processed["payload"] = payload

    return processed


# =========================================
# exponential decay
# =========================================

def apply_distance_decay(
    strength,
    distance
):

    decay = math.exp(
        -distance * 0.5
    )

    return strength * decay
