from typing import Dict

from internalnet.hir.schema import ResourceAllocation


class ResourceAllocator:

    def allocate(
        self,
        behavior_name: str,
        behavior_value: float,
        resource_coefficients: Dict[str, float],
    ) -> ResourceAllocation:

        resources = {
            resource_name: (
                behavior_value * float(coefficient)
            )
            for resource_name, coefficient
            in resource_coefficients.items()
        }

        return ResourceAllocation(
            behavior_name=behavior_name,
            resources=resources,
        )
