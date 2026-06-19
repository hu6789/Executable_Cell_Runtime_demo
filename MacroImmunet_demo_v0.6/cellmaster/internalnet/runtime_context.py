# cellmaster/internalnet/runtime_context.py


# =========================================
# Runtime Context Builder
# =========================================

def build_runtime_context(

    runtime_entity,

    node_inputs,

    runtime_request=None,

    runtime_graph=None,

    tick=None
):

    """
    build unified internal runtime context

    responsibilities:
        - expose runtime entity state
        - expose node inputs
        - expose runtime metadata
        - expose graph/runtime profiles
        - provide shared context for all
          runtime pipeline stages

    used by:
        - node engine
        - passive engine
        - modulation hooks
        - HIR
        - behavior engine
    """

    context = {

        # =================================
        # runtime identity
        # =================================

        "cell_id":
            runtime_entity.id,

        "cell_type":
            getattr(
                runtime_entity,
                "type",
                None
            ),

        # =================================
        # runtime timing
        # =================================

        "tick":
            tick,

        # =================================
        # runtime entity
        # =================================

        "runtime_entity":
            runtime_entity,

        # =================================
        # base runtime state
        # =================================

        "base_runtime_state":
            runtime_entity.runtime_state.snapshot(),

        # =================================
        # node inputs
        # =================================

        "node_inputs":
            node_inputs,

        # =================================
        # runtime request
        # =================================

        "runtime_request":
            runtime_request,

        # =================================
        # runtime graph/profile
        # =================================

        "runtime_graph":
            runtime_graph,

        # =================================
        # label/context exposure
        # =================================

        "runtime_labels":

            getattr(
                runtime_entity,
                "label_flags",
                {}
            ),

        # =================================
        # staged runtime states
        # =================================

        "node_state":
            None,

        "passive_state":
            None,

        "modulated_state":
            None,

        # =================================
        # HIR output
        # =================================

        "hir_output":
            None,

        # =================================
        # behavior outputs
        # =================================

        "behavior_outputs":
            [],

        # =================================
        # runtime debug info
        # =================================

        "runtime_debug":
            {}
    }

    return context
