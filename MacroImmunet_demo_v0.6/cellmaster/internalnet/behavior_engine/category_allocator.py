# cellmaster/internalnet/behavior_engine/category_allocator.py
# reserved for contribution-level bias
# will be consumed by behavior_group /
# behavior_aggregate stage

# =========================================
# Behavior Category Allocation
# =========================================

def allocate_behavior_categories(
    ecology_context
):

    """
    perform high-level behavior category allocation

    responsibilities:
        - allocate global behavior ecology
        - distribute runtime resource tendency
        - bias behavior category priority
        - construct category-level runtime share

    DOES NOT:
        - compute concrete behavior drive
        - execute behavior competition
        - evaluate graph contributions
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
    # initialize category allocation
    # =====================================

    category_allocation = {

        "survival":
            1.0,

        "repair":
            1.0,

        "secretion":
            1.0,

        "mobility":
            1.0,

        "proliferation":
            1.0
    }

    # =====================================
    # apply ecology bias
    # =====================================

    apply_bias_allocation(
        category_allocation,
        ecology_bias
    )

    # =====================================
    # apply ATP resource scaling
    # =====================================

    apply_resource_scaling(
        category_allocation,
        ATP
    )

    # =====================================
    # normalize allocation
    # =====================================

    normalized = normalize_allocation(
        category_allocation
    )

    updated_context = dict(
        ecology_context
    )

    updated_context[
        "category_allocation"
    ] = normalized

    return updated_context


# =========================================
# Apply Ecology Bias
# =========================================

def apply_bias_allocation(
    allocation,
    ecology_bias
):

    allocation[
        "survival"
    ] *= ecology_bias.get(
        "survival_bias",
        1.0
    )

    allocation[
        "repair"
    ] *= ecology_bias.get(
        "repair_bias",
        1.0
    )

    allocation[
        "secretion"
    ] *= ecology_bias.get(
        "secretion_bias",
        1.0
    )

    allocation[
        "mobility"
    ] *= ecology_bias.get(
        "mobility_bias",
        1.0
    )

    allocation[
        "proliferation"
    ] *= ecology_bias.get(
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
    low ATP shifts ecology
    toward survival/repair
    """

    if ATP < 5.0:

        allocation[
            "survival"
        ] *= 1.5

        allocation[
            "repair"
        ] *= 1.3

        allocation[
            "proliferation"
        ] *= 0.3

        allocation[
            "secretion"
        ] *= 0.6

    if ATP < 2.0:

        allocation[
            "mobility"
        ] *= 0.3


# =========================================
# Normalize Allocation
# =========================================

def normalize_allocation(
    allocation
):

    total = sum(
        allocation.values()
    )

    if total <= 0:

        return allocation

    normalized = {}

    for key, value in allocation.items():

        normalized[key] = (
            value / total
        )

    return normalized
