# cellinstance/templates/cell_template.py


# =========================================
# Cell Template
# =========================================

class CellTemplate:

    """
    static biological definition layer

    responsibilities:
        - define biological identity
        - define graph references
        - define initial runtime state schema
        - define HIR capabilities
        - define public exposure rules
        - define runtime parameter schemas

    DOES NOT:
        - execute runtime logic
        - store runtime state
        - write world state
        - perform physiology simulation
    """

    def __init__(

        self,

        template_id,

        identity,

        graph_refs=None,

        init_node_state=None,

        hir_capabilities=None,

        exposure_rules=None,

        runtime_params=None
    ):

        # =================================
        # template identity
        # =================================

        self.template_id = template_id

        self.identity = identity

        # =================================
        # runtime graph references
        # =================================

        self.graph_refs = (
            graph_refs or {}
        )

        # =================================
        # runtime initialization schema
        # =================================

        self.init_node_state = (
            init_node_state or {}
        )

        # =================================
        # HIR capabilities
        # =================================

        self.hir_capabilities = (
            hir_capabilities or {}
        )

        # =================================
        # public exposure semantics
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

    # =====================================
    # export template
    # =====================================

    def to_dict(self):

        return {

            "template_id":
                self.template_id,

            "identity":
                self.identity,

            "graph_refs":
                self.graph_refs,

            "init_node_state":
                self.init_node_state,

            "hir_capabilities":
                self.hir_capabilities,

            "exposure_rules":
                self.exposure_rules,

            "runtime_params":
                self.runtime_params
        }
