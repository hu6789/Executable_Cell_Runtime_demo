# demo/observer/timeline.py

"""
=========================================================
Simulation Timeline
=========================================================

Store runtime history for replay and analysis.

Responsibilities
----------------
- record simulation history
- provide tick lookup
- export runtime history

DOES NOT
--------
- access SimulationWorld
- compute statistics
- print logs
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==========================================================
# Tick Record
# ==========================================================

@dataclass
class TickRecord:

    tick: int

    snapshot: Any

    statistics: Any

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ==========================================================
# Timeline
# ==========================================================

class Timeline:

    """
    Simulation history storage.

    Stores immutable TickRecords.
    """

    def __init__(

        self,

        max_records=None

    ):

        self.records: List[TickRecord] = []

        self.max_records = max_records

    # ======================================================
    # Record
    # ======================================================

    def record(

        self,

        snapshot,
 
        statistics,

        metadata=None

    ):

        self.records.append(

            TickRecord(

                tick=snapshot.tick,

                snapshot=snapshot,

                statistics=statistics,

                metadata=metadata or {}

            )

        )

        #
        # Rolling window
        #

        if (

            self.max_records is not None

            and

            len(self.records) > self.max_records

        ):

            self.records.pop(0)

    # ======================================================
    # Lookup
    # ======================================================

    def latest(self) -> Optional[TickRecord]:

        if not self.records:

            return None

        return self.records[-1]

    def get(

        self,

        tick

    ) -> Optional[TickRecord]:

        for record in self.records:

            if record.tick == tick:

                return record

        return None

    # ======================================================
    # Helpers
    # ======================================================

    def clear(self):

        self.records.clear()

    def __len__(self):

        return len(self.records)

    def __iter__(self):

        return iter(self.records)
