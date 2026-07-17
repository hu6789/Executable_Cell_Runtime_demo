# aip/vml/execution_profile.py


# =========================================
# Viral Execution Scheduler
# =========================================

"""
responsibilities:

    - determine viral strategy

    - allocate execution priorities

    - modulate viral behavior intensity

DOES NOT:

    - execute behaviors

    - modify runtime state

    - generate deception
"""


# =========================================
# main
# =========================================

def build_execution_profile(

    viral_state_label,

    infection_load,

    resource_profile
):

    replication_bias = 0.0
    damage_bias = 0.0
    assembly_bias = 0.0
    release_bias = 0.0
    stealth_bias = 0.0

    execution_scale = (
        resource_profile.get(
            "resource_limit",
            0.0
        )
    )

    # =====================================
    # entry
    # =====================================

    if viral_state_label == "entry":

        stealth_bias = 1.0
        replication_bias = 0.2

    # =====================================
    # replication
    # =====================================

    elif viral_state_label == "replication":

        replication_bias = 1.0
        damage_bias = 0.2

    # =====================================
    # assembly
    # =====================================

    elif viral_state_label == "assembly":

        assembly_bias = 1.0
        replication_bias = 0.5

    # =====================================
    # release
    # =====================================

    elif viral_state_label == "release":

        release_bias = 1.0
        damage_bias = 1.0

    # =====================================
    # stress
    # =====================================

    elif viral_state_label == "stress":

        replication_bias = 0.3
        stealth_bias = 0.5

    # =====================================
    # collapse
    # =====================================

    elif viral_state_label == "collapse":

        execution_scale *= 0.1

    # =====================================
    # infection load scaling
    # =====================================

    viral_load = infection_load.get(
        "viral_load",
        0.0
    )

    load_scale = min(
        viral_load / 100.0,
        2.0
    )

    replication_bias *= load_scale
    damage_bias *= load_scale
    assembly_bias *= load_scale
    release_bias *= load_scale

    # =====================================
    # output
    # =====================================

    return {

        "replication_bias":
            replication_bias,

        "damage_bias":
            damage_bias,

        "assembly_bias":
            assembly_bias,

        "release_bias":
            release_bias,

        "stealth_bias":
            stealth_bias,

        "execution_scale":
            execution_scale
    }
