# cellmaster/internalnet/passive_engine/passive_runtime_state.py


# =========================================
# Passive Runtime State Builder
# =========================================

def build_passive_runtime_state(
    passive_definition,
    computed_delta,
    transformed_delta,
    gate_result,
    runtime_context=None
):
    """
    convert passive result into runtime state patch

    responsibilities:
        - map passive output to target nodes
        - build state update payload
        - prepare internalnet merge input

    DOES NOT:
        - modify world state
        - execute physics
    """

    # =====================================
    # resolve target
    # =====================================

    update_target = passive_definition.get(
        "passive_gate",
        {}
    ).get(
        "update_target"
    )

    # fallback: infer from involved nodes
    if update_target is None:

        involved_nodes = passive_definition.get(
            "involved_nodes",
            []
        )

        update_target = (
            involved_nodes[0]
            if involved_nodes
            else None
        )

    # =====================================
    # build patch
    # =====================================

    patch = {}

    if update_target is not None:

        patch[update_target] = transformed_delta

    # =====================================
    # metadata
    # =====================================

    return {

        "runtime_type":
            "passive_state",

        "gate_passed":
            gate_result.get("gate_passed", True),

        "computed_delta":
            computed_delta,

        "transformed_delta":
            transformed_delta,

        "state_patch":
            patch,

        "target":
            update_target,

        "tick":
            runtime_context.get("tick") if runtime_context else None
    }
