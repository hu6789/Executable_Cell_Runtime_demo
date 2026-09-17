
# compute_plan/schema.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from internalnet.graph_engine.schema import GraphEdge


@dataclass(frozen=True)
class CellComputePlan:
    """Resolved computation plan for one cell.

    The plan is generated from the cell's graph structure.
    It describes the structural candidates, relationships,
    and resolved execution dependencies available to the cell.

    The plan does not execute biological calculations.
    """

    cell_id: str

    graph_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )

    candidate_nodes: Tuple[str, ...] = field(
        default_factory=tuple
    )

    candidate_genes: Tuple[str, ...] = field(
        default_factory=tuple
    )

    candidate_behaviors: Tuple[str, ...] = field(
        default_factory=tuple
    )

    edges: Tuple[GraphEdge, ...] = field(
        default_factory=tuple
    )

    node_execution_order: Tuple[str, ...] = field(
        default_factory=tuple
    )

