# minisio/core/router.py

from typing import List, Dict, Any


class MiniSIORouter:

    """
    MiniSIO Router v0.1

    Responsibility:
        - route normalized requests to proper compiler pipelines
        - split multi-domain requests
        - preserve original request structure

    DOES NOT:
        - modify request content
        - validate schema
        - compile intents
    """

    # =========================================
    # PUBLIC ENTRY
    # =========================================

    def route(self, requests: List[Any]) -> Dict[str, List[Any]]:

        intent_requests = []
        event_requests = []
        lifecycle_requests = []

        for req in requests:

            routes = self._classify(req)

            if "intent" in routes:
                intent_requests.append(req)

            if "event" in routes:
                event_requests.append(req)

            if "lifecycle" in routes:
                lifecycle_requests.append(req)

        return {
            "intent": intent_requests,
            "event": event_requests,
            "lifecycle": lifecycle_requests
        }

    # =========================================
    # CLASSIFICATION LOGIC
    # =========================================

    def _classify(self, req):

        op = getattr(req, "operation", None)

        if op is None:
            return []

        routes = []

        # -------------------------------------
        # FIELD / SIGNAL / INTERACTION
        # -------------------------------------
        if op in ["emit_field", "spawn_substance", "move_entity"]:

            routes.append("intent")

        # -------------------------------------
        # LIFECYCLE EVENTS
        # -------------------------------------
        if op in ["create_cell", "delete_entity"]:

            routes.append("lifecycle")

        # -------------------------------------
        # TEMPORAL EVENTS
        # -------------------------------------
        temporal = getattr(req, "temporal", None)

        if temporal:

            delay = getattr(temporal, "delay", None)
            duration = getattr(temporal, "duration", None)

            if delay or duration:

                routes.append("event")

        # -------------------------------------
        # DEFAULT FALLBACK
        # -------------------------------------
        if not routes:

            routes.append("intent")

        return routes
