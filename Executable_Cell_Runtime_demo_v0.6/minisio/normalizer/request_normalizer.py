# minisio/normalizer/request_normalizer.py

"""
MiniSIO Request Normalizer

Responsibilities
----------------
- validate external requests
- normalize raw dict -> OrchestrationRequest
- build spatial / temporal contexts
- provide unified request objects for compiler stage

DOES NOT
---------
- compile intents
- execute simulation
- modify world state
"""

from typing import Dict, List, Optional

from minisio.minisio_schema import (
    OrchestrationRequest,
    SpatialContext,
    TemporalContext,
)


# =========================================================
# Request Normalizer
# =========================================================

class RequestNormalizer:

    # =====================================================
    # batch
    # =====================================================

    def normalize_batch(
        self,
        raw_requests: List[Dict]
    ) -> List[OrchestrationRequest]:

        normalized = []

        for request in raw_requests:

            try:

                obj = self.normalize_single(request)

                if obj is not None:
                    normalized.append(obj)

            except Exception as e:

                print(
                    f"[MiniSIO] rejected request: {e}"
                )

        return normalized

    # =====================================================
    # single
    # =====================================================

    def normalize_single(
        self,
        request: Dict
    ) -> Optional[OrchestrationRequest]:

        if not isinstance(request, dict):
            raise ValueError(
                "request must be dict"
            )

        operation = request.get("operation")

        if operation is None:
            raise ValueError(
                "missing operation"
            )

        payload = request.get("payload") or {}

        if not isinstance(payload, dict):
            raise ValueError(
                "payload must be dict"
            )

        return OrchestrationRequest(

            operation=operation,

            write_mode=request.get(
                "write_mode",
                "runtime_state"
            ),

            source=request.get(
                "source",
                "external"
            ),

            target_type=request.get(
                "target_type",
                "unknown"
            ),

            target_id=request.get(
                "target_id"
            ),

            spatial=self._build_spatial(
                request
            ),

            temporal=self._build_temporal(
                request
            ),

            payload=payload,

            schedule_mode=request.get(
                "schedule_mode",
                "immediate"
            )
        )

    # =====================================================
    # spatial
    # =====================================================

    def _build_spatial(
        self,
        request: Dict
    ) -> Optional[SpatialContext]:

        payload = request.get(
            "payload",
            {}
        )

        position = (
            request.get("position")
            or payload.get("position")
        )

        if position is None:
            return None

        return SpatialContext(

            position=(
                int(position[0]),
                int(position[1])
            ),

            radius=request.get("radius"),

            region=request.get("region")
        )

    # =====================================================
    # temporal
    # =====================================================

    def _build_temporal(
        self,
        request: Dict
    ) -> TemporalContext:

        payload = request.get(
            "payload",
            {}
        )

        tick = (
            request.get("tick")
            or payload.get("tick")
        )

        if tick is None:
            raise ValueError(
                "missing tick"
            )

        return TemporalContext(

            tick=int(tick),

            delay=request.get("delay"),

            duration=request.get("duration")
        )
