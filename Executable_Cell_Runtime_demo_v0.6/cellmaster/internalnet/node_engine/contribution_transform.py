# cellmaster/internalnet/node_engine/contribution_transform.py

import math


# =========================================
# Contribution Transform
# =========================================

def apply_contribution_transform(
    edge,
    runtime_context
):

    """
    transform edge contribution
    before category aggregation

    supported transforms:
        - linear
        - sigmoid
        - relu
        - square
        - normalized
        - limiting
    """

    source = edge.get(
        "source"
    )

    if source is None:

        return None

    # =====================================
    # resolve source runtime value
    # =====================================

    source_value = resolve_runtime_value(

        runtime_context,
        source
    )

    if source_value is None:

        return None

    # =====================================
    # edge weight
    # =====================================

    weight = edge.get(
        "weight",
        1.0
    )

    weighted_value = (
        source_value * weight
    )

    # =====================================
    # transform selection
    # =====================================

    transform = edge.get(
        "transform",
        "linear"
    )

    transformed_value = (
        execute_transform(

            transform=
                transform,

            value=
                weighted_value,

            edge=
                edge
        )
    )

    # =====================================
    # build transformed contribution
    # =====================================

    return {

        "source": source,

        "target": edge.get("target"),

        "category": edge.get(
            "contribution_category",
            "activation"
        ),

        "value": transformed_value,

        "participation_requirement":
            edge.get(
                "participation_requirement",
                "optional"
            )
    }


# =========================================
# Execute Transform
# =========================================

def execute_transform(
    transform,
    value,
    edge
):

    # =====================================
    # linear
    # =====================================

    if transform == "linear":

        return value

    # =====================================
    # sigmoid
    # =====================================

    if transform == "sigmoid":

        slope = edge.get(
            "sigmoid_slope",
            1.0
        )

        midpoint = edge.get(
            "sigmoid_midpoint",
            0.0
        )

        return sigmoid(
            value,
            slope,
            midpoint
        )

    # =====================================
    # relu
    # =====================================

    if transform == "relu":

        return max(
            0.0,
            value
        )

    # =====================================
    # square
    # =====================================

    if transform == "square":

        return value * value

    # =====================================
    # normalized
    # =====================================

    if transform == "normalized":

        max_value = edge.get(
            "normalization_max",
            1.0
        )

        if max_value <= 0:

            return 0.0

        return (
            value / max_value
        )

    # =====================================
    # limiting
    # =====================================

    if transform == "limiting":

        limit = edge.get(
            "limit",
            1.0
        )

        return min(
            value,
            limit
        )

    # =====================================
    # fallback
    # =====================================

    return value


# =========================================
# Sigmoid
# =========================================

def sigmoid(
    value,
    slope,
    midpoint
):

    exponent = (
        -slope * (value - midpoint)
    )

    return (
        1.0 / (
            1.0 + math.exp(exponent)
        )
    )


# =========================================
# Resolve Runtime Value
# =========================================

def resolve_runtime_value(
    runtime_context,
    source_name
):

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
