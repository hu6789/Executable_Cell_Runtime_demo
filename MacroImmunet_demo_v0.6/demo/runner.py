# demo/runner.py

"""
=========================================================
Simulation Runner
=========================================================

Top-level runtime driver for MacroImmunet demo.

Responsibilities
----------------
- initialize runtime
- drive simulation loop
- coordinate scenario callbacks
- notify observers

Pipeline
--------
initialize()

for each tick

    Scenario.before_tick()

    SimulationRuntime.step()

    Observer.observe()

    Scenario.after_tick()

shutdown()

DOES NOT
--------
- perform biological reasoning
- modify world directly
- generate intents
"""

from typing import Optional


class SimulationRunner:

    """
    Top-level simulation driver.

    Runner owns the simulation lifecycle while all
    biological computation remains inside the runtime.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(

        self,

        runtime,

        world,

        scenario=None,

        observer=None

    ):

        self.runtime = runtime

        self.world = world

        self.scenario = scenario

        self.observer = observer

        self.running = False

    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self):

        """
        Initialize runtime components.
        """

        if hasattr(self.runtime, "initialize"):

            self.runtime.initialize()

        if (

            self.scenario is not None

            and

            hasattr(
                self.scenario,
                "initialize"
            )

        ):

            self.scenario.initialize(self)

        if (

            self.observer is not None

            and

            hasattr(
                self.observer,
                "initialize"
            )

        ):

            self.observer.initialize(self)

    # =====================================================
    # Run
    # =====================================================

    def run(

        self,

        ticks: int

    ):

        """
        Execute simulation.

        Parameters
        ----------
        ticks
            Number of ticks to execute.
        """

        self.initialize()

        self.running = True

        for tick in range(ticks):

            if not self.running:

                break

            self.step(tick)

        self.shutdown()

    # =====================================================
    # Execute One Tick
    # =====================================================

    def step(

        self,

        tick: int

    ):

        #
        # Scenario
        #

        if (

            self.scenario is not None

            and

            hasattr(
                self.scenario,
                "before_tick"
            )

        ):

            self.scenario.before_tick(

                tick,

                self

            )

        #
        # Runtime
        #

        runtime_result = (

            self.runtime.step(
                tick
            )

        )

        #
        # Observer
        #

        if (

            self.observer is not None

            and

            hasattr(
                self.observer,
                "observe"
            )

        ):

            self.observer.observe(

                tick=tick,

                world=self.world,

                runtime_result=runtime_result

            )

        #
        # Scenario post hook
        #

        if (

            self.scenario is not None

            and

            hasattr(
                self.scenario,
                "after_tick"
            )

        ):

            self.scenario.after_tick(

                tick,

                self

            )

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self):

        self.running = False

        if (

            self.observer is not None

            and

            hasattr(
                self.observer,
                "shutdown"
            )

        ):

            self.observer.shutdown()

        if (

            self.scenario is not None

            and

            hasattr(
                self.scenario,
                "shutdown"
            )

        ):

            self.scenario.shutdown()

    # =====================================================
    # Controls
    # =====================================================

    def stop(self):

        """
        Stop simulation after current tick.
        """

        self.running = False
