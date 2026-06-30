# demo/observer/statistics.py

"""
=========================================================
Runtime Statistics
=========================================================

Compute runtime statistics from StateSnapshot.

Responsibilities
----------------
- summarize snapshot data
- compute lightweight runtime metrics
- provide observer-friendly statistics

DOES NOT
--------
- access SimulationWorld
- modify snapshots
- store history
- print output
"""

from dataclasses import dataclass, field
from typing import Dict, Any


# ==========================================================
# Statistics Result
# ==========================================================

@dataclass
class RuntimeStatistics:

    tick: int

    cell_count: int = 0

    substance_count: int = 0

    field_count: int = 0

    average_runtime_state: Dict[str, float] = field(
        default_factory=dict
    )

    cells_by_template: Dict[str, int] = field(
        default_factory=dict
    )

    substances_by_type: Dict[str, int] = field(
        default_factory=dict
    )

    total_field_strength: Dict[str, float] = field(
        default_factory=dict
    )


# ==========================================================
# Statistics
# ==========================================================

class Statistics:

    """
    Compute observer statistics.

    Input:
        StateSnapshot

    Output:
        RuntimeStatistics
    """

    # ======================================================
    # Public
    # ======================================================

    def compute(

        self,

        snapshot

    ) -> RuntimeStatistics:

        stats = RuntimeStatistics(

            tick=snapshot.tick,

            cell_count=len(snapshot.cells),

            substance_count=len(snapshot.substances),

            field_count=len(snapshot.fields)

        )

        stats.cells_by_template = (
            self._count_templates(snapshot)
        )

        stats.substances_by_type = (
            self._count_substances(snapshot)
        )

        stats.average_runtime_state = (
            self._average_runtime_state(snapshot)
        )

        stats.total_field_strength = (
            self._field_strength(snapshot)
        )

        return stats

    # ======================================================
    # Cell
    # ======================================================

    def _count_templates(

        self,

        snapshot

    ):

        result = {}

        for cell in snapshot.cells.values():

            template = cell.get(
                "template_id",
                "unknown"
            )

            result[template] = (

                result.get(template, 0) + 1

            )

        return result

    # ======================================================
    # Substance
    # ======================================================

    def _count_substances(

        self,

        snapshot

    ):

        result = {}

        for substance in snapshot.substances.values():

            subtype = substance.get(

                "substance_type",

                "unknown"

            )

            result[subtype] = (

                result.get(subtype, 0) + 1

            )

        return result

    # ======================================================
    # Runtime State
    # ======================================================

    def _average_runtime_state(

        self,

        snapshot

    ):

        totals = {}

        counts = {}

        for cell in snapshot.cells.values():

            runtime = cell.get(

                "runtime_state",

                {}

            )

            for key, value in runtime.items():

                if not isinstance(

                    value,

                    (int, float)

                ):

                    continue

                totals[key] = (

                    totals.get(key, 0.0)

                    + value

                )

                counts[key] = (

                    counts.get(key, 0)

                    + 1

                )

        averages = {}

        for key in totals:

            averages[key] = (

                totals[key]

                / counts[key]

            )

        return averages

    # ======================================================
    # Fields
    # ======================================================

    def _field_strength(

        self,

        snapshot

    ):

        result = {}

        for field_name, values in snapshot.fields.items():

            result[field_name] = sum(

                values.values()

            )

        return result
