# cellmaster/internalnet/behavior_engine/category_allocator.py

from cellmaster.internalnet.behavior_engine.ecology_category_mapper import (
    map_ecology_to_behavior_categories
)


# =========================================
# Behavior Category Allocation
# =========================================

def allocate_behavior_categories(
    ecology_context
):

    """
    perform high-level behavior category allocation

    responsibilities:
        - allocate ecology-level runtime tendency
        - apply physiology/resource constraints
        - translate ecology allocation into
          behavior-category allocation
        - expose runtime behavior shares

    DOES NOT:
        - compete behaviors
        - evaluate graph contributions
        - execute behaviors
    """

    ecology_bias = ecology_context.get(
        "ecology_bias",
        {}
    )

    runtime_ecology = ecology_context.get(
        "ecology_context",
        {}
    )

    resource_ecology = runtime_ecology.get(
        "resource_ecology",
        {}
    )

    ATP = resource_ecology.get(
        "ATP",
        0.0
    )

    # =====================================
    # initialize ecology allocation
    # =====================================

    ecology_allocation = build_initial_ecology_allocation()

    # =====================================
    # ecology bias
    # =====================================

    apply_bias_allocation(
        ecology_allocation,
        ecology_bias
    )

    # =====================================
    # resource scaling
    # =====================================

    apply_resource_scaling(
        ecology_allocation,
        ATP
    )

    # =====================================
    # normalize ecology allocation
    # =====================================

    ecology_allocation = normalize_allocation(
        ecology_allocation
    )

    # =====================================
    # ecology -> behavior category
    # =====================================

    category_allocation = (
        map_ecology_to_behavior_categories(
            ecology_allocation
        )
    )

    # =====================================
    # update context
    # =====================================

    updated_context = dict(
        ecology_context
    )

    updated_context[
        "ecology_allocation"
    ] = ecology_allocation

    updated_context[
        "category_allocation"
    ] = category_allocation

    return updated_context


# =========================================
# Initial Ecology Allocation
# =========================================

def build_initial_ecology_allocation():

    """
    ecology dimensions

    these are NOT behavior categories.

    they represent global physiological
    investment directions.
    """

    return {

        "survival": 1.0,

        "repair": 1.0,

        "secretion": 1.0,

        "mobility": 1.0,

        "proliferation": 1.0
    }


# =========================================
# Apply Ecology Bias
# =========================================

def apply_bias_allocation(
    allocation,
    ecology_bias
):

    allocation["survival"] *= ecology_bias.get(
        "survival_bias",
        1.0
    )

    allocation["repair"] *= ecology_bias.get(
        "repair_bias",
        1.0
    )

    allocation["secretion"] *= ecology_bias.get(
        "secretion_bias",
        1.0
    )

    allocation["mobility"] *= ecology_bias.get(
        "mobility_bias",
        1.0
    )

    allocation["proliferation"] *= ecology_bias.get(
        "proliferation_bias",
        1.0
    )


# =========================================
# Resource Scaling
# =========================================

def apply_resource_scaling(
    allocation,
    ATP
):

    """
    ATP shortage shifts investment toward
    survival and repair.
    """

    if ATP < 5.0:

        allocation["survival"] *= 1.5
        allocation["repair"] *= 1.3

        allocation["secretion"] *= 0.6
        allocation["proliferation"] *= 0.3

    if ATP < 2.0:

        allocation["mobility"] *= 0.3


# =========================================
# Normalize Allocation
# =========================================

def normalize_allocation(
    allocation
):

    total = sum(
        allocation.values()
    )

    if total <= 0.0:

        return dict(allocation)

    normalized = {}

    for key, value in allocation.items():

        normalized[key] = (
            value / total
        )

    return normalized
