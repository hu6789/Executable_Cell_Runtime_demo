# inputbuilder/field_processor.py


# =========================================
# field perception processing
# =========================================

def process_field_inputs(
    processed_inputs
):

    """
    grouped field processing

    includes:
        - exposure weighting
        - gradient estimation
        - accumulation
    """

    processed = {}

    for target_id, items in processed_inputs.items():

        processed[target_id] = []

        for item in items:

            payload = item.get(
                "payload",
                {}
            )

            interaction_mode = item.get(
                "interaction_mode"
            )

            # ---------------------------------
            # non-field passthrough
            # ---------------------------------

            if interaction_mode != "field":

                processed[target_id].append(
                    item
                )

                continue

            result = process_single_field(
                item
            )

            if result is not None:

                processed[target_id].append(
                    result
                )

    return processed


# =========================================
# process single field
# =========================================

def process_single_field(
    item
):

    payload = item.get(
        "payload",
        {}
    )

    receptor_strength = payload.get(
        "receptor_strength",
        0.0
    )

    # -------------------------------------
    # accumulation
    # -------------------------------------

    accumulated = min(

        receptor_strength * 1.2,
        1.0
    )

    updated = dict(item)

    payload = dict(payload)

    payload["field_strength"] = (
        accumulated
    )

    # -------------------------------------
    # simple gradient estimate
    # -------------------------------------

    payload["gradient_detected"] = (
        accumulated > 0.3
    )

    updated["payload"] = payload

    return updated
