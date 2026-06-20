# minisio/compiler/intent_compiler.py

from typing import List, Dict, Any
from minisio.minisio_schema import (
    OrchestrationRequest,
    MiniSIOOperation
)


class IntentCompiler:

    """
    MiniSIO Compiler v0.3 (STABLE)

    Key Fixes:
        - single canonical compile path
        - strict payload schema
        - no dual interpretation logic
        - IntentBuilder compatibility guaranteed
    """

    def __init__(self, schema=None):
        self.schema = schema or {}
    # =========================================
    # ENTRY
    # =========================================

    def compile(self, requests, metadata=None):

        intents = []

        for i, req in enumerate(requests):

            intent = self._compile_single(req, i)

            if intent is None:
                continue

            # attach metadata (safe layer)
            intent["source"] = "minisio"
            intent["intent_origin"] = "external_orchestration"

            intents.append(intent)

        return intents

    # =========================================
    # SINGLE CANONICAL COMPILER
    # =========================================

    def _compile_single(self, req, i):

        op = req.operation

        # ================================
        # FIELD EMISSION
        # ================================
        if op == MiniSIOOperation.EMIT_FIELD:

            return {
                "intent_id": f"minisio_field_{req.target_id}_{i}",

                # LabelCenter required
                "operation": "add",
                "write_mode": "field",

                "target_type": req.target_type,
                "target_id": req.target_id,

                # ============================
                # CANONICAL PAYLOAD
                # ============================
                "payload": {
                    "type": "field",

                    "field_type": req.payload.get("field_type"),
                    "strength": req.payload.get("field_strength", 1.0),

                    "position": req.spatial.position if req.spatial else None,
                    "radius": req.spatial.radius if req.spatial else None,

                    "tick": req.temporal.tick if req.temporal else None,
                    "delay": req.temporal.delay if req.temporal else None
                }
            }

        # ================================
        # CREATE CELL
        # ================================
        if op == MiniSIOOperation.CREATE_CELL:

            return {
                "intent_id": f"minisio_cell_{req.target_id}_{i}",

                "operation": "add",

                "write_mode": "entity_lifecycle",

                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {

                    "type": "cell",

                    "template_id":
                        req.payload.get("template_id"),

                    "position":
                        req.spatial.position if req.spatial else None,

                    "initial_state":
                        req.payload.get(
                            "initial_state",
                            {}
                        ),

                    "tick":
                        req.temporal.tick if req.temporal else None
                }
            }

        # ================================
        # VIRUS INJECTION
        # ================================
        if op == MiniSIOOperation.INJECT_VIRUS:

            return {
                "intent_id": f"minisio_virus_{req.target_id}_{i}",
                "operation": "add",
                "write_mode": "viral_injection",
                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {
                    "type": "virus",
                    "virus_type": req.payload.get("virus_type"),
                    "load": req.payload.get("load", 1.0),
                    "position": req.spatial.position if req.spatial else None,
                    "tick": req.temporal.tick if req.temporal else None
                }
            }

        # ================================
        # EVENT
        # ================================
        if op == MiniSIOOperation.SCHEDULE_EVENT:

            return {
                "intent_id": f"minisio_event_{req.target_id}_{i}",
                "operation": "add",
                "write_mode": "event",
                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {
                    "type": "event",
                    **req.payload,
                    "tick": req.temporal.tick if req.temporal else None
                }
            }

        return None

    # =========================================
    # WRITE MODE MAP (保留但收敛)
    # =========================================

    def _map_write_mode(self, op):

        if op == "emit_field":
            return "field"

        if op == "create_cell":
            return "cell_state"

        if op == "delete_entity":
            return "entity_lifecycle"

        return "runtime_state"
