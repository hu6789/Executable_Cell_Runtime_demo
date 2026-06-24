# cellinstance/runtime/runtime_entity.py


# =========================================
# Runtime Entity
# =========================================

class RuntimeEntity:

    """
    executable biological runtime entity

    responsibilities:
        - store runtime state
        - store runtime graph context
        - expose runtime identity
        - carry biological execution profiles

    DOES NOT:
        - execute runtime logic directly
        - write world state
        - schedule runtime execution
    """

    def __init__(

        self,

        cell_id,

        template_id,

        identity,

        runtime_state,

        runtime_graph,

        hir_capabilities=None,

        exposure_rules=None,

        runtime_params=None,

        position=None
    ):

        # =================================
        # identity
        # =================================

        self.id = cell_id

        self.template_id = template_id

        self.identity = identity

        # =================================
        # spatial state
        # =================================

        self.position = (
            position or (0, 0)
        )

        # =================================
        # runtime execution state
        # =================================

        self.runtime_state = (
            runtime_state or {}
        )

        # =================================
        # runtime graph
        # =================================

        self.runtime_graph = (
            runtime_graph
        )

        # =================================
        # HIR capability boundary
        # =================================

        self.hir_capabilities = (
            hir_capabilities or {}
        )

        # =================================
        # outward exposure semantics
        # =================================

        self.exposure_rules = (
            exposure_rules or {}
        )

        # =================================
        # runtime parameter schema
        # =================================

        self.runtime_params = (
            runtime_params or {}
        )

        # =================================
        # parasite systems
        # =================================

        self.parasites = []

        # =================================
        # label flags
        # =================================

        self.label_flags = {}

        # =================================
        # directed effects
        # =================================

        self.directed_effects = []

        # =================================
        # runtime bookkeeping
        # =================================

        self.runtime_metadata = {

            "alive": True,

            "spawn_tick": None,

            "last_runtime_tick": None
        }

    # =====================================
    # runtime alive check
    # =====================================

    def is_alive(self):

        return self.runtime_metadata.get(
            "alive",
            True
        )

    # =====================================
    # mark removed
    # =====================================

    def mark_removed(self):

        self.runtime_metadata[
            "alive"
        ] = False

    # =====================================
    # export summary
    # =====================================

    def summary(self):

        return {

            "cell_id":
                self.id,

            "template_id":
                self.template_id,

            "identity":
                self.identity,

            "position":
                self.position,

            "runtime_state":
                self.runtime_state
        }
