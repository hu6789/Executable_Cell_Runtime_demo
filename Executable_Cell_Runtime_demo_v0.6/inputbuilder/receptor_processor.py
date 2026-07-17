# inputbuilder/receptor_processor.py

from semantic.receptor_map import (
    SIGNAL_RECEPTOR_MAP
)
# =========================================
# receptor processing
# =========================================

def process_receptors(
    processed_inputs
):

    """
    grouped receptor processing

    determines:
        - receptor existence
        - receptor sensitivity
        - amplification
    """

    processed = {}

    for target_id, items in processed_inputs.items():

        processed[target_id] = []

        for item in items:

            result = apply_receptor_gate(
                item
            )

            if result is not None:

                processed[target_id].append(
                    result
                )

    return processed


# =========================================
# receptor gate
# =========================================

def apply_receptor_gate(
    item
):

    payload = item.get(
        "payload",
        {}
    )

    internal_signal = payload.get(
        "internal_signal"
    )

    receptor_name = (

        SIGNAL_RECEPTOR_MAP.get(
            internal_signal
        )
    )   

    # -------------------------------------
    # no receptor needed
    # -------------------------------------

    if receptor_name is None:

        return item

    # -------------------------------------
    # mock receptor expression
    # future:
    # pulled from cell state
    # -------------------------------------

    receptor_expression = 1.0

    # -------------------------------------
    # processed strength
    # -------------------------------------

    processed_strength = payload.get(
        "processed_strength",
        0.0
    )

    receptor_scaled = (

        processed_strength
        * receptor_expression
    )

    gated = dict(item)

    payload = dict(payload)

    payload["receptor"] = receptor_name

    payload["receptor_strength"] = (
        receptor_scaled
    )

    gated["payload"] = payload

    return gated
