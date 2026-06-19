# cellmaster/scheduler/eligibility.py


# =========================================
# runtime eligibility
# =========================================

def check_runtime_eligibility(
    runtime_context,
    world,
    runtime_records
):

    """
    hard runtime gating

    determines whether a cell
    is allowed to enter runtime
    pipeline this tick.
    """

    cell_id = runtime_context.get(
        "cell_id"
    )

    # -------------------------------------
    # cell existence
    # -------------------------------------

    cell = world.cells.get(
        cell_id
    )

    if cell is None:

        return False

    # -------------------------------------
    # removed / dead
    # -------------------------------------

    if getattr(
        cell,
        "removed",
        False
    ):

        return False

    if getattr(
        cell,
        "dead",
        False
    ):

        return False

    # -------------------------------------
    # runtime disabled
    # -------------------------------------

    runtime_disabled = getattr(
        cell,
        "runtime_disabled",
        False
    )

    if runtime_disabled:

        return False

    # -------------------------------------
    # hard cooldown
    # -------------------------------------

    runtime_record = runtime_records.get(

        cell_id,
        {}
    )

    hard_cooldown = runtime_record.get(
        "hard_cooldown",
        0
    )

    if hard_cooldown > 0:

        return False

    return True
