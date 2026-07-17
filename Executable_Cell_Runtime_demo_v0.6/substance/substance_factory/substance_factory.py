# substance/substance_factory/substance_factory.py

from substance.substance_factory.runtime_assembler import (
    assemble_runtime_entity
)


class SubstanceFactory:

    """
    Runtime Substance Factory

    Responsibilities:
        - template lookup
        - runtime entity creation

    Does NOT:
        - update world
        - execute interactions
        - run dynamics
    """

    def __init__(

        self,

        template_registry
    ):

        self.template_registry = (
            template_registry
        )

    # =====================================
    # create runtime entity
    # =====================================

    def create_runtime_entity(

        self,

        template_id,

        substance_id,

        position,

        amount=None,
        
        source_id=None
    ):

        template = (
            self.template_registry.get(
                template_id
            )
        )

        if template is None:

            raise ValueError(

                f"Unknown substance template: "
                f"{template_id}"
            )

        return assemble_runtime_entity(

            template=
                template,

            substance_id=
                substance_id,

            position=
                position,

            amount=
                amount,

            source_id=
                source_id
        )

    # =====================================
    # helpers
    # =====================================

    def available_templates(self):

        return sorted(

            self.template_registry.keys()
        )
