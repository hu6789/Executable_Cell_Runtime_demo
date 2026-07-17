# cellinstance/factory/cell_factory.py


from cellinstance.factory.runtime_assembler import (
    RuntimeAssembler
)

from cellinstance.factory.stochastic_initializer import (
    StochasticInitializer
)

from cellinstance.runtime.runtime_entity import (
    RuntimeEntity
)

from cellinstance.runtime.runtime_state import RuntimeState

# =========================================
# Cell Factory
# =========================================

class CellFactory:

    """
    runtime biological entity factory

    responsibilities:
        - construct runtime entities
        - assemble runtime graph/state
        - initialize stochastic runtime values
        - attach runtime execution context

    DOES NOT:
        - execute runtime logic
        - write world state directly
        - apply lifecycle changes
    """

    def __init__(

        self,

        template_loader,

        runtime_graph_loader
    ):

        self.template_loader = (
            template_loader
        )

        self.runtime_graph_loader = (
            runtime_graph_loader
        )

        self.runtime_assembler = (
            RuntimeAssembler(
                runtime_graph_loader
            )
        )

        self.stochastic_initializer = (
            StochasticInitializer()
        )

    # =====================================
    # create runtime entity
    # =====================================

    def create_runtime_entity(

        self,

        template_id,

        cell_id,

        position=None,

        overrides=None
    ):

        # =================================
        # load template
        # =================================

        template = (
            self.template_loader.get_template(
                template_id
            )
        )

        if template is None:

            raise ValueError(

                f"template not found: "
                f"{template_id}"
            )

        # =================================
        # initialize runtime state
        # =================================

        runtime_state = RuntimeState(
            self.stochastic_initializer.initialize_runtime_state(
                template.init_node_state
            )
        )
        # =================================
        # assemble runtime graph
        # =================================

        runtime_graph = (
            self.runtime_assembler
            .assemble_runtime_graph(

                template.graph_refs
            )
        )

        # =================================
        # construct runtime entity
        # =================================

        entity = RuntimeEntity(

            cell_id=
                cell_id,

            template_id=
                template.template_id,

            identity=
                template.identity,

            runtime_state=
                runtime_state,

            runtime_graph=
                runtime_graph,

            hir_capabilities=
                template.hir_capabilities,

            exposure_rules=
                template.exposure_rules,

            runtime_params=
                template.runtime_params,

            position=
                position
        )

        # =================================
        # runtime overrides
        # =================================

        if overrides is not None:

            self.apply_overrides(

                entity,
                overrides
            )

        return entity

    # =====================================
    # apply runtime overrides
    # =====================================

    def apply_overrides(

        self,

        entity,

        overrides
    ):

        runtime_state = overrides.get(
            "runtime_state",
            {}
        )

        for k, v in runtime_state.items():

            entity.runtime_state[k] = v
