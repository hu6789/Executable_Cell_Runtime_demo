from dataclasses import dataclass, field
from typing import Dict, Set

from internalnet.runtime.state import GeneState, NodeState


@dataclass
class CellState:
    """
    Persistent World state of one cell.

    id is immutable by convention.
    type may change in later stages.
    Graph is derived from type and is not stored here.
    """

    id: str
    type: str

    nodes: Dict[str, NodeState] = field(default_factory=dict)
    genes: Dict[str, GeneState] = field(default_factory=dict)
    labels: Set[str] = field(default_factory=set)


@dataclass
class WorldState:
    """
    Minimal World state for the v0.7 demo.

    Cells are persistent cell states.
    SHH field stores the current extracellular SHH field.
    """

    cells: Dict[str, CellState] = field(default_factory=dict)
    shh_field: object = None
