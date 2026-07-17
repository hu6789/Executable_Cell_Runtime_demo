# minisio/compiler/event_compiler.py

from typing import Any, Dict, List


class EventCompiler:
    """
    MiniSIO Event Compiler v0.2

    Responsibilities
    ----------------
    - compile delayed / scheduled requests
    - generate canonical event requests
    - provide LabelCenter-compatible event package

    DOES NOT
    ----------------
    - execute events
    - modify world
    - create runtime/entity intents
    """

    def compile(
        self,
        requests: List[Any],
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:

        metadata = metadata or {}
        events = []

        for request in requests:
            events.append(
                self._compile_single(request, metadata)
            )

        return events


    def _compile_single(self, request, metadata=None):

        temporal = request.temporal

        return {
            "intent_id": f"event_{request.target_id}",
            "operation": request.operation,

            # 🔥 CRITICAL: LabelCenter routing key
            "write_mode": "event",

            "target_type": request.target_type,
            "target_id": request.target_id,

            # --------------------------
            # flat event fields
            # --------------------------
            "tick": temporal.tick if temporal else None,
            "delay": temporal.delay if temporal else None,
            "duration": temporal.duration if temporal else None,

            "schedule_mode": request.schedule_mode,

            "payload": request.payload,

            "source": (metadata or {}).get("source", "MiniSIO"),
            "compiler": "event"
        }
