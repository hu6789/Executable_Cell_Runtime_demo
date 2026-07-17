# substance/substance_spawn/spawn_from_field.py

from uuid import uuid4


def spawn_substances_from_field_intents(
    intents,
    substance_factory,
    world
):
    """
    Convert emit_field intents into runtime substances.

    Only field types that have a registered SubstanceTemplate
    will be instantiated as Runtime Substance entities.

    Returns
    -------
    list
        Newly created runtime substances.
    """

    spawned = []

    for intent in intents:

        if intent.get("write_mode") != "field":
            continue

        payload = intent.get("payload", {})
        
        source_id = intent.get("source_id")
 
        field_type = payload.get("field_type")

        if field_type is None:
            continue

        if field_type not in substance_factory.available_templates():
            continue

        position = payload.get("position")

        amount = payload.get("amount", 0.0)

        if amount is None:
            amount = intent.get("amount", 0.0)

        substance = substance_factory.create_runtime_entity(
            template_id=field_type,
            substance_id=f"{field_type}_{uuid4().hex[:8]}",
            position=position,
            amount=amount,
            source_id=source_id
        )
        

        world.add_substance(substance)

        spawned.append(substance)

    return spawned
