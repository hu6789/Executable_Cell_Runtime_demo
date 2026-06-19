# inputbuilder/node_input_standardizer.py


# =========================================
# standardize node inputs
# =========================================

def standardize_node_inputs(
    translated_inputs
):

    standardized = []

    for target_id, inputs in translated_inputs.items():

        node_input = build_node_input(

            target_id,
            inputs
        )

        standardized.append(
            node_input
        )

    return standardized


# =========================================
# build node input
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

        standardized = {

            "input_type": item.get(
                "input_type"
            ),

            "internal_signal": payload.get(
                "internal_signal"
            ),

            "strength": payload.get(

                "field_strength",

                payload.get(
                    "receptor_strength",

                    payload.get(
                        "processed_strength",
                        0.0
                    )
                )
            ),

            "source_id": item.get(
                "source_id"
            )
        }

        packaged.append(
            standardized
        )

    return {

        "target_id": target_id,

        "node_inputs": packaged
    }
