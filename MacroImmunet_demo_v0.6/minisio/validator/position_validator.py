# minisio/validator/position_validator.py

from typing import Optional, Tuple, Any


class PositionValidator:

    """
    MiniSIO Position Validator v0.1

    Responsibility:
        - validate spatial position integrity
        - ensure safe world-bound writes
        - prevent spatial explosion

    DOES NOT:
        - modify coordinates
        - infer missing position
        - apply routing logic
    """

    def __init__(self, world_width=50, world_height=50, max_radius=50):

        self.world_width = world_width
        self.world_height = world_height
        self.max_radius = max_radius

    # =========================================
    # batch API
    # =========================================

    def validate_batch(self, requests):

        return [r for r in requests if self.validate_single(r)]

    # =========================================
    # single validation
    # =========================================

    def validate_single(self, req) -> bool:

        spatial = getattr(req, "spatial", None)

        if spatial is None:
            # allow non-spatial requests (e.g. lifecycle)
            return True

        pos = spatial.position

        # -----------------------------
        # type check
        # -----------------------------
        if pos is None:
            return False

        if not isinstance(pos, (tuple, list)):
            return False

        if len(pos) != 2:
            return False

        x, y = pos

        # -----------------------------
        # numeric check
        # -----------------------------
        try:
            x = float(x)
            y = float(y)
        except Exception:
            return False

        # NaN / inf guard
        if x != x or y != y:
            return False

        if x == float("inf") or y == float("inf"):
            return False

        # -----------------------------
        # bounds check
        # -----------------------------
        if x < 0 or y < 0:
            return False

        if x > self.world_width or y > self.world_height:
            return False

        # -----------------------------
        # radius check
        # -----------------------------
        radius = getattr(spatial, "radius", None)

        if radius is not None:

            try:
                radius = float(radius)
            except Exception:
                return False

            if radius < 0:
                return False

            if radius > self.max_radius:
                return False

        return True
