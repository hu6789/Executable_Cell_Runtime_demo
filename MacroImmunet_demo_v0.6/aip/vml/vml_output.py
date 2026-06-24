# aip/vml/vml_output.py


# =========================================
# VML Output Builder
# =========================================

"""
responsibilities:

    - package VML runtime results

    - provide unified VML context

DOES NOT:

    - perform calculations

    - modify runtime state

    - execute viral behaviors
"""


# =========================================
# build output
# =========================================

def build_vml_output(

    viral_state_label,

    infection_load,

    resource_profile,

    execution_profile,

    deception_context,

    resource_preemption
):

    return {

        # -----------------------------
        # truth state
        # -----------------------------

        "viral_state_label":
            viral_state_label,

        # -----------------------------
        # infection assessment
        # -----------------------------

        "infection_load":
            infection_load,

        # -----------------------------
        # structural availability
        # -----------------------------

        "resource_profile":
            resource_profile,

        # -----------------------------
        # viral scheduler output
        # -----------------------------

        "execution_profile":
            execution_profile,

        # -----------------------------
        # host deception layer
        # -----------------------------

        "deception_context":
            deception_context,

        # -----------------------------
        # execution reservation
        # -----------------------------

        "resource_preemption":
            resource_preemption
    }
