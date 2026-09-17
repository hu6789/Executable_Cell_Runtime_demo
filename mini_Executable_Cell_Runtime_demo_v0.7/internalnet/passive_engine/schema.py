# internalnet/passive_engine/schema.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PassiveDefinition:
    """Definition of a passive dynamic.

    A passive definition describes a reusable passive formula
    and how its result should affect node runtime state.
    """

    name: str
    applies_to: list[str] = field(default_factory=list)
    formula: dict[str, Any] = field(default_factory=dict)
    update: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PassiveRuntimeState:
    """State changes produced by one passive calculation.

    This is a state patch, not a replacement NodeRuntimeState.
    It does not mutate the original node runtime state.
    """

    node_name: str
    passive_name: str
    state_changes: dict[str, float] = field(default_factory=dict)
