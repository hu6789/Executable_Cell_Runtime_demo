# cellmaster/internalnet/runtime_modulation/modulation_engine.py


from cellmaster.internalnet.runtime_modulation.modulation_context import (
    build_modulation_context
)

from cellmaster.internalnet.runtime_modulation.modulation_aggregate import (
    aggregate_modulation_results
)

from cellmaster.internalnet.runtime_modulation.modulation_runtime_state import (
    build_modulation_runtime_state
)

from cellmaster.internalnet.runtime_modulation.modulation_runtime_delta import (
    build_modulation_runtime_delta
)
# =========================================
# Runtime Modulation Engine
# =========================================

class RuntimeModulationEngine:

    """
    runtime modulation execution layer

    responsibilities:
        - construct modulation context
        - execute runtime hooks
        - collect modulation outputs
        - merge modulation results
        - return unified modulation package

    DOES NOT:
        - directly modify runtime state
        - directly write world state
        - execute behaviors
        - evaluate HIR
    """

    def __init__(
        self,
        registry
    ):

        self.registry = registry

    # =====================================
    # main modulation entry
    # =====================================

    def process(
        self,
        runtime_entity,
        runtime_state,
        node_runtime_results,
        passive_runtime_results,
        runtime_graph,
        node_inputs,
        tick=None
    ):

        # =================================
        # build modulation context
        # =================================

        modulation_context = (
            build_modulation_context(

                runtime_entity=
                    runtime_entity,

                runtime_state=
                    runtime_state,

                node_runtime_results=
                    node_runtime_results,

                passive_runtime_results=
                    passive_runtime_results,

                runtime_graph=
                    runtime_graph,

                node_inputs=
                    node_inputs,

                tick=tick
            )
        )

        # =================================
        # load active hooks
        # =================================

        if self.registry is None:

            active_hooks = []

        else:

            active_hooks = (
                self.registry.get_runtime_hooks(
                    runtime_entity
                )
            )

        collected_results = []

        # =================================
        # execute hooks
        # =================================

        for hook in active_hooks:
            
            print()
            print("RUN HOOK")
            print(hook.hook_name)

            result = hook.apply(
                modulation_context
            )

            print()
            print("HOOK RESULT")
            print(result)

            result = hook.apply(
                modulation_context
            )

            if result is None:

                continue

            # single result
            if isinstance(result, dict):

                collected_results.append(
                    result
                )

            # list result
            elif isinstance(result, list):

                collected_results.extend(
                    result
                )

        # =================================
        # merge modulation outputs
        # =================================

        aggregated_results = (
            aggregate_modulation_results(
                collected_results
            )
        )
        
        modulation_runtime_state = (
            build_modulation_runtime_state(
                aggregated_results
            )
        )
        
        modulation_runtime_delta = (
            build_modulation_runtime_delta(

                modulation_runtime_state=
                    modulation_runtime_state
            )
        )

        return {

            "runtime_type":
                "modulation",

            "tick":
                tick,

            "modulation_context":
                modulation_context,

            "aggregated_results":
                aggregated_results,

            "modulation_runtime_state":
                modulation_runtime_state,

            "modulation_runtime_delta":
                modulation_runtime_delta
        }
