# minisio/minisio_schema.py

# =========================================================
# MiniSIO Schema v0.1
# External Orchestration Layer Contract
# =========================================================

from dataclasses import dataclass
from typing import Any, Dict, Tuple, Optional, List


# =========================================================
# Operation Types
# =========================================================

class MiniSIOOperation:
    """
    All external orchestration operations
    """
    CREATE_CELL = "create_cell"
    INJECT_VIRUS = "inject_virus"
    EMIT_FIELD = "emit_field"
    SPAWN_SUBSTANCE = "spawn_substance"
    MOVE_ENTITY = "move_entity"
    DELETE_ENTITY = "delete_entity"
    SCHEDULE_EVENT = "schedule_event"


# =========================================================
# Spatial Context
# =========================================================

@dataclass
class SpatialContext:
    """
    Spatial binding for all orchestration requests
    """
    position: Tuple[int, int]
    radius: Optional[float] = None
    region: Optional[str] = None


# =========================================================
# Temporal Context
# =========================================================

@dataclass
class TemporalContext:
    """
    Tick-based scheduling context
    """
    tick: int
    delay: Optional[int] = None
    duration: Optional[int] = None


# =========================================================
# Core Orchestration Request
# =========================================================

@dataclass
class OrchestrationRequest:
    """
    Unified external simulation command
    """

    # -----------------------------
    # operation
    # -----------------------------
    operation: str

    # -----------------------------
    # target
    # -----------------------------
    target_type: str            # cell / virus / substance / field
    target_id: Optional[str] = None

    # -----------------------------
    # context
    # -----------------------------
    spatial: Optional[SpatialContext] = None
    temporal: Optional[TemporalContext] = None

    # -----------------------------
    # payload
    # -----------------------------
    payload: Dict[str, Any] = None

    # -----------------------------
    # scheduling mode
    # -----------------------------
    schedule_mode: str = "immediate"  # immediate / delayed / recurring


    def __post_init__(self):
        if self.payload is None:
            self.payload = {}


# =========================================================
# Specialized Requests
# =========================================================

@dataclass
class CellInjectionRequest:
    """
    Create cell in world
    """
    template_id: str
    cell_id: str
    position: Tuple[int, int]
    tick: int
    initial_state: Dict[str, Any]


@dataclass
class ViralInjectionRequest:
    """
    Infect or inject virus into system
    """
    virus_type: str
    tick: int

    target_cell_id: Optional[str] = None
    position: Optional[Tuple[int, int]] = None

    load: float = 1.0


@dataclass
class FieldEmissionRequest:
    """
    Emit field/substance into world
    """
    field_type: str
    position: Tuple[int, int]
    radius: float
    tick: int
    strength: float


# =========================================================
# MiniSIO Output Package
# =========================================================

@dataclass
class MiniSIOIntentPackage:
    """
    Output compiled intents for IntentBuilder
    """
    intents: List[Dict[str, Any]]
    metadata: Dict[str, Any]
