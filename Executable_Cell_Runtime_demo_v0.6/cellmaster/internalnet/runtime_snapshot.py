# cellmaster/internalnet/runtime_snapshot.py


# =========================================
# Runtime Snapshot Builder
# =========================================

def build_runtime_snapshot(

    node_runtime_results,

    passive_runtime_results,

    modulation_output,

    hir_output,

    behavior_output,

    tick=None
):

    return {

        "tick":
            tick,

        "node_runtime_results":
            node_runtime_results,

        "passive_runtime_results":
            passive_runtime_results,

        "modulation_output":
            modulation_output,

        "hir_output":
            hir_output,

        "behavior_output":
            behavior_output
    }
