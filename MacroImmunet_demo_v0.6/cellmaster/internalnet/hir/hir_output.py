# cellmaster/internalnet/hir/hir_output.py


# =========================================
# HIR Runtime Output
# =========================================

def build_hir_output(
    tick,
    global_context,
    adjusted_context,
    fate_progression,
    physiological_constraints,
    state_labels,
    regulated_behaviors
):

    """
    build unified HIR runtime output

    responsibilities:
        - package HIR interpretation
        - package fate progression
        - package physiological constraints
        - package state labels
        - package regulated behaviors

    DOES NOT:
        - directly execute behaviors
        - directly modify runtime state
        - directly write world
    """

    return {

        "runtime_type":
            "hir",

        "tick":
            tick,

        "global_context":
            global_context,

        "adjusted_context":
            adjusted_context,

        "fate_progression":
            fate_progression,

        "physiological_constraints":
            physiological_constraints,

        "state_labels":
            state_labels,

        "regulated_behaviors":
            regulated_behaviors
    }
