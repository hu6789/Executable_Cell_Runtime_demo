# aip/vml/resource_preemption.py


# =========================================
# Resource Pre-emption Mapping
# =========================================

"""
responsibilities:

    - reserve execution priority

    - bias resource allocation

    - influence viral behavior capacity

DOES NOT:

    - consume resources

    - modify runtime state

    - execute behaviors
"""


# =========================================
# main
# =========================================

def build_resource_preemption(

    viral_state_label,

    infection_load,

    resource_profile,

    execution_profile
):

    resource_limit = (
        resource_profile.get(
            "resource_limit",
            0.0
        )
    )

    replication_bias = (
        execution_profile.get(
            "replication_bias",
            0.0
        )
    )

    assembly_bias = (
        execution_profile.get(
            "assembly_bias",
            0.0
        )
    )

    release_bias = (
        execution_profile.get(
            "release_bias",
            0.0
        )
    )

    # =====================================
    # defaults
    # =====================================

    ribosome_bias = 0.0

    er_bias = 0.0

    membrane_bias = 0.0

    trafficking_bias = 0.0

    # =====================================
    # cycle-specific allocation
    # =====================================

    if viral_state_label == "entry":

        trafficking_bias = 0.6

    elif viral_state_label == "replication":

        ribosome_bias = (
            0.8 * replication_bias
        )

        er_bias = (
            0.5 * replication_bias
        )

    elif viral_state_label == "assembly":

        er_bias = (
            0.8 * assembly_bias
        )

        trafficking_bias = (
            0.5 * assembly_bias
        )

    elif viral_state_label == "release":

        membrane_bias = (
            0.8 * release_bias
        )

        trafficking_bias = (
            1.0 * release_bias
        )

    elif viral_state_label == "stress":

        ribosome_bias = 0.2

    elif viral_state_label == "collapse":

        ribosome_bias = 0.0

        er_bias = 0.0

        membrane_bias = 0.0

        trafficking_bias = 0.0

    # =====================================
    # scale by resource availability
    # =====================================

    ribosome_bias *= resource_limit

    er_bias *= resource_limit

    membrane_bias *= resource_limit

    trafficking_bias *= resource_limit

    # =====================================
    # output
    # =====================================

    return {

        "ribosome_bias":
            ribosome_bias,

        "ER_bias":
            er_bias,

        "membrane_bias":
            membrane_bias,

        "trafficking_bias":
            trafficking_bias
    }
