# intent_builder/request_collector.py


# =========================================
# collect runtime requests
# =========================================

def collect_requests(
    request_queue,
    incoming_requests
):

    """
    request intake layer

    responsibilities:
        - validate minimal request schema
        - reject malformed requests
        - append valid requests

    does NOT:
        - perform semantic translation
        - scale values
        - classify write modes
    """

    if not incoming_requests:

        return []

    accepted = []

    rejected = []

    for request in incoming_requests:

        if validate_request(request):

            request_queue.append(request)

            accepted.append(request)

        else:

            rejected.append(request)

    return {

        "accepted": accepted,

        "rejected": rejected
    }


# =========================================
# minimal request validation
# =========================================

def validate_request(
    request
):

    """
    minimal runtime request validation
    """

    if not isinstance(request, dict):

        return False

    request_type = request.get(
        "request_type"
    )

    if request_type is None:

        return False

    # -------------------------------------
    # field request
    # -------------------------------------

    if request_type == "field":

        required = [

            "signal",
            "source_id",
            "position"
        ]

        return check_required(
            request,
            required
        )

    # -------------------------------------
    # cell_state
    # -------------------------------------

    elif request_type == "cell_state":

        required = [

            "target_id",
            "payload"
        ]

        return check_required(
            request,
            required
        )
        
    # -------------------------------------
    # runtime_state
    # -------------------------------------

    elif request_type == "runtime_state":

        required = [

            "target_id",
            "payload"
        ]

        return check_required(
            request,
            required
        )
        
    # -------------------------------------
    # label_flag
    # -------------------------------------

    elif request_type == "label_flag":

        required = [

            "target_id",
            "label",
            "value"
        ]

        return check_required(
            request,
            required
        )

    # -------------------------------------
    # targeted_directed
    # -------------------------------------

    elif request_type == "targeted_directed":

        required = [

            "source_id",
            "target_id",
            "operation"
        ]

        return check_required(
            request,
            required
        )

    # -------------------------------------
    # link
    # -------------------------------------

    elif request_type == "link":

        required = [

            "source_id",
            "target_id",
            "operation"
        ]

        return check_required(
            request,
            required
        )

    # -------------------------------------
    # lifecycle request
    # -------------------------------------

    elif request_type == "entity_lifecycle":

        required = [

            "operation"
        ]

        return check_required(
            request,
            required
        )

    # -------------------------------------
    # unknown type
    # -------------------------------------

    return False
# =========================================
# required key checker
# =========================================

def check_required(
    data,
    required_keys
):

    for key in required_keys:

        if key not in data:

            return False

    return True
