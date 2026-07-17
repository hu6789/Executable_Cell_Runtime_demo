# intent_builder/value_scaler.py


# =========================================
# scale runtime request values
# =========================================

def scale_request_values(
    request
):

    """
    convert internal runtime magnitude
    into world magnitude
    """

    request_type = request.get(
        "request_type"
    )

    scaled = dict(request)

    # =====================================
    # field scaling
    # =====================================

    if request_type == "field":

        scale_field_request(
            scaled
        )

    # =====================================
    # targeted_directed
    # =====================================

    elif request_type == "targeted_directed":

        scale_directed_request(
            scaled
        )

    return scaled


# =========================================
# field scaling
# =========================================

def scale_field_request(request):

    strength = request.get(
        "strength",
        0.0
    )

    payload = request.get(
        "payload",
        {}
    )

    amount = payload.get(
        "amount",
        1.0
    )

    request["scaled_strength"] = (
        strength * amount
    )


# =========================================
# directed scaling
# =========================================

def scale_directed_request(
    request
):

    strength = request.get(
        "strength",
        0.0
    )

    request["scaled_strength"] = (
        strength
    )
