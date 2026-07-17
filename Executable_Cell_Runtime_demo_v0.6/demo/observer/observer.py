# demo/observer/observer.py

"""
=========================================================
Simulation Observer
=========================================================

Observer orchestration layer.

Responsibilities
----------------
- capture runtime snapshots
- compute runtime statistics
- record timeline
- dispatch console output

DOES NOT
--------
- access runtime pipeline
- modify simulation world
- execute biological logic
"""

from demo.observer.state_snapshot import (
    StateSnapshotBuilder
)

from demo.observer.statistics import (
    Statistics
)

from demo.observer.timeline import (
    Timeline
)

from demo.observer.console_logger import (
    ConsoleLogger
)

from visualization.recorder import (
    VisualizationRecorder
)

class SimulationObserver:

    """
    High-level observer pipeline.

    Runtime:

        World
            ↓
        Snapshot
            ↓
        Statistics
            ↓
        Timeline
            ↓
        ConsoleLogger
    """

    def __init__(

        self,

        timeline=None,

        console_logger=None,

        enable_console=True

    ):

        self.snapshot_builder = StateSnapshotBuilder()

        self.statistics = Statistics()
        
        self.visualization = VisualizationRecorder()

        #
        # Allow external timeline
        #

        self.timeline = (

            timeline

            or

            Timeline()

        )

        #
        # Allow custom logger
        #

        if console_logger is not None:

            self.console = console_logger

        else:

            self.console = ConsoleLogger(

                enabled=enable_console

            )
    # =====================================================
    # Observe
    # =====================================================

    def observe(
        self,
        tick,
        world,
        runtime_result=None,
        metadata=None

    ):

        snapshot = (

            self.snapshot_builder.capture(

                world,

                tick

            )

        )

        stats = (

            self.statistics.compute(

                snapshot

            )

        )
        
        #
        # Visualization Snapshot
        #

        self.visualization.record_tick(

            tick=tick,

            world=world,

            runtime_result=runtime_result

        )

        self.timeline.record(

            snapshot,

            stats,

            metadata

        )

        record = self.timeline.latest()

        if self.console is not None:

            self.console.log(

                record

            )

        return record

    # =====================================================
    # Helpers
    # =====================================================

    def latest(self):

        return self.timeline.latest()

    def clear(self):

        self.timeline.clear()

        self.visualization.clear()
