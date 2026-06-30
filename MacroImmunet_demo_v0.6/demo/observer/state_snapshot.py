# demo/observer/state_snapshot.py

"""
=========================================================
State Snapshot
=========================================================

Capture immutable runtime snapshots for observers.

Responsibilities
----------------
- capture current world state
- provide read-only observer data
- decouple observers from SimulationWorld

DOES NOT
--------
- modify world
- compute statistics
- print logs
- store history
"""

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict


# ==========================================================
# Snapshot
# ==========================================================

@dataclass
class StateSnapshot:
    """
    Immutable runtime snapshot.

    All observer modules consume this object instead
    of accessing SimulationWorld directly.
    """

    tick: int

    cells: Dict[str, Any] = field(default_factory=dict)

    substances: Dict[str, Any] = field(default_factory=dict)

    fields: Dict[str, Any] = field(default_factory=dict)

    field_defs: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    @property
    def cell_count(self):

        return len(self.cells)

    @property
    def substance_count(self):

        return len(self.substances)

    @property
    def field_count(self):

        return len(self.fields)


# ==========================================================
# Snapshot Builder
# ==========================================================

class StateSnapshotBuilder:

    """
    Capture SimulationWorld into an observer snapshot.

    This is the only observer component allowed to
    access SimulationWorld directly.
    """

    # ======================================================
    # Public Entry
    # ======================================================

    def capture(

        self,

        world,

        tick

    ) -> StateSnapshot:

        return StateSnapshot(

            tick=tick,

            cells=self._capture_cells(world),

            substances=self._capture_substances(world),

            fields=deepcopy(world.fields),

            field_defs=deepcopy(world.field_defs),

            metadata=deepcopy(
                getattr(world, "metadata", {})
            )

        )

    # ======================================================
    # Cells
    # ======================================================

    def _capture_cells(

        self,

        world

    ):

        snapshot = {}

        for cell_id, cell in world.cells.items():

            snapshot[cell_id] = {

                "template_id": getattr(
                    cell,
                    "template_id",
                    None
                ),

                "identity": getattr(
                    cell,
                    "identity",
                    None
                ),

                "position": deepcopy(
                    getattr(
                        cell,
                        "position",
                        None
                    )
                ),

                "runtime_state": self._runtime_state_to_dict(
                    getattr(
                        cell,
                        "runtime_state",
                        None
                    )
                )

            }

        return snapshot

    # ======================================================
    # Substances
    # ======================================================

    def _capture_substances(

        self,

        world

    ):

        snapshot = {}

        for sid, substance in world.substances.items():

            snapshot[sid] = {

                "substance_type": getattr(
                    substance,
                    "substance_type",
                    None
                ),

                "position": deepcopy(
                    getattr(
                        substance,
                        "position",
                        None
                    )
                ),

                "amount": getattr(
                    substance,
                    "amount",
                    None
                )

            }

        return snapshot

    # ======================================================
    # Runtime State
    # ======================================================

    def _runtime_state_to_dict(

        self,

        runtime_state

    ):

        if runtime_state is None:

            return {}

        #
        # RuntimeState currently exposes snapshot().
        #

        if hasattr(runtime_state, "snapshot"):

            return deepcopy(
                runtime_state.snapshot()
            )

        #
        # fallback
        #

        try:

            return deepcopy(dict(runtime_state))

        except Exception:

            return {}
