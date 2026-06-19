# cellmaster/internalnet/behavior_engine/behavior_transform.py
# TODO
#
# 1.
# sigmoid overflow protection
#
# 2.
# parameterized transform support
#
# 3.
# limiting transform currently
# applies upper-bound only
#

import math


# =========================================
# Behavior Contribution Transform
# =========================================

def apply_behavior_transform(
    gated_contributions
):

    """
    apply runtime preprocessing
    to behavior contributions

    responsibilities:
        - apply transform functions
        - preprocess contribution values
        - preserve semantic category

    DOES NOT:
        - aggregate categories
        - compute behavior drive
        - evaluate behavior gate
    """

    transformed = []

    for contribution in gated_contributions:

        raw_value = contribution.get(
            "raw_value",
            0.0
        )

        weight = contribution.get(
            "weight",
            1.0
        )

        transform = contribution.get(
            "transform",
            "linear"
        )

        weighted = raw_value * weight

        transformed_value = apply_transform(
            weighted,
            transform
        )

        updated = dict(
            contribution
        )

        updated[
            "transformed_value"
        ] = transformed_value

        transformed.append(
            updated
        )

    return transformed


# =========================================
# Transform Dispatcher
# =========================================

def apply_transform(
    value,
    transform
):

    if transform == "linear":

        return value

    if transform == "sigmoid":

        return sigmoid_transform(
            value
        )

    if transform == "relu":

        return relu_transform(
            value
        )

    if transform == "square":

        return square_transform(
            value
        )

    if transform == "inverse":

        return inverse_transform(
            value
        )

    if transform == "normalized":

        return normalized_transform(
            value
        )

    if transform == "limiting":

        return limiting_transform(
            value
        )

    return value


# =========================================
# Individual Transforms
# =========================================

def sigmoid_transform(value):

    value = max(
        min(value, 50),
        -50
    )

    return (
        1.0 /
        (
            1.0 +
            math.exp(-value)
        )
    )

def relu_transform(value):

    return max(
        0.0,
        value
    )


def square_transform(value):

    return value * value


def inverse_transform(value):

    return (
        1.0 / (1.0 + abs(value))
    )

# bounded normalization
def normalized_transform(value):

    return (
        value / (1.0 + abs(value))
    )


def limiting_transform(
    value,
    limit=1.0
):
# upper bounded only
#   return min(
#       value,
#       limit
#   )
    return max(
        -limit,
        min(value, limit)
    )
