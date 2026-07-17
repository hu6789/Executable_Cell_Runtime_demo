# cellmaster/internalnet/node_engine/runtime_clamp.py


# =========================================
# Apply Runtime Clamp
# =========================================

def apply_runtime_clamp(
    value,
    clamp_config,
    runtime_context=None
):

    """
    apply physiological/runtime limits

    responsibilities:
        - prevent numerical explosion
        - enforce physiological bounds
        - maintain stable runtime states
        - support dynamic cell-specific limits

    supported:
        - min/max clamp
        - soft clamp
        - runtime adaptive clamp
        - baseline-relative clamp
    """

    # =====================================
    # static clamp
    # =====================================

    minimum = clamp_config.get(
        "runtime_min"
    )

    maximum = clamp_config.get(
        "runtime_max"
    )

    clamped_value = value

    if minimum is not None:

        clamped_value = max(
            minimum,
            clamped_value
        )

    if maximum is not None:

        clamped_value = min(
            maximum,
            clamped_value
        )

    # =====================================
    # soft clamp
    # =====================================

    if clamp_config.get(
        "soft_clamp",
        False
    ):

        clamped_value = apply_soft_clamp(

            value=
                clamped_value,

            clamp_config=
                clamp_config
        )

    # =====================================
    # adaptive clamp
    # =====================================

    adaptive = clamp_config.get(
        "adaptive_clamp"
    )

    if adaptive is not None:

        clamped_value = apply_adaptive_clamp(

            value=
                clamped_value,

            adaptive_config=
                adaptive,

            runtime_context=
                runtime_context
        )

    return {

        "raw_value":
            value,

        "clamped_value":
            clamped_value,

        "clamp_applied":
            (
                clamped_value != value
            ),

        "clamp_type":
            "static"
    }


# =========================================
# Soft Clamp
# =========================================

def apply_soft_clamp(
    value,
    clamp_config
):

    """
    compress extreme values
    instead of hard truncation
    """

    soft_limit = clamp_config.get(
        "soft_limit",
        1.0
    )

    compression = clamp_config.get(
        "soft_compression",
        0.5
    )

    if abs(value) <= soft_limit:

        return value

    overflow = (
        abs(value)
        - soft_limit
    )

    compressed = (

        soft_limit
        + overflow * compression
    )

    if value < 0:

        compressed *= -1

    return compressed


# =========================================
# Adaptive Clamp
# =========================================

def apply_adaptive_clamp(
    value,
    adaptive_config,
    runtime_context
):

    """
    runtime-dependent physiological limit

    example:
        ATP max depends on mitochondrial health
    """

    if runtime_context is None:

        return value

    source = adaptive_config.get(
        "source"
    )

    scale = adaptive_config.get(
        "scale",
        1.0
    )

    adaptive_min = adaptive_config.get(
        "min"
    )

    adaptive_max = adaptive_config.get(
        "max"
    )

    source_value = resolve_runtime_value(

        runtime_context,
        source
    )

    if source_value is None:

        return value

    dynamic_limit = (
        source_value * scale
    )

    # -------------------------------------
    # adaptive maximum
    # -------------------------------------

    if adaptive_max is not None:

        adaptive_upper = min(

            adaptive_max,
            dynamic_limit
        )

        value = min(
            value,
            adaptive_upper
        )

    # -------------------------------------
    # adaptive minimum
    # -------------------------------------

    if adaptive_min is not None:

        adaptive_lower = max(

            adaptive_min,
            -dynamic_limit
        )

        value = max(
            value,
            adaptive_lower
        )

    return value


# =========================================
# Resolve Runtime Value
# =========================================

def resolve_runtime_value(
    runtime_context,
    source_name
):

    if source_name is None:

        return None

    runtime_state = runtime_context.get(
        "runtime_state",
        {}
    )

    if source_name in runtime_state:

        return runtime_state[
            source_name
        ]

    runtime_labels = runtime_context.get(
        "runtime_labels",
        {}
    )

    if source_name in runtime_labels:

        return runtime_labels[
            source_name
        ]

    if source_name in runtime_context:

        return runtime_context[
            source_name
        ]

    return None
