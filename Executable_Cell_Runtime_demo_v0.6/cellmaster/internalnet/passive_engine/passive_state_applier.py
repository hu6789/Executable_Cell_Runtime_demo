# cellmaster/internalnet/passive_engine/passive_state_applier.py


# =========================================
# Passive State Applier
# =========================================

def apply_passive_runtime_results(
    runtime_state,
    passive_runtime_results
):
    """
    merge passive outputs into runtime state

    responsibilities:
        - apply state_patch from passive results
        - accumulate multiple passive effects
        - ensure deterministic merge

    DOES NOT:
        - compute passive
        - modify graph
    """

    if runtime_state is None:
        runtime_state = {}

    for result in passive_runtime_results:

        state_patch = result.get(
            "runtime_state",
            {}
        ).get(
            "state_patch",
            {}
        )

        for node, delta in state_patch.items():

            runtime_state[node] = (
                runtime_state.get(node, 0.0) + delta
            )

    return runtime_state
