# internalnet/node_engine/schema.py

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class NodeDefinition:
    name: str
    category: str
    polymorphism: List[str] = field(default_factory=list)
    half_life: Optional[float] = None
    diffusion: Optional[float] = None
    diffusion_source_states: List[str] = field(
        default_factory=list
    )
    formulation: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class NodeInput:
    node_name: str
    total: float
    states: Dict[str, float] = field(default_factory=dict)
    related_inputs: Dict[str, Dict[str, Any]] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class NodeRuntimeState:
    node_name: str
    total: float
    states: Dict[str, float] = field(default_factory=dict)
