# intent_builder/intent_standardizer.py

import uuid

from intentbuilder.write_classifier import (
    classify_write_mode
)

# =========================================
# standardize intent
# =========================================

def standardize_intent(request):

    request_type = request.get(
        "request_type"
    )

    # =====================================
    # field
    # =====================================

    if request_type == "field":

        return build_field_intent(
            request
        )

    # =====================================
    # cell state
    # =====================================

    elif request_type == "cell_state":

        return build_cell_state_intent(
            request
        )
        
    # =====================================
    # cell state
    # =====================================
    
    elif request_type == "runtime_state":

        return build_runtime_state_intent(
            request
        )
    
    # =====================================
    # label flag
    # =====================================

    elif request_type == "label_flag":

        return build_label_flag_intent(
            request
        )

    # =====================================
    # targeted directed
    # =====================================

    elif request_type == "targeted_directed":

        return build_targeted_directed_intent(
            request
        )

    # =====================================
    # link
    # =====================================

    elif request_type == "link":

        return build_link_intent(
            request
        )

    # =====================================
    # lifecycle
    # =====================================

    elif request_type == "entity_lifecycle":

        return build_lifecycle_intent(
            request
        )

    return None


# =========================================
# field intent
# =========================================

def build_field_intent(request):

    return {

        "intent_id": str(uuid.uuid4()),

        "write_mode": "field",

        "operation": "add",

        "source_id": request.get(
            "source_id"
        ),

        "payload": {

            "field_type": request.get(
                "translated_signal"
            ),

            "position": request.get(
                "position"
            ),

            "amount": request.get(
                "scaled_strength",
                0.0
            )
        }
    }

# =========================================
# lifecycle intent
# =========================================

def build_lifecycle_intent(request):

    return {

        "intent_id": str(uuid.uuid4()),

        "write_mode": "entity_lifecycle",

        "operation": request.get(
            "operation"
        ),

        "target_id": request.get(
            "target_id"
        ),

        "payload": request.get(
            "payload",
            {}
        )
    }
    
# =========================================
# cell state
# ========================================= 
def build_cell_state_intent(request):

    return {

        "intent_id": str(uuid.uuid4()),

        "write_mode": "cell_state",

        "operation": "add",

        "target_id": request.get(
            "target_id"
        ),

        "payload": request.get(
            "payload",
            {}
        )
    }
  
# =========================================
# runtime state
# =========================================   
def build_runtime_state_intent(request):

    return {

        "intent_id":
            str(uuid.uuid4()),

        "write_mode":
            "runtime_state",

        "operation":
            "set",

        "target_id":
            request.get(
                "target_id"
            ),

        "payload":
            request.get(
                "payload",
                {}
            )
    }
    
# =========================================
# label flag
# =========================================
def build_label_flag_intent(request):

    return {

        "intent_id": str(uuid.uuid4()),

        "write_mode": "label_flag",

        "operation": "set",

        "target_id": request.get(
            "target_id"
        ),

        "payload": {

            "label": request.get(
                "label"
            ),

            "value": request.get(
                "value"
            )
        }
    }
# =========================================
# targeted directed
# =========================================
def build_targeted_directed_intent(
    request
):

    payload = dict(

        request.get(
            "payload",
            {}
        )
    )

    if "strength" in request:

        payload["strength"] = (

            request["strength"]
        )

    return {

        "intent_id":
            str(uuid.uuid4()),

        "write_mode":
            "targeted_directed",

        "operation":
            request.get(
                "operation",
                "directed_effect"
            ),

        "source_id":
            request.get(
                "source_id"
            ),

        "target_id":
            request.get(
                "target_id"
            ),

        "payload":
            payload
    }
# =========================================
# link
# =========================================
def build_link_intent(request):

    return {

        "intent_id": str(uuid.uuid4()),

        "write_mode": "link",

        "operation": request.get(
            "operation",
            "add"
        ),

        "source_id": request.get(
            "source_id"
        ),

        "target_id": request.get(
            "target_id"
        ),

        "payload": request.get(
            "payload",
            {}
        )
    }
