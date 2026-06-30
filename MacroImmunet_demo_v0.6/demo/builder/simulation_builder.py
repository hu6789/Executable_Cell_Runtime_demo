# demo/builder/simulation_builder.py

"""
=========================================================
Simulation Builder
=========================================================

Construct runtime-ready simulation objects.

Responsibilities
----------------
- initialize runtime loaders
- construct runtime factories
- build SimulationWorld
- populate initial runtime entities

DOES NOT
--------
- execute simulation
- perform biological reasoning
- modify runtime after build
"""

from typing import Dict, Optional, Tuple

from demo.runtime.simulation_world import SimulationWorld

from cellinstance.templates.template_loader import (
    TemplateLoader
)

from cellmaster.internalnet.runtime_graph.graph_loader import (
    RuntimeGraphLoader
)

from cellinstance.factory.cell_factory import (
    CellFactory
)

from substance.substance_factory.substance_factory import (
    SubstanceFactory
)


class SimulationBuilder:

    """
    Build runtime-ready simulation worlds.

    Designed for demo, testing and future scenarios.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(

        self,

        cell_template_dir="cellinstance/cells",

        substance_registry=None

    ):

        #
        # loaders
        #

        self.template_loader = TemplateLoader()

        self.template_loader.load_template_directory(
            cell_template_dir
        )

        self.graph_loader = RuntimeGraphLoader()

        #
        # factories
        #

        self.cell_factory = CellFactory(

            self.template_loader,

            self.graph_loader

        )

        self.substance_factory = SubstanceFactory(

            substance_registry or {}

        )

        #
        # world
        #

        self.world = SimulationWorld(

            cell_factory=self.cell_factory,

            substance_factory=self.substance_factory

        )

    # =====================================================
    # Cells
    # =====================================================

    def add_cell(

        self,

        template_id,

        cell_id,

        position=(0, 0),

        runtime_state=None

    ):

        entity = self.cell_factory.create_runtime_entity(

            template_id=template_id,

            cell_id=cell_id,

            position=position

        )

        runtime_state = runtime_state or {}

        for key, value in runtime_state.items():

            entity.runtime_state[key] = value

        self.world.add_cell(entity)

        return self

    # =====================================================
    # Substances
    # =====================================================

    def add_substance(

        self,

        template_id,

        substance_id,

        position=(0, 0),

        amount=1.0

    ):

        entity = self.substance_factory.create_runtime_entity(

            template_id=template_id,

            substance_id=substance_id,

            position=position,

            amount=amount

        )

        self.world.add_substance(entity)

        return self

    # =====================================================
    # Fields
    # =====================================================

    def add_field(

        self,

        field_name,

        values,

        definition=None

    ):

        self.world.fields[field_name] = dict(values)

        self.world.field_defs[field_name] = (

            definition or {}

        )

        return self

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(

        self,

        **kwargs

    ):

        self.world.metadata.update(kwargs)

        return self

    # =====================================================
    # Build
    # =====================================================

    def build(self):

        """
        Return fully initialized world.
        """

        return self.world
