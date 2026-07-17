# inputbuilder/interaction_request_builder.py

import uuid


# =========================================
# build interaction requests
# =========================================

def build_interaction_requests(
    standardized_inputs
):

    """
    convert standardized node inputs
    into interaction requests
    for substance master / external systems

    examples:
        - cytokine uptake
        - receptor binding
        - viral attachment
        - antibody neutralization
    """

    requests = []

    for node_input in standardized_inputs:

        built = build_single_request(
            node_input
        )

        if built is not None:

            requests.append(
                built
            )

    return requests


# =========================================
# build single request
# =========================================

def build_single_request(
    node_input
):

    interaction_mode = node_input.get(
        "interaction_mode"
    )

    payload = node_input.get(
        "payload",
        {}
    )

    # =====================================
    # field exposure
    # =====================================

    if interaction_mode == "field":

        return {

            "request_id": str(
                uuid.uuid4()
            ),

            "request_type": "field_interaction",

            "target_id": node_input.get(
                "target_id"
            ),

            "signal": payload.get(
                "translated_signal"
            ),

            "strength": payload.get(
                "weighted_strength",
                0.0
            ),

            "payload": {

                "concentration": payload.get(
                    "concentration",
                    0.0
                ),

                "distance": payload.get(
                    "distance"
                )
            }
        }

    # =====================================
    # contact interaction
    # =====================================

    elif interaction_mode == "contact":

        return {

            "request_id": str(
                uuid.uuid4()
            ),

            "request_type": "contact_interaction",

            "source_id": node_input.get(
                "source_id"
            ),

            "target_id": node_input.get(
                "target_id"
            ),

            "payload": {

                "distance": payload.get(
                    "distance"
                ),

                "translated_signal": payload.get(
                    "translated_signal"
                )
            }
        }

    # =====================================
    # binding interaction
    # =====================================

    elif interaction_mode == "binding":

        return {

            "request_id": str(
                uuid.uuid4()
            ),

            "request_type": "binding_interaction",

            "source_id": node_input.get(
                "source_id"
            ),

            "target_id": node_input.get(
                "target_id"
            ),

            "payload": {

                "binding_affinity": payload.get(
                    "binding_affinity",
                    0.0
                ),

                "translated_signal": payload.get(
                    "translated_signal"
                )
            }
        }

    # =====================================
    # directed interaction
    # =====================================

    elif interaction_mode == "directed":

        return {

            "request_id": str(
                uuid.uuid4()
            ),

            "request_type": "directed_interaction",

            "source_id": node_input.get(
                "source_id"
            ),

            "target_id": node_input.get(
                "target_id"
            ),

            "payload": {

                "damage": payload.get(
                    "damage",
                    0.0
                ),

                "translated_signal": payload.get(
                    "translated_signal"
                )
            }
        }

    # =====================================
    # persistent interaction
    # =====================================

    elif interaction_mode == "persistent":

        return {

            "request_id": str(
                uuid.uuid4()
            ),

            "request_type": "persistent_interaction",

            "source_id": node_input.get(
                "source_id"
            ),

            "target_id": node_input.get(
                "target_id"
            ),

            "payload": {

                "duration": payload.get(
                    "duration",
                    0
                ),

                "translated_signal": payload.get(
                    "translated_signal"
                )
            }
        }

    return None
