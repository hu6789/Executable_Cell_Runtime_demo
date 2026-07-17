# demo/runtime/field_projection_engine.py

"""
=========================================================
Field Projection Engine
=========================================================

Convert selected field signals into runtime substance
entities for SubstanceMaster processing.

Responsibilities
----------------
- inspect world fields
- identify field types supporting projection
- instantiate runtime substance entities
- populate world.substances

DOES NOT
--------
- execute biological interactions
- modify field values
- run diffusion or decay
- update cells
"""

from substance.templates.template_loader import (
    TemplateLoader
)

from substance.substance_factory.substance_factory import (
    SubstanceFactory
)


class FieldProjectionEngine:

    """
    Build runtime substance entities from field maps.

    Runtime substances are rebuilt every tick and act as a
    transient execution cache for SubstanceMaster.
    """

    def __init__(

        self,

        template_loader=None,

        substance_factory=None

    ):

        self.template_loader = (
            template_loader
            or TemplateLoader()
        )

        self.substance_factory = (
            substance_factory
            or SubstanceFactory()
        )

    # =====================================================
    # public api
    # =====================================================

    def project(

        self,

        world

    ):

        """
        Rebuild runtime substance cache from field maps.
        """

        #
        # Runtime cache
        #

        world.substances.clear()

        #
        # Every field
        #

        for field_type, field in world.fields.items():

            template = self.template_loader.load(
                field_type
            )

            if template is None:
                continue

            projection = template.get(
                "field_projection"
            )

            #
            # Not every field becomes a substance
            #

            if not projection:
                continue

            #
            # Iterate projected field values
            #

            values = getattr(
                field,
                "values",
                None
            )

            if values is None:

                values = getattr(
                    field,
                    "grid",
                    None
                )

            if values is None:

                values = field

            #
            # dict[(x,y)] -> amount
            #

            for position, amount in values.items():

                if amount <= 0:
                    continue

                substance = self.substance_factory.create(

                    template_id=field_type,

                    position=position,

                    amount=amount

                )

                world.add_substance(
                    substance
                )
