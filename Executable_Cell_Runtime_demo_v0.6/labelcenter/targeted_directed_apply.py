# labelcenter/targeted_directed_apply.py


DEBUG = False


def debug_print(*args, **kwargs):

    if DEBUG:
        print(*args, **kwargs)


# =========================================
# apply targeted directed writes
# =========================================

def apply_targeted_directed_updates(
    world,
    intents
):

    """
    authoritative directed interaction apply

    examples:
        - perforin attack
        - FasL signaling
        - receptor injection
        - viral delivery
    """

    for intent in intents:

        apply_single_directed_write(
            world,
            intent
        )


# =========================================
# apply single directed write
# =========================================

def apply_single_directed_write(
    world,
    intent
):

    source_id = intent.get(
        "source_id"
    )

    target_id = intent.get(
        "target_id"
    )

    operation = intent.get(
        "operation"
    )

    payload = intent.get(
        "payload",
        {}
    )

    # -------------------------------------
    # validate
    # -------------------------------------

    if target_id not in world.cells:

        return

    target = world.cells[target_id]

    # -------------------------------------
    # init directed_effects
    # -------------------------------------

    if not hasattr(
        target,
        "directed_effects"
    ):

        target.directed_effects = []

    # -------------------------------------
    # register effect
    # -------------------------------------

    effect = {

        "source_id": source_id,

        "operation": operation,

        "payload": payload
    }

    target.directed_effects.append(
        effect
    )

    debug_print(

        f"[TargetedDirected] "

        f"{source_id} -> {target_id} "

        f"{operation}"
    )
