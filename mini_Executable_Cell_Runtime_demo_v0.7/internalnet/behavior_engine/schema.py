# internalnet/behavior_engine/schema.py

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class BehaviorDefinition:
    """Static definition of a behavior."""

    name: str
    category: Optional[str] = None
    formula: Dict[str, Any] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)
    internal_outputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BehaviorIntention:
    behavior_name: str
    value: float
    inputs: Dict[str, float] = field(default_factory=dict)
    internal_outputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BehaviorRuntimeState:
    """Final runtime state of a behavior."""

    behavior_name: str
    intention: float
    value: float
