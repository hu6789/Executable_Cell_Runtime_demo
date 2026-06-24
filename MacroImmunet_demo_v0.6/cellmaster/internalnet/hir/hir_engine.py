# cellmaster/internalnet/hir/hir_engine.py


from cellmaster.internalnet.hir.physiological_context import (
    integrate_global_context
)

from cellmaster.internalnet.hir.interpretation_adjustment import (
    adjust_physiological_interpretation
)

from cellmaster.internalnet.hir.fate_progression import (
    compute_fate_progression
)

from cellmaster.internalnet.hir.physiological_constraint import (
    compute_physiological_constraints
)

from cellmaster.internalnet.hir.hir_output import (
    build_hir_output
)

from cellmaster.internalnet.hir.state_label import (
    evaluate_state_labels
)

from cellmaster.internalnet.hir.behavior_regulation import (
    regulate_behaviors
)

from cellmaster.internalnet.hir.modulation_bridge import (
    extract_hir_interpretation_delta
)

# =========================================
# HIR Engine
# =========================================

class HIREngine:

    """
    Homeostatic / Integrity Regulator

    responsibilities:
        - integrate global physiology
        - apply interpretation adjustment
        - compute fate progression
        - generate physiological constraints
        - generate unified HIR runtime output

    DOES NOT:
        - execute behaviors
        - directly modify runtime state
        - directly write world
    """

    def __init__(self):

        pass

    # =====================================
    # main runtime entry
    # =====================================

    def process(
        self,
        runtime_entity,
        runtime_state,
        behavior_defs,
        modulation_runtime_state,
        hir_interpretation_delta=None,
        tick=None
    ):

        # =================================
        # integrate global physiology
        # =================================

        global_context = (
            integrate_global_context(

                runtime_entity=
                    runtime_entity,

                runtime_state=
                    runtime_state,

                modulation_runtime_state=
                    modulation_runtime_state
            )
        )
        
        # =================================
        # modulation interpretation bridge
        # =================================

        if hir_interpretation_delta is None:

            hir_interpretation_delta = (

                extract_hir_interpretation_delta(

                    modulation_runtime_state
                )
            )
        
        # =================================
        # apply interpretation adjustment
        # =================================

        adjusted_context = (

            adjust_physiological_interpretation(

                global_context=
                    global_context,

                hir_interpretation_delta=
                    hir_interpretation_delta,

                runtime_entity=
                    runtime_entity
            )
        )

        # =================================
        # compute fate progression
        # =================================

        fate_progression = (
            compute_fate_progression(

                adjusted_context=
                    adjusted_context,

                runtime_entity=
                    runtime_entity
            )
        )

        # =================================
        # generate physiological constraints
        # =================================

        physiological_constraints = (
            compute_physiological_constraints(

                adjusted_context=
                    adjusted_context,

                fate_progression=
                    fate_progression,

                runtime_entity=
                    runtime_entity
            )
        )

        # =================================
        # evaluate state labels
        # =================================

        state_labels = (

            evaluate_state_labels(

                adjusted_context=
                    adjusted_context,

                fate_progression=
                    fate_progression,

                runtime_entity=
                    runtime_entity
            )
        )
        
        # =================================
        # regulate behaviors
        # =================================

        regulated_behaviors = (

            regulate_behaviors(

                behavior_defs=
                    behavior_defs,

                physiological_constraints=
                    physiological_constraints,

                fate_progression=
                    fate_progression,

                adjusted_context=
                    adjusted_context
            )
        )

        # =================================
        # build unified HIR output
        # =================================

        hir_output = (

            build_hir_output(

                tick=
                    tick,

                global_context=
                    global_context,

                adjusted_context=
                    adjusted_context,

                fate_progression=
                    fate_progression,

                physiological_constraints=
                    physiological_constraints,

                state_labels=
                    state_labels,

                regulated_behaviors=
                    regulated_behaviors
            )
        )

        return hir_output
