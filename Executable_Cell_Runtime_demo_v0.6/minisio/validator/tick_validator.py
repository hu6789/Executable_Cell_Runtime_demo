# minisio/validator/tick_validator.py


class TickValidator:

    """
    MiniSIO Tick Validator v0.1

    Responsibility:
        - ensure temporal tick validity
        - prevent invalid or explosive scheduling

    DOES NOT:
        - modify requests
        - interpret semantics
        - validate spatial / payload
    """

    def __init__(self, max_tick=10**6):

        # safety boundary (prevent runaway simulation time)
        self.max_tick = max_tick

    # =========================================
    # PUBLIC API
    # =========================================

    def validate_batch(self, requests):

        valid = []

        for req in requests:

            if self.validate_single(req):
                valid.append(req)

        return valid

    def validate_single(self, req):

        # -----------------------------
        # must have temporal
        # -----------------------------
        if not hasattr(req, "temporal") or req.temporal is None:
            return False

        tick = req.temporal.tick

        # -----------------------------
        # type check
        # -----------------------------
        if tick is None:
            return False

        if not isinstance(tick, int):
            return False

        # -----------------------------
        # range check
        # -----------------------------
        if tick < 0:
            return False

        if tick > self.max_tick:
            return False

        return True
