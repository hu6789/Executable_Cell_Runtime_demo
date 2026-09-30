from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set
from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import GeneState, NodeState

@dataclass(frozen=True)
class BehaviorIntention:
    """
    Base behavior intention calculated by BehaviorEngine.

    This is the pre-HIR-adjustment behavior value.
    """
    behavior_name: str
    value: float
    inputs: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class TFRegulationDelta:
    """
    Delta produced by TF regulation.

    The regulator adjusts a BehaviorIntention but does not
    construct the final BehaviorRuntimeState.
    """
    behavior_name: str
    delta: float


@dataclass(frozen=True)
class ResourceAllocation:
    """
    Result of resource allocation for one behavior.

    Allocation describes how much resource is available/assigned
    to realize the behavior. It does not directly define the
    final behavior value.
    """
    behavior_name: str
    resources: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class ResourceDelta:
    """
    Delta produced by resource realization.

    The resource layer adjusts the TF-adjusted behavior intention
    but does not construct the final BehaviorRuntimeState.
    """
    behavior_name: str
    delta: float


@dataclass(frozen=True)
class BehaviorRuntimeState:
    behavior_name: str
    source_type: str
    source_name: str
    node_states: Dict[str, NodeState] = field(default_factory=dict)
    gene_states: Dict[str, GeneState] = field(default_factory=dict)
    value: float = 0.0
    internal_outputs: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class BehaviorExternalEffect:
    """
    Effect of a behavior that is exposed outside HIR.

    HIR only organizes this result. It does not apply the effect
    to World or LabelCenter.
    """
    behavior_name: str
    effect_type: str
    target: str
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HIROutput:
    """
    Public output of HIR for the current tick.

    ``runtime`` is the final InternalNet runtime snapshot after
    Node, Passive, and Gene stages. HIR does not modify or construct
    this runtime; InternalNet attaches it when the complete pipeline
    finishes.
    """
    runtime: Optional[Runtime] = None
    behaviors: Dict[str, BehaviorRuntimeState] = field(default_factory=dict)
    external_effects: Dict[str, BehaviorExternalEffect] = field(
        default_factory=dict
    )
    labels: Set[str] = field(default_factory=set)
    type_name: Optional[str] = None
