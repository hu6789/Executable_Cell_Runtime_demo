# aip/vml/vml_engine.py


from aip.vml.viral_cycle import (
    determine_viral_cycle_state
)

from aip.vml.infection_load import (
    evaluate_infection_load
)

from aip.vml.resource_profile import (
    evaluate_resource_profile
)

from aip.vml.execution_profile import (
    build_execution_profile
)

from aip.vml.deception_context import (
    build_deception_context
)

from aip.vml.resource_preemption import (
    build_resource_preemption
)

from aip.vml.vml_output import (
    build_vml_output
)


# =========================================
# Viral Modulation Layer
# =========================================

class VMLEngine:

    """
    Viral Modulation Layer

    responsibilities:

        - determine viral lifecycle state

        - evaluate infection burden

        - evaluate resource availability

        - schedule viral execution

        - generate deception context

        - generate resource reservation

    DOES NOT:

        - modify runtime state

        - execute viral behaviors

        - execute host behaviors
    """

    # =====================================
    # main
    # =====================================

    def process(

        self,

        runtime_entity,

        passive_runtime_state,

        tick=None
    ):

        # =================================
        # viral cycle
        # =================================

        viral_state_label = (

            determine_viral_cycle_state(

                passive_runtime_state
            )
        )

        # =================================
        # infection load
        # =================================

        infection_load = (

            evaluate_infection_load(

                passive_runtime_state,

                viral_state_label
            )
        )

        # =================================
        # resource profile
        # =================================

        resource_profile = (

            evaluate_resource_profile(

                passive_runtime_state,

                infection_load
            )
        )

        # =================================
        # execution scheduler
        # =================================

        execution_profile = (

            build_execution_profile(

                viral_state_label,

                infection_load,

                resource_profile
            )
        )

        # =================================
        # deception layer
        # =================================

        deception_context = (

            build_deception_context(

                passive_runtime_state,

                viral_state_label,

                infection_load,

                execution_profile
            )
        )

        # =================================
        # resource reservation
        # =================================

        resource_preemption = (

            build_resource_preemption(

                viral_state_label,

                infection_load,

                resource_profile,

                execution_profile
            )
        )

        # =================================
        # output
        # =================================

        return build_vml_output(

            viral_state_label=
                viral_state_label,

            infection_load=
                infection_load,

            resource_profile=
                resource_profile,

            execution_profile=
                execution_profile,

            deception_context=
                deception_context,

            resource_preemption=
                resource_preemption
        )
