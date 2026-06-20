# minisio/core/minisio.py

from typing import List, Dict, Any

from minisio.normalizer.request_normalizer import RequestNormalizer
from minisio.compiler.intent_compiler import IntentCompiler
from minisio.minisio_schema import MiniSIOIntentPackage


# =========================================
# MiniSIO Core v0.2
# =========================================

class MiniSIO:

    """
    Responsibilities:
        - orchestrate MiniSIO pipeline
        - ensure stable intent schema
        - isolate normalization vs compilation vs routing

    DOES NOT:
        - execute simulation
        - modify world state
        - decide biological logic
    """

    def __init__(self, schema: Dict[str, Any] = None):

        self.schema = schema or {}

        self.normalizer = RequestNormalizer()
        self.compiler = IntentCompiler(schema=self.schema)

        # ⭐ NEW: routing layer (lightweight but critical)
        self.router = MiniSIORouter()


    # =========================================
    # main entry
    # =========================================

    def receive(
        self,
        raw_requests: List[Dict[str, Any]],
        metadata: Dict[str, Any] = None
    ) -> MiniSIOIntentPackage:

        metadata = metadata or {}

        # -----------------------------
        # 1. normalize
        # -----------------------------
        normalized = self.normalizer.normalize_batch(raw_requests)

        # -----------------------------
        # 2. compile
        # -----------------------------
        compiled_intents = self.compiler.compile(
            normalized,
            metadata=metadata
        )

        # -----------------------------
        # 3. route (NEW STABILITY LAYER)
        # -----------------------------
        routed_intents = self.router.route(
            compiled_intents,
            metadata=metadata
        )

        # -----------------------------
        # 4. package
        # -----------------------------
        return MiniSIOIntentPackage(
            intents=routed_intents,
            metadata={
                "status": "ok",
                "raw_count": len(raw_requests),
                "normalized_count": len(normalized),
                "compiled_count": len(compiled_intents),
                "routed_count": len(routed_intents),
                "source": metadata.get("source", "unknown")
            }
        )


# =========================================
# MiniSIO Router (CRITICAL MISSING PIECE)
# =========================================

class MiniSIORouter:

    """
    Responsibilities:
        - enforce stable intent schema
        - normalize payload fields
        - ensure downstream compatibility (IntentBuilder / LabelCenter)
    """

    def route(
        self,
        intents: List[Dict[str, Any]],
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:

        out = []

        for intent in intents:

            intent = self._normalize_payload(intent)
            intent = self._normalize_write_mode(intent)
            intent = self._attach_metadata(intent, metadata)

            out.append(intent)

        return out


    # -----------------------------------------
    # payload normalization
    # -----------------------------------------

    def _normalize_payload(self, intent: Dict[str, Any]) -> Dict[str, Any]:

        payload = intent.get("payload", {})

        if not isinstance(payload, dict):
            payload = {}

        # unify field naming (VERY IMPORTANT)
        if "field_strength" in payload:
            payload["strength"] = payload.pop("field_strength")

        # unify position key safety
        if "pos" in payload and "position" not in payload:
            payload["position"] = payload.pop("pos")

        intent["payload"] = payload
        return intent


    # -----------------------------------------
    # write mode cleanup hook
    # -----------------------------------------

    def _normalize_write_mode(self, intent: Dict[str, Any]) -> Dict[str, Any]:

        wm = intent.get("write_mode")

        # future-proof normalization hook
        if wm is None:
            intent["write_mode"] = "runtime_state"

        return intent


    # -----------------------------------------
    # metadata tagging
    # -----------------------------------------

    def _attach_metadata(
        self,
        intent: Dict[str, Any],
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        if metadata:
            intent["source_tag"] = metadata.get("source", "minisio")

        intent["pipeline_version"] = "minisio_v0.2"

        return intent
