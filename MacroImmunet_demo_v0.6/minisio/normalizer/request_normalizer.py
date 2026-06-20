# minisio/normalizer/request_normalizer.py

# =========================================================
# MiniSIO Request Normalizer v0.1
# =========================================================

from typing import Any, Dict, List, Optional
from dataclasses import asdict

from minisio.minisio_schema import (
    OrchestrationRequest,
    SpatialContext,
    TemporalContext,
    MiniSIOOperation
)


# =========================================================
# Request Normalizer
# =========================================================

class RequestNormalizer:

    """
    Responsibilities:
        - normalize raw external dict -> OrchestrationRequest
        - enforce schema correctness
        - fill missing spatial/temporal fields
        - reject invalid operations

    DOES NOT:
        - compile intents
        - execute simulation logic
        - modify world
    """

    # =========================================
    # public entry
    # =========================================

    def normalize_batch(
        self,
        raw_requests: List[Dict[str, Any]]
    ) -> List[OrchestrationRequest]:

        normalized = []

        for req in raw_requests:

            try:
                obj = self.normalize_single(req)

                if obj is None:
                    continue

                normalized.append(obj)

            except Exception as e:

                print(f"[MiniSIO] rejected request: {e}")

        return normalized


    # =========================================
    # normalize single request
    # =========================================

    def normalize_single(
        self,
        req: Dict[str, Any]
    ) -> Optional[OrchestrationRequest]:

        if not isinstance(req, dict):
            raise ValueError("request must be dict")

        # -----------------------------
        # operation validation
        # -----------------------------
        operation = req.get("operation")

        if operation is None:
            raise ValueError("missing operation")

        if not self._is_valid_operation(operation):
            raise ValueError(f"invalid operation: {operation}")

        # -----------------------------
        # target
        # -----------------------------
        target_type = req.get("target_type", "unknown")
        target_id = req.get("target_id", None)

        # -----------------------------
        # payload
        # -----------------------------
        payload = req.get("payload", {})

        if payload is None:
            payload = {}

        if not isinstance(payload, dict):
            raise ValueError("payload must be dict")

        # -----------------------------
        # spatial normalization
        # -----------------------------
        spatial = self._build_spatial(req)

        # -----------------------------
        # temporal normalization (IMPORTANT)
        # -----------------------------
        temporal = self._build_temporal(req)

        # -----------------------------
        # schedule mode
        # -----------------------------
        schedule_mode = req.get("schedule_mode", "immediate")

        if schedule_mode not in ["immediate", "delayed", "recurring"]:
            schedule_mode = "immediate"

        # -----------------------------
        # build final object
        # -----------------------------
        return OrchestrationRequest(
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            spatial=spatial,
            temporal=temporal,
            payload=payload,
            schedule_mode=schedule_mode
        )


    # =========================================
    # spatial builder
    # =========================================

    def _build_spatial(self, req: Dict[str, Any]) -> Optional[SpatialContext]:

        position = req.get("position")

        # allow payload fallback (but normalize it)
        if position is None:
            payload = req.get("payload", {})
            position = payload.get("position")

        if position is None:
            return None

        if not isinstance(position, (tuple, list)) or len(position) != 2:
            raise ValueError(f"invalid position: {position}")

        return SpatialContext(
            position=(int(position[0]), int(position[1])),
            radius=req.get("radius"),
            region=req.get("region")
        )


    # =========================================
    # temporal builder
    # =========================================

    def _build_temporal(self, req: Dict[str, Any]) -> TemporalContext:

        tick = req.get("tick")

        # fallback: payload tick
        if tick is None:
            payload = req.get("payload", {})
            tick = payload.get("tick")

        if tick is None:
            raise ValueError("missing tick")

        return TemporalContext(
            tick=int(tick),
            delay=req.get("delay"),
            duration=req.get("duration")
        )


    # =========================================
    # operation validator
    # =========================================

    def _is_valid_operation(self, op: str) -> bool:

        valid_ops = {
            MiniSIOOperation.CREATE_CELL,
            MiniSIOOperation.INJECT_VIRUS,
            MiniSIOOperation.EMIT_FIELD,
            MiniSIOOperation.SPAWN_SUBSTANCE,
            MiniSIOOperation.MOVE_ENTITY,
            MiniSIOOperation.DELETE_ENTITY,
            MiniSIOOperation.SCHEDULE_EVENT
        }

        return op in valid_ops
