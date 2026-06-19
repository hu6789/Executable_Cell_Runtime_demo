# cellmaster/internalnet/passive_engine/passive_transform.py

import math


# =========================================
# Passive Runtime Transform
# =========================================

def apply_passive_transform(passive_definition, value, runtime_context):
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

    transform = passive_definition.get("passive_transform", {}) or {}

    t_type = transform.get("transform", "none")
    params = transform.get("parameters", {}) or {}

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
        scale = params.get("scale", 1.0)
        return value / scale if scale != 0 else 0.0

    # =====================================
    # sigmoid
    # =====================================
    if t_type == "sigmoid":
        return 1.0 / (1.0 + math.exp(-value))

    # =====================================
    # limiting
    # =====================================
    if t_type == "limiting":
        return max(params.get("min", -1.0),
                   min(value, params.get("max", 1.0)))

    return value
