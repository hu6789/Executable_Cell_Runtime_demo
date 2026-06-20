# labelcenter/lifecycle_manager.py


# =========================================
# apply lifecycle writes
# =========================================

def apply_lifecycle_updates(
    world,
    lifecycle_intents
):

    """
    lifecycle authority:

        - add entity
        - remove entity
        - transform entity

    lifecycle_manager DOES NOT:
        - perform biology logic
        - build runtime physiology
        - interpret fate meaning
    """

    # -------------------------------------
    # phase ordering
    # -------------------------------------

    remove_intents = []
    add_intents = []
    transform_intents = []

    for intent in lifecycle_intents:

        operation = intent.get("operation")

        if operation == "remove":

            remove_intents.append(intent)

        elif operation == "add":

            add_intents.append(intent)

        elif operation == "transform":

            transform_intents.append(intent)

    # -------------------------------------
    # apply transform first
    # -------------------------------------

    apply_transforms(
        world,
        transform_intents
    )

    # -------------------------------------
    # apply remove
    # -------------------------------------

    apply_removals(
        world,
        remove_intents
    )

    # -------------------------------------
    # apply add
    # -------------------------------------

    apply_additions(
        world,
        add_intents
    )


# =========================================
# remove entities
# =========================================

def apply_removals(
    world,
    intents
):

    for intent in intents:

        target_id = intent.get(
            "target_id"
        )

        if not target_id:
            continue

        if target_id in world.cells:

            world.remove_cell(
                target_id
            )


# =========================================
# add entities
# =========================================

def apply_additions(
    world,
    intents
):

    for intent in intents:

        payload = intent.get(
            "payload",
            {}
        )

        # ----------------------
        # create runtime cell
        # ----------------------

        template_id = payload.get(
            "template_id"
        )

        if template_id:

            entity = (
                world.cell_factory
                .create_runtime_entity(
                    template_id=template_id,
                    cell_id=(
                        payload.get("cell_id")
                        or intent.get("target_id")
                    ),
                    position=payload.get(
                        "position"
                    )
                )
            )

            world.add_cell(entity)

            continue

        # ----------------------
        # legacy path
        # ----------------------

        entity = payload.get(
            "entity"
        )

        if entity is not None:

            world.add_cell(entity)


# =========================================
# transform entities
# =========================================

def apply_transforms(
    world,
    intents
):

    for intent in intents:

        target_id = intent.get(
            "target_id"
        )

        payload = intent.get(
            "payload",
            {}
        )

        new_type = payload.get(
            "new_type"
        )

        if not target_id:
            continue

        if target_id not in world.cells:
            continue

        if not new_type:
            continue

        cell = world.cells[target_id]

        # ---------------------------------
        # temporary simple transform
        # ---------------------------------

        cell.type = new_type
