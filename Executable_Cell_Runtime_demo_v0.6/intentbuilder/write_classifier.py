# intent_builder/write_classifier.py


# =========================================
# classify write mode
# =========================================

def classify_write_mode(
    request
):

    """
    runtime request
    →
    world write mode
    """

    request_type = request.get(
        "request_type"
    )

    # =====================================
    # field
    # =====================================

    if request_type == "field":

        return "field"

    # =====================================
    # cell_state
    # =====================================

    elif request_type == "cell_state":

        return "cell_state"

    # =====================================
    # runtime_state
    # =====================================

    elif request_type == "runtime_state":

        return "runtime_state"

    # =====================================
    # label_flag
    # =====================================

    elif request_type == "label_flag":

        return "label_flag"

    # =====================================
    # targeted_directed
    # =====================================

    elif request_type == "targeted_directed":

        return "targeted_directed"

    # =====================================
    # link
    # =====================================

    elif request_type == "link":

        return "link"

    # =====================================
    # lifecycle
    # =====================================

    elif request_type == "entity_lifecycle":

        return "entity_lifecycle"

    # =====================================
    # unknown
    # =====================================

    return "unknown"
