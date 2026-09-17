import math
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class SHHField:
    """
    Minimal 1D SHH field for the v0.7 demo.

    Each source is represented by:
        cell_id -> (position, amount)

    SHH concentration at a position is the sum of contributions
    from all sources.
    """

    decay_length: float = 1.0
    sources: Dict[str, Tuple[float, float]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if self.decay_length <= 0:
            raise ValueError("decay_length must be positive")

    def set_source(
        self,
        cell_id: str,
        position: float,
        amount: float,
    ) -> None:
        self.sources[cell_id] = (position, amount)

    def remove_source(self, cell_id: str) -> None:
        self.sources.pop(cell_id, None)

    def concentration_at(self, position: float) -> float:
        total = 0.0

        for source_position, amount in self.sources.values():
            distance = abs(position - source_position)

            total += (
                amount
                * math.exp(-distance / self.decay_length)
            )

        return total
