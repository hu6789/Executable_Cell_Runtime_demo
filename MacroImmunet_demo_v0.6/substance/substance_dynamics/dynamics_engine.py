# substance/substance_dynamics/dynamics_engine.py

from substance.substance_dynamics.diffusion import (
    diffuse_substance
)

from substance.substance_dynamics.decay import (
    decay_substance
)

from substance.substance_dynamics.cleanup import (
    cleanup_substances
)

from substance.substance_dynamics.aggregation import (
    aggregate_substances
)

from substance.substance_factory.substance_factory import (
    SubstanceFactory
)


class SubstanceDynamicsEngine:

    """
    World-side autonomous substance update

    diffusion
        ↓
    decay
        ↓
    aggregation
        ↓
    cleanup
    """

    def __init__(
        self,
        factory
    ):
        self.factory = factory

    def update(
        self,
        substances
    ):

        # =================================
        # diffusion
        # =================================

        offspring = []

        for entity in substances:

            children = diffuse_substance(
                entity
            )

            for child_data in children:

                child = self.factory.create_runtime_entity(

                    template_id=
                        child_data["substance_type"],

                    substance_id=
                        child_data["substance_id"],

                    position=
                        child_data["position"],

                    amount=
                        child_data["amount"]
                )

                offspring.append(
                    child
                )

        substances.extend(
            offspring
        )

        # =================================
        # decay
        # =================================

        for entity in substances:

            decay_substance(
                entity
            )

        # =================================
        # aggregation
        # =================================

        result = aggregate_substances(
            substances
        )

        substances = result[
            "survivors"
        ]

        # =================================
        # cleanup
        # =================================

        result = cleanup_substances(
            substances
        )

        substances = result[
            "alive"
        ]

        return substances
