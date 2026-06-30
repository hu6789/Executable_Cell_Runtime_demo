# demo/minidemo.py

"""
=========================================================
MiniDemo
=========================================================

High-level runtime entry for MacroImmunet Demo.

Responsibilities
----------------
- build simulation
- own runtime objects
- execute ticks
- expose simple demo API

DOES NOT
--------
- perform biological reasoning
- modify InternalNet
- access LabelCenter directly
- implement scenarios
"""

from demo.builder.simulation_builder import (
    SimulationBuilder
)

from demo.runtime.simulation_runtime import (
    SimulationRuntime
)

from demo.runtime.simulation_runner import (
    SimulationRunner
)

from demo.observer.observer import (
    SimulationObserver
)


class MiniDemo:

    """
    High-level simulation API.

    Runtime:

        Scenario
            ↓

        SimulationBuilder
            ↓

        SimulationWorld
            ↓

        SimulationRuntime
            ↓

        SimulationRunner
            ↓

        SimulationObserver
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        builder=None,

        observer=None

    ):

        self.builder = (

            builder

            or

            SimulationBuilder()

        )

        self.observer = (

            observer

            or

            SimulationObserver()

        )

        self.world = None

        self.runtime = None

        self.runner = None

    # =====================================================
    # Build
    # =====================================================

    def build(

        self,

        scenario

    ):

        """
        Build a simulation from a scenario.
        """

        self.world = self.builder.build(

            scenario

        )

        self.runtime = SimulationRuntime(

            world=self.world

        )

        self.runner = SimulationRunner(

            runtime=self.runtime,

            observer=self.observer

        )

        return self.world

    # =====================================================
    # Step
    # =====================================================

    def step(self):

        """
        Execute one simulation tick.
        """

        if self.runner is None:

            raise RuntimeError(

                "Simulation has not been built."

            )

        return self.runner.step()

    # =====================================================
    # Run
    # =====================================================

    def run(

        self,

        ticks

    ):

        """
        Execute multiple ticks.
        """

        results = []

        for _ in range(ticks):

            results.append(

                self.step()

            )

        return results

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        """
        Reset runtime state.
        """

        self.world = None

        self.runtime = None

        self.runner = None

        self.observer.clear()

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def tick(self):

        if self.runtime is None:

            return 0

        return self.runtime.tick

    @property
    def timeline(self):

        return self.observer.timeline

    @property
    def latest(self):

        return self.observer.latest()
