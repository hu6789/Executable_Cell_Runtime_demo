# labelcenter/directed_effect_projection.py


def apply_directed_effects(
    cell
):

    effects = list(
        cell.directed_effects
    )

    for effect in effects:

        apply_single_effect(
            cell,
            effect
        )

    cell.directed_effects.clear()


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

        print(

            "[DirectedEffect]",

            "cell_membrane",

            old_value,

            "->",

            new_value
        )
def apply_world_directed_effects(
    world
):

    for cell in world.cells.values():

        apply_directed_effects(
            cell
        )
