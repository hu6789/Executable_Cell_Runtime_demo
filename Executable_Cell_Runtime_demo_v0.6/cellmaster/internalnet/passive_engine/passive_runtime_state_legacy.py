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
        - convert passive outputs into state patch
        - prepare internalnet merge input

    DOES NOT:
        - modify world state
        - execute physics
    """

    patch = {}

    outputs = passive_definition.get(
        "outputs",
        []
    )

    for output in outputs:

        target = output.get("target")

        if target is None:
            continue

        patch[target] = transformed_delta

    return {

        "runtime_type":
            "passive_state",

        "gate_passed":
            gate_result.get(
                "passed",
                True
            ),

        "computed_delta":
            computed_delta,

        "transformed_delta":
            transformed_delta,

        "state_patch":
            patch,

        "outputs":
            outputs,

        "tick":
            runtime_context.get("tick")
            if runtime_context
            else None
    }
