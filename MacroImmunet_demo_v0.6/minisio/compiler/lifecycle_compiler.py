# minisio/compiler/lifecycle_compiler.py

from typing import Dict, Any, List
from minisio.minisio_schema import MiniSIOOperation


class LifecycleCompiler:

    """
    MiniSIO Lifecycle Compiler v0.1

    Responsibility:
        - convert lifecycle-related requests into LabelCenter intents
        - handle entity creation / deletion / state transitions

    DOES NOT:
        - handle field / signal logic
        - perform physics or diffusion
        - validate input schema
    """

    # =========================================
    # PUBLIC ENTRY
    # =========================================

    def compile(self, requests, metadata=None):

        intents = []

        for i, req in enumerate(requests):

            intent = self._compile_single(req, i)

            if intent is not None:
                intents.append(intent)

        return intents

    # =========================================
    # SINGLE COMPILATION
    # =========================================

    def _compile_single(self, req, i):

        op = req.operation

        # ---------------------------------
        # CREATE CELL
        # ---------------------------------
        if op == MiniSIOOperation.CREATE_CELL:

            return {

                "intent_id": f"lifecycle_create_{req.target_id}_{i}",

                "operation": "add",

                "write_mode": "entity_lifecycle",

                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {

                    "entity_type": "cell",

                    "template_id":
                        req.payload.get("template_id"),

                    "cell_id":
                        req.payload.get(
                            "cell_id",
                            req.target_id
                        ),

                    "position":
                        self._get_position(req),

                    "initial_state":
                        req.payload.get(
                            "initial_state",
                                    {}
                        )
                },

                "source": "minisio",
                "intent_origin": "lifecycle_compiler"
            }

        # ---------------------------------
        # DELETE ENTITY
        # ---------------------------------
        if op == MiniSIOOperation.DELETE_ENTITY:

            return {
                "intent_id": f"lifecycle_delete_{req.target_id}_{i}",
                "operation": "remove",
                "write_mode": "entity_lifecycle",

                "target_type": req.target_type,
                "target_id": req.target_id,

                "payload": {
                    "reason": req.payload.get("reason", "unspecified"),
                    "tick": req.temporal.tick if req.temporal else None
                },

                "source": "minisio",
                "intent_origin": "lifecycle_compiler"
            }

        # ---------------------------------
        # STATE TRANSITION
        # ---------------------------------
        if op == MiniSIOOperation.SCHEDULE_EVENT:

            # lifecycle can also piggyback event-style transitions
            if req.payload.get("lifecycle_transition"):

                return {
                    "intent_id": f"lifecycle_transition_{req.target_id}_{i}",
                    "operation": "update",
                    "write_mode": "cell_state",

                    "target_type": req.target_type,
                    "target_id": req.target_id,

                    "payload": {
                        "from": req.payload.get("from_state"),
                        "to": req.payload.get("to_state"),
                        "tick": req.temporal.tick if req.temporal else None
                    },

                    "source": "minisio",
                    "intent_origin": "lifecycle_compiler"
                }

        return None

    # =========================================
    # HELPERS
    # =========================================

    def _get_position(self, req):

        if req.spatial is None:
            return None

        return req.spatial.position
