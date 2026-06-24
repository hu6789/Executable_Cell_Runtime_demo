# aip/viral_behavior_engine/viral_category_allocator.py

# =========================================
# Viral Category Allocation
# =========================================

def allocate_behavior_categories(
    viral_cycle_state,
    viral_context
):

    """
    viral category allocation

    responsibilities:

        - allocate lifecycle tendency

        - consume execution_profile

        - consume resource_preemption

        - generate category allocation

    DOES NOT:

        - perform competition

        - compute behavior drive

        - execute behaviors
    """

    allocation = {

        "entry": 1.0,
        "replication": 1.0,
        "assembly": 1.0,
        "release": 1.0
    }

    # =====================================
    # cycle bias
    # =====================================

    apply_cycle_bias(
        allocation,
        viral_cycle_state
    )

    # =====================================
    # execution profile bias
    # =====================================

    apply_execution_profile_bias(
        allocation,
        viral_context.get(
            "execution_profile",
            {}
        )
    )

    # =====================================
    # resource preemption bias
    # =====================================

    apply_resource_preemption_bias(
        allocation,
        viral_context.get(
            "resource_preemption",
            {}
        )
    )

    # =====================================
    # normalize
    # =====================================

    allocation = normalize_allocation(
        allocation
    )

    return {

        "category_allocation":
            allocation,

        "viral_cycle_state":
            viral_cycle_state,

        "execution_profile":
            viral_context.get(
                "execution_profile",
                {}
            ),

        "resource_preemption":
            viral_context.get(
                "resource_preemption",
                {}
            )
    }


# =========================================
# Cycle Bias
# =========================================

def apply_cycle_bias(
    allocation,
    viral_cycle_state
):

    if viral_cycle_state == "entry":

        allocation["entry"] *= 3.0

    elif viral_cycle_state == "replication":

        allocation["replication"] *= 3.0

    elif viral_cycle_state == "assembly":

        allocation["assembly"] *= 3.0

    elif viral_cycle_state == "release":

        allocation["release"] *= 3.0

    elif viral_cycle_state == "stress":

        allocation["entry"] *= 1.5
        allocation["replication"] *= 0.5

    elif viral_cycle_state == "collapse":

        allocation["replication"] *= 0.2
        allocation["assembly"] *= 0.3
        allocation["release"] *= 0.5


# =========================================
# Execution Profile Bias
# =========================================

def apply_execution_profile_bias(
    allocation,
    execution_profile
):

    allocation["entry"] *= (

        1.0 +

        execution_profile.get(
            "stealth_bias",
            0.0
        )
    )

    allocation["replication"] *= (

        1.0 +

        execution_profile.get(
            "replication_bias",
            0.0
        )
    )

    allocation["assembly"] *= (

        1.0 +

        execution_profile.get(
            "assembly_bias",
            0.0
        )
    )

    allocation["release"] *= (

        1.0 +

        execution_profile.get(
            "release_bias",
            0.0
        )
    )


# =========================================
# Resource Preemption Bias
# =========================================

def apply_resource_preemption_bias(
    allocation,
    resource_preemption
):

    allocation["replication"] *= (

        1.0 +

        resource_preemption.get(
            "ribosome_bias",
            0.0
        )
    )

    allocation["assembly"] *= (

        1.0 +

        resource_preemption.get(
            "ER_bias",
            0.0
        )
    )

    allocation["release"] *= (

        1.0 +

        resource_preemption.get(
            "membrane_bias",
            0.0
        )
    )


# =========================================
# Normalize
# =========================================

def normalize_allocation(
    allocation
):

    total = sum(
        allocation.values()
    )

    if total <= 0:

        return allocation

    return {

        key: value / total

        for key, value in (
            allocation.items()
        )
    }
