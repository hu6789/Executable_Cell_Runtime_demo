from typing import Dict

from internalnet.hir.schema import (
    BehaviorIntention,
    ResourceAllocation,
    ResourceDelta,
)


class ResourceRealizer:

    def realize(
        self,
        intention: BehaviorIntention,
        allocation: ResourceAllocation,
        available_resources: Dict[str, float],
    ) -> ResourceDelta:

        satisfaction_ratios = []

        for resource_name, requested in allocation.resources.items():
            requested = float(requested)

            if requested <= 0.0:
                continue

            available = float(
                available_resources.get(resource_name, 0.0)
            )

            ratio = min(
                available / requested,
                1.0,
            )

            satisfaction_ratios.append(ratio)

        if satisfaction_ratios:
            resource_factor = min(satisfaction_ratios)
        else:
            resource_factor = 1.0

        delta = (
            intention.value
            * (resource_factor - 1.0)
        )

        return ResourceDelta(
            behavior_name=intention.behavior_name,
            delta=delta,
        )
