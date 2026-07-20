# labelcenter/directed_effect_projection.py


def apply_directed_effects(
    cell
):

    events = []


    effects = list(
        cell.directed_effects
    )


    for effect in effects:

        result = apply_single_effect(

            cell,

            effect

        )


        if result:

            events.append(result)


    cell.directed_effects.clear()


    return events

def apply_single_effect(
    cell,
    effect
):

    operation = effect.get(
        "operation"
    )

    payload = effect.get(
        "payload",
        {}
    )

    # =========================
    # membrane damage
    # =========================

    if operation == "membrane_damage":

        strength = payload.get(
            "strength",
            0.0
        )

        old_value = (
            cell.runtime_state.get(
                "cell_membrane",
                0.0
            )
        )

        new_value = max(
            0.0,
            old_value - strength
        )

        cell.runtime_state.set(
            "cell_membrane",
            new_value
        )
        
        return {

            "type": "membrane_damage",

            "source": "perforin",

            "target": cell.id,

            "strength": strength

        }
        
    return None

def apply_world_directed_effects(
    world
):

    events = []

    for cell in world.cells.values():
    
        events.extend(
            apply_directed_effects(cell)
        )

    return events
