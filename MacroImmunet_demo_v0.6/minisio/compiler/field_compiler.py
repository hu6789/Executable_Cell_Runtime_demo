# minisio/compiler/field_compiler.py

from typing import Any, Dict, List


# =========================================================
# Field Compiler v0.6
# =========================================================

class FieldCompiler:

    """
    Field Compiler

    Responsibilities
    ----------------
    - compile field write requests
    - generate LabelCenter-compatible field intents
    - preserve field payload

    DOES NOT
    --------
    - execute diffusion
    - calculate field dynamics
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
    # Single Request
    # =====================================================

    def _compile_single(
        self,
        request,
        index,
        metadata
    ) -> Dict[str, Any]:

        payload = dict(request.payload)

        # -----------------------------
        # spatial flatten
        # -----------------------------
        position = None

        if request.spatial is not None:
            position = request.spatial.position
        else:
            position = payload.get("position")
 
        # -----------------------------
        # field semantic extraction
        # -----------------------------
        field_type = payload.get("field_type") or request.target_id

        # ⚠️ unify strength → amount（关键修复点）
        amount = payload.get("amount")
        if amount is None:
            amount = payload.get("strength", 0.0)

        radius = payload.get("radius")
        region = payload.get("region")

        # -----------------------------
        # FINAL FLAT WRITE (IMPORTANT)
        # -----------------------------
        return {
            "intent_id": f"field_{index}",
            "operation": request.operation,
            "write_mode": "field",
            "target_type": request.target_type,
            "target_id": request.target_id,

            # 🔥 FLAT SCHEMA (LabelCenter needs this)
            "field_type": field_type,
            "position": position,
            "amount": amount,
            "radius": radius,
            "region": region,

            "tick": request.temporal.tick if request.temporal else None,
    
            "source": metadata.get("source", "MiniSIO"),
            "compiler": "field"
        }
