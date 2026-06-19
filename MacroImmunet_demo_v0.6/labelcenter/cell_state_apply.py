# labelcenter/cell_state_apply.py

from labelcenter.write_aggregator import (
    aggregate_cell_state
)


# =========================================
# apply cell state updates
# =========================================

def apply_cell_state_updates(
    world,
    intents
):

    """
    authoritative runtime state patch apply

    LabelCenter does NOT:
        - recompute physiology
        - run graph
        - execute behavior

    only applies finalized state writes
    """

    aggregated = aggregate_cell_state(
        intents
    )

    print(

        f"[CellState] aggregated writes: "

        f"{len(aggregated)}"
    )

    for write in aggregated:

        apply_single_state_write(
            world,
            write
        )


# =========================================
# apply single write
# =========================================
def apply_single_state_write(
    world,
    write
):

    target_id = write.get(
        "target_id"
    )

    state = write.get(
        "state"
    )

    if target_id not in world.cells:
        return

    cell = world.cells[target_id]

    old = getattr(
        cell,
        "cell_state",
        None
    )

    cell.cell_state = state

    print(

        f"[CellState] "

        f"{target_id} "

        f"{old} -> {state}"
    )
