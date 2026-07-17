# demo/runtime/simulation_runtime.py

"""
=========================================================
Simulation Runtime
=========================================================

Runtime execution driver for MacroImmunet Demo.

Responsibilities
----------------
- drive one simulation tick
- orchestrate runtime pipeline
- collect runtime intents
- commit world updates through LabelCenter

Pipeline
--------
ScanMaster
    ↓
InputBuilder
    ↓
CellMaster
    ↓
SubstanceMaster (optional)
    ↓
IntentBuilder
    ↓
LabelCenter

DOES NOT
--------
- perform biological reasoning
- modify runtime state directly
- create entities directly
- interpret scenarios
"""

from typing import Optional, List, Dict, Any

from scanmaster.scan_master import ScanMaster
from inputbuilder.input_builder import InputBuilder
from cellmaster.cell_master import CellMaster
from substance.substance_master.substance_master import SubstanceMaster
from intentbuilder.intent_builder import IntentBuilder
from labelcenter.labelcenter import LabelCenter
from substance.substance_factory.substance_factory import (
    SubstanceFactory
)

from substance.templates.template_loader import (
    load_template_directory
)

from substance.substance_spawn.spawn_from_field import (
    spawn_substances_from_field_intents
)

class SimulationRuntime:

    """
    Runtime execution orchestrator.

    Owns every runtime component and executes one
    complete simulation tick.

    Scenario / GUI / CLI should only interact with
    SimulationRuntime instead of individual modules.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(

        self,

        world,

        scanmaster: Optional[ScanMaster] = None,

        inputbuilder: Optional[InputBuilder] = None,

        cellmaster: Optional[CellMaster] = None,

        substancemaster: Optional[SubstanceMaster] = None,

        intentbuilder: Optional[IntentBuilder] = None,

        labelcenter: Optional[LabelCenter] = None

    ):

        self.world = world
        
        templates = load_template_directory(
            "substance/substances"
        )

        self.substance_factory = SubstanceFactory(
            templates
        )

        self.scanmaster = scanmaster or ScanMaster()

        self.inputbuilder = inputbuilder or InputBuilder()

        self.cellmaster = cellmaster or CellMaster()

        self.substancemaster = (
            substancemaster or SubstanceMaster()
        )

        self.intentbuilder = (
            intentbuilder or IntentBuilder()
        )

        self.labelcenter = (
            labelcenter or LabelCenter()
        )

    # =====================================================
    # Public API
    # =====================================================

    def initialize(self):
        """
        Runtime initialization hook.

        Reserved for future initialization logic.

        Current implementation intentionally does nothing.
        """
        return

    # =====================================================
    # Execute One Tick
    # =====================================================

    def step(
        self,
        tick: int
    ) -> Dict[str, Any]:

        """
        Execute one complete runtime tick.

        Returns
        -------
        dict

            {
                "events": ...
                "node_inputs": ...
                "cell_packages": ...
                "substance_requests": ...
                "intents": ...
            }
        """

        # ---------------------------------------------
        # Scan
        # ---------------------------------------------

        events = self._run_scan(
            tick
        )

        # ---------------------------------------------
        # Input Builder
        # ---------------------------------------------

        node_inputs = self._run_input_builder(
            events
        )

        # ---------------------------------------------
        # Cell Runtime
        # ---------------------------------------------

        cell_packages = self._run_cell_pipeline(

            node_inputs=node_inputs,

            tick=tick

        )

        # ---------------------------------------------
        # Build intents
        # ---------------------------------------------

        intents = self._run_intent_builder(
            cell_packages,
            []
        )

        # ---------------------------------------------
        # Spawn runtime substances
        # ---------------------------------------------

        spawn_substances_from_field_intents(
            intents=intents,
            world=self.world,
            substance_factory=self.substance_factory
        )

        # ---------------------------------------------
        # Substance runtime
        # ---------------------------------------------

        substance_requests = self._run_substance_pipeline()

        # ---------------------------------------------
        # Substance requests -> IntentBuilder
        # ---------------------------------------------

        if substance_requests:

            self.intentbuilder.collect(
                substance_requests
            )

            intents.extend(
                self.intentbuilder.build()
            )

        # ---------------------------------------------
        # LabelCenter
        # ---------------------------------------------

        self._run_labelcenter(

            intents,

            tick

        )

        return {

            "events": events,

            "node_inputs": node_inputs,

            "cell_packages": cell_packages,

            "substance_requests": substance_requests,

            "intents": intents

        }

    # =====================================================
    # Scan
    # =====================================================

    def _run_scan(
        self,
        tick
    ):

        return self.scanmaster.scan(

            self.world,

            tick

        )

    # =====================================================
    # InputBuilder
    # =====================================================

    def _run_input_builder(
        self,
        events
    ):

        self.inputbuilder.collect(
            events
        )

        result = self.inputbuilder.build()

        return result.get(
            "node_inputs",
            []
        )

    # =====================================================
    # Cell Pipeline
    # =====================================================

    def _run_cell_pipeline(

        self,

        node_inputs,

        tick

    ):

        return self.cellmaster.run(

            node_inputs=node_inputs,

            world=self.world,

            tick=tick

        )

    # =====================================================
    # Substance Pipeline
    # =====================================================

    def _run_substance_pipeline(self):

        requests = []

        for substance in self.world.substances.values():

            # --------------------------
            # collect nearby cells
            # --------------------------

            candidate_cells = []

            radius = substance.template.effect_radius

            sx, sy = substance.position

            for cell in self.world.cells.values():

                cx, cy = cell.position

                distance = abs(cx - sx) + abs(cy - sy)

                if distance <= radius:

                    candidate_cells.append(cell)

            # --------------------------
            # collect nearby substances
            # --------------------------

            candidate_substances = []

            for other in self.world.substances.values():

                if other.id == substance.id:
                    continue

                if other.position == substance.position:

                    candidate_substances.append(other)

            result = self.substancemaster.process(

                substance=substance,

                template=substance.template,

                candidate_cells=candidate_cells,

                candidate_substances=candidate_substances,

                world=self.world
            )

            if result:
                requests.extend(result)

        return requests

    # =====================================================
    # Intent Builder
    # =====================================================

    def _run_intent_builder(

        self,

        cell_packages,

        substance_requests

    ):

        #
        # Cell packages
        #

        for package in cell_packages:

            self.intentbuilder.collect(

                package.get(

                    "intent_requests",

                    []

                )

            )

        #
        # Substance requests
        #

        if substance_requests:

            self.intentbuilder.collect(

                substance_requests

            )

        return self.intentbuilder.build()

    # =====================================================
    # LabelCenter
    # =====================================================

    def _run_labelcenter(

        self,

        intents,

        tick

    ):

        self.labelcenter.collect(
            intents
        )

        self.labelcenter.apply(

            self.world,

            tick

        )

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def cells(self):

        return self.world.cells

    @property
    def substances(self):

        return getattr(
            self.world,
            "substances",
            {}
        )

    @property
    def fields(self):

        return self.world.fields
