# labelcenter/field_dynamics.py

from collections import defaultdict


# =========================================
# apply field dynamics
# =========================================

def apply_field_dynamics(
    world,
    field_defs
):

    """
    world.fields:

    {
        "IFN_gamma": {
            (x, y): value
        }
    }
    """

    updated_fields = {}

    # -------------------------------------
    # evolve each field independently
    # -------------------------------------

    for field_type, grid in world.fields.items():

        cfg = field_defs.get(
            field_type,
            {}
        )

        evolved = evolve_single_field(
            world=world,
            grid=grid,
            config=cfg
        )

        updated_fields[field_type] = evolved

    # -------------------------------------
    # replace world fields
    # -------------------------------------

    world.fields = updated_fields


# =========================================
# evolve one field
# =========================================

def evolve_single_field(
    world,
    grid,
    config
):

    diffusion_rate = config.get(
        "diffusion_rate",
        0.0
    )

    decay_rate = config.get(
        "decay_rate",
        0.0
    )

    cleanup_threshold = config.get(
        "cleanup_threshold",
        1e-4
    )

    # -------------------------------------
    # diffusion phase
    # -------------------------------------

    diffused = diffuse_grid(
        world=world,
        grid=grid,
        diffusion_rate=diffusion_rate
    )

    # -------------------------------------
    # decay phase
    # -------------------------------------

    decayed = apply_decay(
        diffused,
        decay_rate
    )

    # -------------------------------------
    # cleanup phase
    # -------------------------------------

    cleaned = cleanup_grid(
        decayed,
        cleanup_threshold
    )

    return cleaned


# =========================================
# diffusion
# =========================================

def diffuse_grid(
    world,
    grid,
    diffusion_rate
):

    if diffusion_rate <= 0:

        return dict(grid)

    new_grid = defaultdict(float)

    # 4-neighbor diffusion
    neighbors = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for (x, y), value in grid.items():

        shared = value * diffusion_rate

        remain = value - shared

        # remain locally
        new_grid[(x, y)] += remain

        # distribute
        portion = shared / len(neighbors)

        for dx, dy in neighbors:

            nx = x + dx
            ny = y + dy

            if not (
                0 <= nx < world.width
                and
                0 <= ny < world.height
            ):
                continue

            new_grid[(nx, ny)] += portion

    return dict(new_grid)


# =========================================
# decay
# =========================================

def apply_decay(
    grid,
    decay_rate
):

    if decay_rate <= 0:

        return dict(grid)

    decayed = {}

    for pos, value in grid.items():

        new_value = value * (
            1.0 - decay_rate
        )

        decayed[pos] = new_value

    return decayed


# =========================================
# cleanup
# =========================================

def cleanup_grid(
    grid,
    threshold
):

    cleaned = {}

    for pos, value in grid.items():

        if value >= threshold:

            cleaned[pos] = value

    return cleaned
