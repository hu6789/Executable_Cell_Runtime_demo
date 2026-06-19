# cellmaster/scheduler/internal_trigger_builder.py

from cellmaster.scheduler.runtime_state_change_detector import (
    detect_runtime_state_changes
)


# =========================================
# build internal runtime triggers
# =========================================

def build_internal_triggers(
    world,
    runtime_records
):

    """
    convert runtime state changes into
    scheduler-compatible node_inputs
    """

    outputs = []

    for cell in world.cells.values():

        record = runtime_records.get(
            cell.id,
            {}
        )

        old_state = record.get(
            "last_runtime_state",
            {}
        )

        new_state = (
            cell.runtime_state.snapshot()
        )

        signals = detect_runtime_state_changes(

            old_state,
            new_state
        )

        if not signals:
            continue

        outputs.append({

            "target_id": cell.id,

            "node_inputs": signals
        })

    return outputs
    
