# inputbuilder/node_input_standardizer.py

# =========================================
# Standardize Node Inputs
# =========================================

def standardize_node_inputs(
    translated_inputs
):

    standardized = []

    for target_id, inputs in translated_inputs.items():

        standardized.append(

            build_node_input(
                target_id,
                inputs
            )
        )

    return standardized


# =========================================
# Build Node Input
# =========================================

def build_node_input(
    target_id,
    inputs
):

    packaged = []

    for item in inputs:

        payload = item.get(
            "payload",
            {}
        )

        strength = (
            payload.get(
                "field_strength",

                payload.get(
                    "strength",

                    payload.get(
                        "processed_strength",

                        payload.get(
                            "receptor_strength",
                            0.0
                        )
                    )
                )
            )
        )

        packaged.append({

            "input_type":
                item.get(
                    "input_type"
                ),

            "internal_signal":
                payload.get(
                    "internal_signal"
                ),

            "strength":
                strength,

            "source_id":
                item.get(
                    "source_id"
                )
        })

    return {

        "target_id":
            target_id,

        "node_inputs":
            packaged
    }
