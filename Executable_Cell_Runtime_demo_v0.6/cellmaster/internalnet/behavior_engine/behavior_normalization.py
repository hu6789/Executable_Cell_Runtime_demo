# cellmaster/internalnet/behavior_engine/behavior_normalization.py

"""
Behavior Signal Normalization

Position

Aggregate
    ↓
Normalization
    ↓
Skeleton

Responsibilities

    - normalize aggregated runtime signals
    - keep skeleton numerically stable
    - preserve semantic ordering

DOES NOT

    - change behavior competition
    - compute drive
"""

# =========================================
# Normalization
# =========================================

DEFAULT_SIGNAL_MAX = 100.0


def normalize_behavior_signals(
    aggregated_contributions,
    graph_context
):

    normalized = {}

    for category, value in (
        aggregated_contributions.items()
    ):

        normalized[category] = (
            normalize_signal(value)
        )

    return normalized


# =========================================
# Normalize Single Signal
# =========================================

def normalize_signal(
    value,
    signal_max=DEFAULT_SIGNAL_MAX
):

    if value <= 0.0:
        return 0.0

    if value >= signal_max:
        return signal_max

    return value
