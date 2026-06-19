# scanmaster/topology_scan.py

import math


# =========================================
# topology scan entry
# =========================================

def scan_topology(
    world,
    tick
):

    """
    scan world topology relations

    current:
        - cell ↔ cell contact

    future:
        - field exposure
        - persistent link
        - directed targeting
        - binding overlap
    """
    topology_events = []

    # cell-cell
    topology_events.extend(

        scan_cell_cell_contacts(
            world,
            tick
        )
    )

    # field exposure
    topology_events.extend(

        scan_field_exposure(
            world,
            tick
        )
    )

    return topology_events

# =========================================
# cell-cell contact scan
# =========================================

def scan_cell_cell_contacts(
    world,
    tick,
    contact_radius=1.5
):

    """
    detect nearby cell-cell topology
    """

    events = []

    cells = list(
        world.cells.values()
    )

    total = len(cells)

    for i in range(total):

        source = cells[i]

        for j in range(i + 1, total):

            target = cells[j]

            distance = compute_distance(

                source.position,
                target.position
            )

            if distance <= contact_radius:

                event = build_contact_topology_event(

                    source=source,
                    target=target,
                    distance=distance,
                    tick=tick
                )

                events.append(event)

    return events


# =========================================
# build topology event
# =========================================

def build_contact_topology_event(
    source,
    target,
    distance,
    tick
):

    return {

        "topology_type": "cell_cell_contact",

        "source_id": source.id,

        "target_id": target.id,

        "source_type": getattr(
            source,
            "type",
            None
        ),

        "target_type": getattr(
            target,
            "type",
            None
        ),

        "distance": distance,

        "tick": tick
    }


# =========================================
# euclidean distance
# =========================================

def compute_distance(
    pos_a,
    pos_b
):

    dx = pos_a[0] - pos_b[0]

    dy = pos_a[1] - pos_b[1]

    return math.sqrt(
        dx * dx + dy * dy
    )
    
# =========================================
# field exposure scan
# =========================================

def scan_field_exposure(
    world,
    tick
):

    events = []

    for field_type, grid in world.fields.items():

        for cell in world.cells.values():

            strength = grid.get(

                cell.position,
                0.0
            )

            if strength <= 0:

                continue

            events.append({

                "topology_type":
                    "field_exposure",

                "field_type":
                    field_type,

                "target_id":
                    cell.id,

                "target_type":
                    getattr(
                        cell,
                        "type",
                        None
                    ),

                "field_strength":
                    strength,

                "tick":
                    tick
            })

    return events
