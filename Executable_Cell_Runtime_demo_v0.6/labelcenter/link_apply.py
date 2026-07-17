# labelcenter/link_apply.py


# =========================================
# apply link updates
# =========================================

def apply_link_updates(
    world,
    intents
):

    """
    authoritative topology relation apply

    examples:
        - immune synapse
        - receptor binding
        - viral attachment
        - persistent adhesion
    """

    print(

        f"[Link] writes={len(intents)}"
    )

    for intent in intents:

        apply_single_link(
            world,
            intent
        )


# =========================================
# apply single link
# =========================================

def apply_single_link(
    world,
    intent
):

    operation = intent.get(
        "operation"
    )

    source_id = intent.get(
        "source_id"
    )

    target_id = intent.get(
        "target_id"
    )

    payload = intent.get(
        "payload",
        {}
    )

    # -------------------------------------
    # init world links
    # -------------------------------------

    if not hasattr(
        world,
        "links"
    ):

        world.links = []

    # -------------------------------------
    # add link
    # -------------------------------------

    if operation == "add":

        link = {

            "source_id": source_id,

            "target_id": target_id,

            "link_type": payload.get(
                "link_type"
            ),

            "strength": payload.get(
                "strength",
                1.0
            ),

            "tick_created": payload.get(
                "tick_created"
            )
        }

        world.links.append(link)

        print(

            f"[Link] ADD "

            f"{source_id} -> {target_id}"
        )

    # -------------------------------------
    # remove link
    # -------------------------------------

    elif operation == "remove":

        retained = []

        removed = 0

        for link in world.links:

            same = (

                link.get("source_id")
                == source_id

                and

                link.get("target_id")
                == target_id
            )

            if same:

                removed += 1

            else:

                retained.append(link)

        world.links = retained

        print(

            f"[Link] REMOVE "

            f"{source_id} -> {target_id} "

            f"removed={removed}"
        )
