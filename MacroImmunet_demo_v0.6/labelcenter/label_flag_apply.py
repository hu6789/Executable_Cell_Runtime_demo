# labelcenter/label_flag_apply.py

from labelcenter.write_aggregator import (
    aggregate_label_flags
)


# =========================================
# apply label flags
# =========================================

def apply_label_flag_updates(
    world,
    intents
):

    """
    authoritative outward label apply

    label_flag is world-visible state
    readable by:
        - ScanMaster
        - receptor interaction
        - immune recognition
    """

    aggregated = aggregate_label_flags(
        intents
    )

    print(

        f"[LabelFlag] aggregated writes: "

        f"{len(aggregated)}"
    )

    for write in aggregated:

        apply_single_label_write(
            world,
            write
        )


# =========================================
# apply single label
# =========================================

def apply_single_label_write(
    world,
    write
):

    target_id = write.get(
        "target_id"
    )

    label = write.get(
        "label"
    )

    value = write.get(
        "value"
    )

    # -------------------------------------
    # validate
    # -------------------------------------

    if target_id not in world.cells:

        return

    cell = world.cells[target_id]

    # -------------------------------------
    # init label flags
    # -------------------------------------

    if not hasattr(
        cell,
        "label_flags"
    ):

        cell.label_flags = {}

    # -------------------------------------
    # apply label
    # -------------------------------------

    old = cell.label_flags.get(
        label
    )

    cell.label_flags[label] = value

    print(

        f"[LabelFlag] "

        f"{target_id} "

        f"{label}: "

        f"{old} -> {value}"
    )
