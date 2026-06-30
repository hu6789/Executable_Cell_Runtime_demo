# demo/runtime/simulation_world.py

"""
=========================================================
Simulation World
=========================================================

Shared runtime world container for MacroImmunet.

Responsibilities
----------------
- store runtime world state
- provide unified entity access
- expose runtime factories
- provide world mutation APIs

DOES NOT
--------
- execute simulation
- perform biological reasoning
- schedule runtime
- advance ticks
"""

from typing import Dict, Optional, Any


class SimulationWorld:

    """
    Runtime world container.

    This object is the shared runtime state used by all
    runtime modules.

    Shared by
    ---------
    - ScanMaster
    - InputBuilder
    - CellMaster
    - SubstanceMaster
    - LabelCenter
    - MiniSIO
    - Observer
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(

        self,

        cell_factory=None,

        substance_factory=None

    ):

        #
        # Runtime entities
        #

        self.cells: Dict[str, Any] = {}

        self.substances: Dict[str, Any] = {}

        self.viruses: Dict[str, Any] = {}

        #
        # Runtime fields
        #

        self.fields: Dict[str, Any] = {}

        self.field_defs: Dict[str, Any] = {}

        #
        # Runtime links
        #

        self.links = {}

        #
        # Directed effects
        #

        self.directed_effects = []

        #
        # Runtime services
        #

        self.cell_factory = cell_factory

        self.substance_factory = substance_factory

        #
        # User metadata
        #

        self.metadata = {}

    # =====================================================
    # Cell API
    # =====================================================

    def add_cell(self, cell):

        self.cells[cell.id] = cell

    def remove_cell(self, cell_id):

        self.cells.pop(cell_id, None)

    def get_cell(self, cell_id):

        return self.cells.get(cell_id)

    def has_cell(self, cell_id):

        return cell_id in self.cells

    # =====================================================
    # Substance API
    # =====================================================

    def add_substance(self, substance):

        self.substances[substance.id] = substance

    def remove_substance(self, substance_id):

        self.substances.pop(substance_id, None)

    def get_substance(self, substance_id):

        return self.substances.get(substance_id)

    def has_substance(self, substance_id):

        return substance_id in self.substances

    # =====================================================
    # Virus API
    # =====================================================

    def add_virus(self, virus):

        self.viruses[virus.id] = virus

    def remove_virus(self, virus_id):

        self.viruses.pop(virus_id, None)

    def get_virus(self, virus_id):

        return self.viruses.get(virus_id)

    def has_virus(self, virus_id):

        return virus_id in self.viruses

    # =====================================================
    # Field API
    # =====================================================

    def ensure_field(self, field_name):

        if field_name not in self.fields:

            self.fields[field_name] = {}

    def ensure_field_definition(

        self,

        field_name,

        definition=None

    ):

        if field_name not in self.field_defs:

            self.field_defs[field_name] = definition or {}

    def clear_field(self, field_name):

        self.fields.pop(field_name, None)

        self.field_defs.pop(field_name, None)

    # =====================================================
    # Directed Effects
    # =====================================================

    def clear_directed_effects(self):

        self.directed_effects.clear()

    # =====================================================
    # Helpers
    # =====================================================

    def entity_count(self):

        return {

            "cells": len(self.cells),

            "substances": len(self.substances),

            "viruses": len(self.viruses)

        }

    def is_empty(self):

        return (

            not self.cells

            and

            not self.substances

            and

            not self.viruses

        )

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        self.cells.clear()

        self.substances.clear()

        self.viruses.clear()

        self.fields.clear()

        self.field_defs.clear()

        self.links.clear()

        self.directed_effects.clear()

        self.metadata.clear()

    # =====================================================
    # Debug
    # =====================================================

    def summary(self):

        return {

            "cells": len(self.cells),

            "substances": len(self.substances),

            "viruses": len(self.viruses),

            "fields": list(self.fields.keys()),

            "links": len(self.links)

        }

    def __repr__(self):

        s = self.summary()

        return (

            "SimulationWorld("

            f"cells={s['cells']}, "

            f"substances={s['substances']}, "

            f"viruses={s['viruses']}, "

            f"fields={len(s['fields'])}"

            ")"

        )
