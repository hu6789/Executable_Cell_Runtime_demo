# minisio/compiler/event_compiler.py

from typing import List, Dict, Any
from minisio.minisio_schema import MiniSIOOperation


class EventCompiler:

    """
    MiniSIO Event Compiler v0.1

    Responsibility:
        - convert scheduled requests into delayed intents
        - build temporal execution plans
        - support recurring events

    DOES NOT:
        - execute events
        - modify world state
        - validate spatial or target correctness
    """

    # =========================================
    # PUBLIC ENTRY
    # =========================================

    def compile(self, requests, metadata=None):

        event_intents = []

        for i, req in enumerate(requests):

            intent = self._compile_single(req, i)

            if intent is not None:
                event_intents.append(intent)

        return event_intents

    # =========================================
    # SINGLE EVENT COMPILATION
    # =========================================

    def _compile_single(self, req, i):

        # -------------------------------------
        # ONLY HANDLE TEMPORAL EVENTS
        # -------------------------------------

        temporal = getattr(req, "temporal", None)

        if temporal is None:
            return None

        delay = getattr(temporal, "delay", None)
        duration = getattr(temporal, "duration", None)

        # -------------------------------------
        # CASE 1: DELAYED EXECUTION
        # -------------------------------------
        if delay and delay > 0:

            return {
                "intent_id": f"event_delayed_{req.operation}_{req.target_id}_{i}",
                "operation": "schedule",
                "write_mode": "event",

                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {
                    "original_operation": req.operation,
                    "execute_at_tick": temporal.tick + delay,
                    "base_tick": temporal.tick,
                    "payload": req.payload
                },

                "source": "minisio",
                "intent_origin": "event_compiler"
            }

        # -------------------------------------
        # CASE 2: RECURRING EVENT
        # -------------------------------------
        if duration and duration > 0:

            return {
                "intent_id": f"event_recurring_{req.operation}_{req.target_id}_{i}",
                "operation": "schedule_recurring",
                "write_mode": "event",

                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {
                    "original_operation": req.operation,
                    "start_tick": temporal.tick,
                    "duration": duration,
                    "interval": req.payload.get("interval", 1),
                    "payload": req.payload
                },

                "source": "minisio",
                "intent_origin": "event_compiler"
            }

        # -------------------------------------
        # NOT AN EVENT
        # -------------------------------------
        return None
