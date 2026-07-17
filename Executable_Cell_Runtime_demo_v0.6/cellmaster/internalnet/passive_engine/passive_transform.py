# cellmaster/internalnet/passive_engine/passive_transform.py

import math


# =========================================
# Passive Runtime Transform
# =========================================

def apply_passive_transform(
    passive_definition,
    value,
    runtime_context
):
    """
    apply post-processing to passive output

    responsibilities:
        - shape physiological signal
        - stabilize numerical output
        - apply bounded transformations

    DOES NOT:
        - change biological meaning
        - modify runtime state
    """

    transform = passive_definition.get(
        "passive_transform",
        {}
    ) or {}

    t_type = transform.get(
        "transform",
        "none"
    )

    # =====================================
    # none
    # =====================================

    if t_type == "none":
        return value

    # =====================================
    # linear
    # =====================================

    if t_type == "linear":
        return value

    # =====================================
    # normalized
    # =====================================

    if t_type == "normalized":

        scale = transform.get(
            "scale",
            1.0
        )

        if scale == 0:
            return 0.0

        return value / scale

    # =====================================
    # sigmoid
    # =====================================

    if t_type == "sigmoid":
        return 1.0 / (
            1.0 + math.exp(-value)
        )

    # =====================================
    # clamp
    # =====================================

    if t_type == "clamp":

        minimum = transform.get(
            "minimum",
            -float("inf")
        )

        maximum = transform.get(
            "maximum",
            float("inf")
        )

        return max(
            minimum,
            min(value, maximum)
        )

    return value
