# minisio/normalizer/spatial_normalizer.py

from typing import Any, Dict, Optional, Tuple


class SpatialNormalizer:

    """
    MiniSIO Spatial Normalizer v0.1

    Responsibility:
        - unify spatial representation
        - extract position / radius / region from mixed inputs
        - guarantee LabelCenter-compatible structure

    DOES NOT:
        - validate world bounds
        - modify semantics
    """

    # =========================================
    # PUBLIC API
    # =========================================

    def normalize(self, req: Dict[str, Any]) -> Optional[Dict[str, Any]]:

        if not isinstance(req, dict):
            return None

        position = self._extract_position(req)

        if position is None:
            return None

        radius = self._extract_radius(req)
        region = req.get("region")

        return {
            "position": (int(position[0]), int(position[1])),
            "radius": radius,
            "region": region
        }

    # =========================================
    # POSITION
    # =========================================

    def _extract_position(self, req: Dict[str, Any]) -> Optional[Tuple[int, int]]:

        # 1. root level
        if "position" in req:
            return req["position"]

        # 2. payload level
        payload = req.get("payload", {})
        if isinstance(payload, dict) and "position" in payload:
            return payload["position"]

        return None

    # =========================================
    # RADIUS (统一 distance / radius / field range)
    # =========================================

    def _extract_radius(self, req: Dict[str, Any]) -> Optional[float]:

        # direct radius
        if "radius" in req:
            return req["radius"]

        payload = req.get("payload", {})

        if not isinstance(payload, dict):
            return None

        # field systems often use "distance" as radius proxy
        if "radius" in payload:
            return payload["radius"]

        if "distance" in payload:
            return float(payload["distance"])

        # some systems encode field strength scaling as proxy (optional hook)
        return None
