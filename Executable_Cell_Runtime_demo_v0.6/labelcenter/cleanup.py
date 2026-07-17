# labelcenter/cleanup.py


# =========================================
# world cleanup
# =========================================

def cleanup_world(
    world
):

    """
    cleanup responsibilities:

        - remove invalid references
        - cleanup stale topology
        - cleanup dead entities
        - cleanup empty field structures

    cleanup DOES NOT:
        - interpret biology
        - judge fate
        - generate new lifecycle events
    """

    cleanup_dead_cells(world)

    cleanup_empty_fields(world)

    cleanup_invalid_links(world)


# =========================================
# cleanup dead cells
# =========================================

def cleanup_dead_cells(
    world
):

    invalid = []

    for cid, cell in world.cells.items():

        # ---------------------------------
        # dead flag
        # ---------------------------------

        if getattr(cell, "removed", False):

            invalid.append(cid)

    for cid in invalid:

        world.remove_cell(cid)


# =========================================
# cleanup empty fields
# =========================================

def cleanup_empty_fields(
    world
):

    removable = []

    for field_type, grid in world.fields.items():

        if not grid:

            removable.append(field_type)

    for field_type in removable:

        del world.fields[field_type]


# =========================================
# cleanup invalid links
# =========================================

def cleanup_invalid_links(
    world
):

    """
    future topology cleanup:

        - orphan immune synapse
        - invalid attachment
        - stale binding
        - broken persistent links
    """

    # -------------------------------------
    # placeholder for v0.6+
    # -------------------------------------

    pass
