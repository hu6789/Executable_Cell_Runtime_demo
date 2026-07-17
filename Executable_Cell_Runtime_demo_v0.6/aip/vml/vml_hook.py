# aip/vml/vml_hook.py


from cellmaster.internalnet.runtime_modulation.modulation_hook import (
    RuntimeModulationHook
)

from aip.vml.vml_engine import (
    VMLEngine
)


# =========================================
# VML Hook
# =========================================

class VMLHook(
    RuntimeModulationHook
):

    """
    VML runtime modulation hook

    responsibilities:

        - execute VML pipeline
        - expose deception context
        - expose resource preemption
        - expose execution profile

    DOES NOT:

        - modify runtime state
        - bypass HIR
        - write world state
    """

    def __init__(self):

        super().__init__(

            hook_name=
                "VMLHook",

            hook_type=
                "viral_modulation",

            priority=
                100,

            enabled=
                True
        )

        self.engine = VMLEngine()

    # =====================================
    # compatibility
    # =====================================

    def supports(
        self,
        runtime_entity
    ):

        parasites = getattr(
            runtime_entity,
            "parasites",
            []
        )

        return len(parasites) > 0

    # =====================================
    # runtime execution
    # =====================================

    def apply(
        self,
        modulation_context
    ):

        runtime_entity = (
            modulation_context[
                "runtime_entity"
            ]
        )

        runtime_state = (
            modulation_context[
                "runtime_state"
            ]
        )

        tick = (
            modulation_context.get(
                "tick"
            )
        )

        return {

            "_payload_type": "vml",

            "payload": self.engine.process(
 
                runtime_entity=runtime_entity,
  
                passive_runtime_state=runtime_state,

                tick=tick
             )
        }
