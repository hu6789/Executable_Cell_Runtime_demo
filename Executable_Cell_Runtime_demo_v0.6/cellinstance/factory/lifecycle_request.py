# cellinstance/factory/lifecycle_request.py


import uuid


# =========================================
# Lifecycle Request Builder
# =========================================

def build_spawn_request(
    runtime_entity,
    position=None,
    metadata=None
):

    """
    build lifecycle request
    for spawning a new runtime cell

    DOES NOT:
        - write into world
        - instantiate inside LabelCenter
        - perform scheduling

    RETURNS:
        request dict
    """

    if metadata is None:

        metadata = {}

    return {

        "request_id":
            str(uuid.uuid4()),

        "request_type":
            "entity_lifecycle",

        "operation":
            "spawn",

        "entity_type":
            "cell",

        "runtime_entity":
            runtime_entity,

        "position":
            position,

        "metadata":
            metadata
    }


# =========================================
# Remove Request
# =========================================

def build_remove_request(
    target_id,
    reason=None
):

    """
    build lifecycle remove request
    """

    return {

        "request_id":
            str(uuid.uuid4()),

        "request_type":
            "entity_lifecycle",

        "operation":
            "remove",

        "target_id":
            target_id,

        "reason":
            reason
    }


# =========================================
# Differentiate Request
# =========================================

def build_differentiation_request(
    source_id,
    target_template,
    preserve_state=True,
    extra_payload=None
):

    """
    request phenotype/template switch

    useful for:
        - differentiation
        - activation transition
        - exhaustion
        - infected conversion
    """

    if extra_payload is None:

        extra_payload = {}

    return {

        "request_id":
            str(uuid.uuid4()),

        "request_type":
            "entity_lifecycle",

        "operation":
            "differentiate",

        "source_id":
            source_id,

        "target_template":
            target_template,

        "preserve_state":
            preserve_state,

        "payload":
            extra_payload
    }


# =========================================
# Split / Divide Request
# =========================================

def build_division_request(
    parent_id,
    daughter_entities,
    metadata=None
):

    """
    build cell division request

    daughter_entities:
        list of runtime entities
    """

    if metadata is None:

        metadata = {}

    return {

        "request_id":
            str(uuid.uuid4()),

        "request_type":
            "entity_lifecycle",

        "operation":
            "divide",

        "parent_id":
            parent_id,

        "daughter_entities":
            daughter_entities,

        "metadata":
            metadata
    }
