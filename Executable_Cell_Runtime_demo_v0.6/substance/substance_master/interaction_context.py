# substance/substance_master/interaction_context.py


def build_interaction_context(

    substance,
    nearby_cells=None,
    nearby_substances=None,
    world=None
):

    """
    Build runtime interaction context.

    SubstanceMaster receives
    a fully prepared interaction snapshot.

    No rule evaluation here.
    No effect computation here.
    """

    if nearby_cells is None:
        nearby_cells = []

    if nearby_substances is None:
        nearby_substances = []

    return {

        # =========================
        # source
        # =========================

        "substance_id":
            substance.id,

        "substance_type":
            substance.substance_type,
            
        "source_id":
            substance.source_id,

        "position":
            substance.position,

        "amount":
            substance.amount,

        # =========================
        # nearby targets
        # =========================

        "candidate_cells":
            nearby_cells,

        "candidate_substances":
            nearby_substances,

        # =========================
        # counts
        # =========================

        "candidate_cell_count":
            len(nearby_cells),

        "candidate_substance_count":
            len(nearby_substances),

        # =========================
        # world
        # =========================

        "world":
            world
    }
