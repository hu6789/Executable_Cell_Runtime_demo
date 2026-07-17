# labelcenter/runtime_state_apply.py

from labelcenter.write_aggregator import (
    aggregate_runtime_state
)

DEBUG = False


def debug_print(*args, **kwargs):

    if DEBUG:
        print(*args, **kwargs)


# =========================================
# apply runtime state updates
# =========================================

def apply_runtime_state_updates(
    world,
    intents
):

    aggregated = aggregate_runtime_state(
        intents
    )

    debug_print(

        f"[RuntimeState] aggregated writes: "

        f"{len(aggregated)}"
    )

    for write in aggregated:

        apply_single_runtime_write(
            world,
            write
        )


# =========================================
# apply single write
# =========================================

def apply_single_runtime_write(
    world,
    write
):

    target_id = write.get(
        "target_id"
    )

    payload = write.get(
        "payload",
        {}
    )

    if target_id not in world.cells:
        return

    cell = world.cells[target_id]

    for node_name, value in payload.items():

        cell.runtime_state.set(
            node_name,
            value
        )

    debug_print(

        f"[RuntimeState] "

        f"{target_id} "

        f"updated {len(payload)} nodes"
    )
