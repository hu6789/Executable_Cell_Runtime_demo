from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class NodeState:
    """
    Runtime data for one Node.

    NodeState stores the actual state of the Node.
    """

    name: str
    total: float
    states: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class GeneState:
    """
    Runtime data for one Gene.

    GeneState stores the actual state of the Gene.
    """

    name: str
    baseline: float
    value: float
    modifications: Dict[str, float] = field(
        default_factory=dict
    )
