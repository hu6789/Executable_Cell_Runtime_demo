# labelcenter/entity_apply.py

"""
Entity Apply Layer

LabelCenter entity write authority.

Responsibilities
----------------
- create runtime entities
- remove runtime entities
- transform runtime entities

DOES NOT
--------
- perform biological reasoning
- decide cell fate
- compile intents
- execute InternalNet
"""

# ==========================================================
# Public Entry
# ==========================================================

def apply_entity_updates(
    world,
    entity_requests
):
    """
    Apply entity write requests.

    Supported operations
    --------------------
    - create_cell
    - delete_entity
    - transform_entity
    """

    create_requests = []
    delete_requests = []
    transform_requests = []
    

    for request in entity_requests:

        operation = request.get("operation")

        if operation == "create":
            create_requests.append(request)

        elif operation == "delete":
            delete_requests.append(request)

        elif operation == "transform":
            transform_requests.append(request)

    _apply_transforms(
        world,
        transform_requests
    )

    _apply_deletes(
        world,
        delete_requests
    )

    _apply_creates(
        world,
        create_requests
    )


# ==========================================================
# Create
# ==========================================================

def _apply_creates(
    world,
    requests
):

    for request in requests:

        payload = request.get(
            "payload",
            {}
        )

        template_id = payload.get(
            "template_id"
        )

        if template_id is None:
            continue

        entity = (
            world.cell_factory.create_runtime_entity(

                template_id=template_id,

                cell_id=request.get(
                    "target_id"
                ),

                position=payload.get(
                    "position"
                )
            )
        )

        world.add_cell(entity)


# ==========================================================
# Delete
# ==========================================================

def _apply_deletes(
    world,
    requests
):

    for request in requests:

        target_id = request.get(
            "target_id"
        )

        if target_id is None:
            continue

        if target_id not in world.cells:
            continue

        world.remove_cell(target_id)


# ==========================================================
# Transform
# ==========================================================

def _apply_transforms(
    world,
    requests
):

    for request in requests:

        target_id = request.get(
            "target_id"
        )

        if target_id not in world.cells:
            continue

        payload = request.get(
            "payload",
            {}
        )

        cell = world.cells[target_id]

        new_type = payload.get(
            "new_type"
        )

        if new_type is not None:

            #
            # Temporary implementation.
            # Future differentiation pipeline
            # can replace this block.
            #

            cell.type = new_type
