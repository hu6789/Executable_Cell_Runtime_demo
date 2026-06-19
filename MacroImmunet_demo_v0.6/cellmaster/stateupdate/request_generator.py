# cellmaster/stateupdate/request_generator.py

# =========================================
# Secreted Signal Request
# =========================================

def build_secreted_signal_request(
    signal,
    cell
):

    signal_type = signal.get(
        "signal_type"
    )

    if signal_type is None:

        return None

    strength = signal.get(
        "strength",
        0.0
    )

    return {

        "request_type":
            "field",

        "signal":
            signal_type,

        "source_id":
            cell.id,

        "position":
            cell.position,

        "strength":
            strength
    }
# =========================================
# state requests
# =========================================

def build_exposure_requests(
    public_exposure,
    runtime_context,
    cell,
    tick=None
):

    requests = []

    # =====================================
    # exposure-derived field requests
    # =====================================

    secreted_signals = public_exposure.get(
        "secreted_signals",
        []
    )

    for signal in secreted_signals:

        request = (
            build_secreted_signal_request(
                signal,
                cell
            )
        )

        if request is not None:

            requests.append(
                request
            )

    # =====================================
    # behavior generated requests
    # =====================================

    requests.extend(

        runtime_context.get(
            "external_requests",
            []
        )
    )

    # =====================================
    # state projection requests
    # =====================================

    requests.extend(

        build_state_requests(
            runtime_context,
            cell
        )
    )

    # =====================================
    # label projection requests
    # =====================================

    requests.extend(

        build_label_requests(
            runtime_context,
            cell
        )
    )

    # =====================================
    # lifecycle projection requests
    # =====================================

    requests.extend(

        build_lifecycle_requests(
            runtime_context,
            cell
        )
    )
    
    # =====================================
    # runtime state requests
    # =====================================
    
    requests.extend(
        build_runtime_state_requests(
            runtime_context,
            cell
        )
    )

    return requests
        
# =========================================
# runtime state 
# =========================================
    
def build_runtime_state_requests(
    runtime_context,
    cell
):

    projected = runtime_context.get(
        "projected_runtime_state",
        {}
    )

    if not projected:
        return []

    return [{

        "request_type":
            "runtime_state",

        "target_id":
            cell.id,

        "payload":
            projected
    }]




# =========================================
# label requests
# =========================================

def build_label_requests(
    runtime_context,
    cell
):

    requests = []

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    if runtime_labels.get(
        "infected",
        False
    ):

        requests.append({

            "request_type":
                "label_flag",

            "target_id":
                cell.id,

            "label":
                "infected",

            "value":
                True
        })

    return requests


# =========================================
# lifecycle requests
# =========================================

def build_lifecycle_requests(
    runtime_context,
    cell
):

    requests = []

    fate = (

        runtime_context
        .get(
            "fate_progression",
            {}
        )
        .get(
            "current_fate"
        )
    )

    if fate == "dead":

        requests.append({

            "request_type":
                "entity_lifecycle",

            "operation":
                "remove",

            "target_id":
                cell.id
        })

    return requests
# =========================================
# state requests
# =========================================

def build_state_requests(
    runtime_context,
    cell
):

    requests = []

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    if runtime_labels.get(
        "activated",
        False
    ):

        requests.append({

            "request_type":
                "cell_state",

            "target_id":
                cell.id,

            "payload": {

                "state":
                    "activated"
            }
        })
    return requests
