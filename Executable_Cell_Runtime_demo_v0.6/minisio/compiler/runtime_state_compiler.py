# minisio/compiler/runtime_state_compiler.py

from typing import Dict, Any, List


# =========================================================
# Runtime State Compiler v0.7 (patched)
# =========================================================

class RuntimeStateCompiler:

    """
    RuntimeState Compiler

    Responsibilities
    ----------------
    - normalize runtime state updates
    - ensure tick safety
    - merge flat + payload state fields
    - generate LabelCenter-compatible intents

    DOES NOT
    --------
    - execute updates
    - interpret biology
    """

    def __init__(self, schema=None):
        self.schema = schema or {}

    # =====================================================
    # Public Entry
    # =====================================================

    def compile(
        self,
        requests: List[Any],
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:

        metadata = metadata or []
        intents = []

        for index, request in enumerate(requests):

            intent = self._compile_single(
                request,
                index,
                metadata
            )

            if intent is not None:
                intents.append(intent)

        return intents

    # =====================================================
    # operation normalize
    # =====================================================

    def _normalize_operation(self, op: str) -> str:

        if op is None:
            return "update"

        mapping = {

            "set_runtime": "update",
            "update_runtime": "update",
            "modify_state": "update",

            "create_state": "create",
            "delete_state": "destroy"

        }

        return mapping.get(op, op)

    # =====================================================
    # Single Request
    # =====================================================

    def _compile_single(
        self,
        request,
        index,
        metadata
    ) -> Dict[str, Any]:

        payload = dict(getattr(request, "payload", {}) or {})

        # -----------------------------------------
        # merge root-level state fields (IMPORTANT)
        # -----------------------------------------
        for k in [
            "ATP", "ROS",
            "viral_signal",
            "IFNGR_activation"
        ]:
            if hasattr(request, k):
                payload.setdefault(k, getattr(request, k))

        # -----------------------------------------
        # tick safety (CRITICAL FIX)
        # -----------------------------------------
        tick = None
        if request.temporal is not None:
            tick = request.temporal.tick

        if tick is None:
            tick = payload.get("tick")

        if tick is None:
            tick = 0

        # -----------------------------------------
        # operation normalize
        # -----------------------------------------
        operation = self._normalize_operation(
            getattr(request, "operation", None)
        )

        # -----------------------------------------
        # build intent
        # -----------------------------------------
        return {

            "intent_id": f"runtime_state_{index}",

            "operation": operation,

            "write_mode": "runtime_state",

            "target_type": getattr(request, "target_type", "cell"),

            "target_id": getattr(request, "target_id", None),

            "payload": payload,

            "tick": tick,

            "source": metadata.get("source", "MiniSIO"),

            "compiler": "runtime_state"
        }
