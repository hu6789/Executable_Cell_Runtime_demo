# minisio/minisio_schema.py

"""
=========================================================
MiniSIO Schema v0.7
=========================================================

Unified Runtime Request Contract

MiniSIO Responsibilities
------------------------
External Request
        ↓
Normalization
        ↓
Compiler
        ↓
LabelCenter Intent

MiniSIO never executes world updates.
MiniSIO only translates external requests.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# =========================================================
# Operations
# =========================================================

class MiniSIOOperation:
    """
    High-level operations accepted by MiniSIO.

    Operations describe user intent.

    Compilers decide how they become LabelCenter intents.
    """

    # -----------------------------------------------------
    # Runtime
    # -----------------------------------------------------

    SET_RUNTIME = "set_runtime"

    # -----------------------------------------------------
    # Entity
    # -----------------------------------------------------

    CREATE_CELL = "create_cell"

    CREATE_SUBSTANCE = "create_substance"

    CREATE_VIRUS = "create_virus"

    DELETE_ENTITY = "delete_entity"

    TRANSFORM_ENTITY = "transform_entity"

    MOVE_ENTITY = "move_entity"

    # -----------------------------------------------------
    # Field
    # -----------------------------------------------------

    EMIT_FIELD = "emit_field"

    # -----------------------------------------------------
    # Event
    # -----------------------------------------------------

    SCHEDULE_EVENT = "schedule_event"

    # -----------------------------------------------------
    # Compatibility
    # -----------------------------------------------------

    INJECT_VIRUS = CREATE_VIRUS

    SPAWN_SUBSTANCE = CREATE_SUBSTANCE


# =========================================================
# Write Modes
# =========================================================

class MiniSIOWriteMode:
    """
    LabelCenter dispatch buckets.
    """

    RUNTIME_STATE = "runtime_state"

    FIELD = "field"

    ENTITY = "entity"

    EVENT = "event"


# =========================================================
# Spatial Context
# =========================================================

@dataclass
class SpatialContext:

    position: Tuple[int, int]

    radius: Optional[float] = None

    region: Optional[str] = None


# =========================================================
# Temporal Context
# =========================================================

@dataclass
class TemporalContext:

    tick: int

    delay: Optional[int] = None

    duration: Optional[int] = None


# =========================================================
# Unified Runtime Request
# =========================================================

@dataclass
class OrchestrationRequest:
    """
    Normalized request entering MiniSIO.

    This object is compiler-facing.

    It is intentionally independent from
    LabelCenter Intent format.
    """

    # required

    operation: str

    write_mode: str

    # source

    source: str = "external"

    # target

    target_type: str = "unknown"

    target_id: Optional[str] = None

    # contexts

    spatial: Optional[SpatialContext] = None

    temporal: Optional[TemporalContext] = None

    # operation payload

    payload: Dict[str, Any] = field(default_factory=dict)

    # scheduling

    schedule_mode: str = "immediate"


# =========================================================
# Compiler Output Package
# =========================================================

@dataclass
class MiniSIORequestPackage:
    """
    Output produced by MiniSIO.

    These requests are already compiled
    into LabelCenter-compatible intents.
    """

    requests: List[Dict[str, Any]]

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __len__(self):

        return len(self.requests)

    def __iter__(self):

        return iter(self.requests)

    def is_empty(self):

        return len(self.requests) == 0
