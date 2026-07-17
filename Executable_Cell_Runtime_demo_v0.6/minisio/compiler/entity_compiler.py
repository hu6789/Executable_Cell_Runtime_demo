# minisio/compiler/entity_compiler.py

from typing import Any, Dict, List


# =========================================================
# Entity Compiler v0.7 (patched for LabelCenter v0.7)
# =========================================================

class EntityCompiler:

    """
    Entity Compiler

    Responsibilities
    ----------------
    - compile entity lifecycle requests
    - normalize operation semantics
    - generate LabelCenter-compatible entity intents

    DOES NOT
    --------
    - create entities
    - modify world
    - validate biology
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

        metadata = metadata or {}
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
    # Operation normalize (IMPORTANT)
    # =====================================================

    def _normalize_operation(self, op: str) -> str:

        if op is None:
            return "create"

        mapping = {

            "create_cell": "create",
            "create_entity": "create",

            "delete_entity": "destroy",
            "remove_cell": "destroy",

            "transform_entity": "transform",
            "update_entity": "transform"

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

        spatial = getattr(request, "spatial", None)
        temporal = getattr(request, "temporal", None)

        # -----------------------------------------
        # spatial fallback (important)
        # -----------------------------------------
        if spatial is not None:

            payload.setdefault("position", spatial.position)
            payload.setdefault("radius", spatial.radius)
            payload.setdefault("region", spatial.region)

        # -----------------------------------------
        # operation normalization
        # -----------------------------------------
        operation = self._normalize_operation(
            getattr(request, "operation", None)
        )

        # -----------------------------------------
        # IMPORTANT: ensure identity fields exist
        # -----------------------------------------
        target_id = getattr(request, "target_id", None)
        target_type = getattr(request, "target_type", "cell")

        # fallback: allow payload override
        if target_id is None:
            target_id = payload.get("cell_id") or payload.get("id")

        # -----------------------------------------
        # tick safety (CRITICAL FIX)
        # -----------------------------------------
        tick = None
        if temporal is not None:
            tick = temporal.tick

        if tick is None:
            tick = payload.get("tick")

        # -----------------------------------------
        # build intent
        # -----------------------------------------
        return {

            "intent_id": f"entity_{index}",

            "operation": operation,

            "write_mode": "entity",

            "target_type": target_type,

            "target_id": target_id,

            "payload": payload,

            "tick": tick if tick is not None else 0,

            "source": metadata.get("source", "MiniSIO"),

            "compiler": "entity"

        }
