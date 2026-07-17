# labelcenter/field_projection.py

from collections import defaultdict
import math


DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
        
# =========================================
# apply field projections
# =========================================

def apply_field_projection(
    world,
    field_writes,
    field_defs
):

    """
    field_writes:

    [
        {
            "field_type": "...",
            "position": (x, y),
            "amount": ...
        }
    ]
    """

    accumulated = defaultdict(
        lambda: defaultdict(float)
    )

    # -------------------------------------
    # project all field sources
    # -------------------------------------

    for write in field_writes:
    
        debug_print("FIELD WRITE:", write)

        field_type = write["field_type"]

        position = write["position"]

        amount = write["amount"]

        cfg = field_defs.get(
            field_type,
            {}
        )

        projection_cfg = cfg.get(
            "field_projection",
            {}
        )

        sigma = projection_cfg.get(
            "projection_sigma",
            1.0
        )

        radius = projection_cfg.get(
            "projection_radius",
            int(3 * sigma) + 1
        )

        max_value = projection_cfg.get(
            "max_value",
            999999
        )

        projected = project_gaussian_source(
            world=world,
            center=position,
            amount=amount,
            sigma=sigma,
            radius=radius
        )

        # accumulate
        for pos, val in projected.items():

            accumulated[field_type][pos] += val

    # -------------------------------------
    # apply to world
    # -------------------------------------

    for field_type, grid in accumulated.items():

        world.fields.setdefault(
            field_type,
            {}
        )

        cfg = field_defs.get(
            field_type,
            {}
        )
        
        for pos, val in grid.items():

            old = world.fields[field_type].get(
                pos,
                0.0
            )

            new = min(
                max_value,
                old + val
            )

            world.fields[field_type][pos] = new


# =========================================
# gaussian source projection
# =========================================

def project_gaussian_source(
    world,
    center,
    amount,
    sigma,
    radius
):

    cx, cy = center

    weights = []

    # -------------------------------------
    # collect weights
    # -------------------------------------

    for dx in range(-radius, radius + 1):

        for dy in range(-radius, radius + 1):

            x = cx + dx
            y = cy + dy

            if not (
                0 <= x < world.width
                and
                0 <= y < world.height
            ):
                continue

            dist = math.sqrt(
                dx * dx + dy * dy
            )

            weight = gaussian_kernel(
                dist,
                sigma
            )

            weights.append(
                (
                    (x, y),
                    weight
                )
            )

    total_weight = sum(
        w for _, w in weights
    )

    if total_weight <= 0:

        return {}

    # -------------------------------------
    # normalize projection
    # -------------------------------------

    projected = {}

    for pos, weight in weights:

        projected[pos] = (
            amount
            * weight
            / total_weight
        )

    return projected


# =========================================
# gaussian kernel
# =========================================

def gaussian_kernel(
    distance,
    sigma
):

    if sigma <= 0:
        return 0.0

    return math.exp(
        -(distance ** 2)
        /
        (2 * sigma ** 2)
    )
