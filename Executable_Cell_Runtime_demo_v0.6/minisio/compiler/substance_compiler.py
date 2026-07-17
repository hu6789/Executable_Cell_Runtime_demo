# minisio/compiler/substance_compiler.py

from typing import Dict, Any, List

from minisio.minisio_schema import (
    OrchestrationRequest,
    MiniSIOOperation
)


class SubstanceCompiler:

    """
    Compile substance requests into LabelCenter intents.
    """

    def __init__(self, schema=None):

        self.schema = schema or {}

    # =====================================================
    # Entry
    # =====================================================

    def compile(

        self,

        requests: List[OrchestrationRequest],

        metadata=None

    ) -> List[Dict[str, Any]]:

        intents = []

        for request in requests:

            if request.operation != MiniSIOOperation.SPAWN_SUBSTANCE:
                continue

            intents.append(

                self._compile_single(request)

            )

        return intents

    # =====================================================
    # Internal
    # =====================================================

    def _compile_single(
        self,
        request: OrchestrationRequest
    ) -> Dict[str, Any]:

        payload = request.payload

        return {
            "intent_id": f"substance_{request.target_id}",
            "operation": request.operation,
            "write_mode": "substance",
            "target_type": request.target_type,
            "target_id": request.target_id,

            # 🔥 FLAT contract
            "substance_type": payload.get("template_id"),
            "position": request.spatial.position if request.spatial else None,
            "amount": payload.get("amount", 1.0),
            "initial_state": payload.get("initial_state", {}),

            "tick": request.temporal.tick if request.temporal else None,
            "source": "MiniSIO",
            "compiler": "substance"
        }
