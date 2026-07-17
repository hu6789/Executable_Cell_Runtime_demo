# minisio/core/router.py

from collections import defaultdict
from typing import Dict, List, Any


# =========================================================
# MiniSIO Router v0.3
# =========================================================

class MiniSIORouter:

    """
    MiniSIO request router.

    Responsibilities
    ----------------
    - group normalized requests by write_mode
    - preserve request ordering
    - prepare compiler batches

    DOES NOT
    --------
    - modify requests
    - infer write modes
    - validate schema
    - compile intents
    - execute simulation
    """

    # =====================================================
    # Public Entry
    # =====================================================

    def route(
        self,
        requests: List[Any]
    ) -> Dict[str, List[Any]]:

        buckets = defaultdict(list)

        for request in requests:

            buckets[
                self._get_write_mode(request)
            ].append(request)

        return dict(buckets)

    # =====================================================
    # Helpers
    # =====================================================

    def _get_write_mode(
        self,
        request: Any
    ) -> str:

        """
        Normalized requests should already contain
        write_mode.

        Unknown modes fall back to runtime_state
        to keep the pipeline robust.
        """

        mode = getattr(
            request,
            "write_mode",
            None
        )

        if mode is None:

            return "runtime_state"

        return mode
