# cellmaster/internalnet/behavior_engine/behavior_signal_normalization.py

"""
Behavior Signal Normalization

Purpose
-------
Convert raw behavior drive into a normalized execution strength.

BehaviorSkeleton computes an absolute drive
(e.g. 324000).

This module converts it into a bounded execution
strength before behavior package generation.

The normalized strength is later multiplied by
node production / physiological cost.

Current version:
    simple saturation normalization

Future:
    Michaelis-Menten
    Hill function
    logistic response
"""

# =========================================
# Behavior Signal Normalization
# =========================================

def normalize_behavior_drive(
    behavior_name,
    raw_drive
):
    """
    Convert an arbitrary raw drive into [0,1].

    Large values quickly saturate to 1.0.

    Examples

        0        -> 0.0
        50       -> 0.33
        100      -> 0.5
        300      -> 0.75
        1000     -> 0.91
        10000    -> 0.99
    """

    raw_drive = max(
        0.0,
        raw_drive
    )

    normalization_constant = 100.0

    normalized_drive = (
        raw_drive
        /
        (
            raw_drive
            +
            normalization_constant
        )
    )

    return {

        "behavior_name":
            behavior_name,

        "raw_drive":
            raw_drive,

        "normalized_drive":
            normalized_drive
    }
