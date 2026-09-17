from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class NodeDelta:
    """
    Delta produced by NodeEngine.

    source tells which engine generated this change.
    """

    source: str
    node_name: str

    total_delta: float = 0.0

    state_deltas: Dict[str, float] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class PassiveDelta:
    """
    Delta produced by PassiveEngine.
    """

    source: str

    passive_name: str

    node_name: str

    total_delta: float = 0.0

    state_deltas: Dict[str, float] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class GeneDelta:
    """
    Delta produced by GeneEngine.
    """

    source: str
    gene_name: str

    value_delta: float = 0.0

    modification_deltas: Dict[str, float] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class BehaviorInternalDelta:
    """
    Internal Runtime changes produced by BehaviorEngine.

    Behavior may modify both Node and Gene states.
    """

    source: str
    behavior_name: str

    node_deltas: Dict[str, NodeDelta] = field(
        default_factory=dict
    )

    gene_deltas: Dict[str, GeneDelta] = field(
        default_factory=dict
    )
