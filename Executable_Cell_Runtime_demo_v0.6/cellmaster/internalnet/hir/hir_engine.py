from cellmaster.internalnet.hir.physiological_context import (
    integrate_global_context
)

from cellmaster.internalnet.hir.perception_layer import (
    build_perceived_context
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

from cellmaster.internalnet.hir.behavior_regulation import (
    regulate_behaviors
)

from cellmaster.internalnet.hir.behavior_budget import (
    allocate_behavior_budget
)

from cellmaster.internalnet.hir.state_label import (
    evaluate_state_labels
)

from cellmaster.internalnet.hir.hir_output import (
    build_hir_output
)

'''
Context Integration

↓

Deception Extraction

↓

Perception Layer

↓

Interpretation Adjustment

↓

Fate Progression

↓

Physiological Constraint

↓

Behavior Budget

↓

Behavior Regulation

↓

State Label

↓

HIR Output
'''

# =========================================
# HIR Engine
# =========================================

class HIREngine:

    def __init__(self):

        pass

    # =====================================
    # Main Runtime Entry
    # =====================================

    def process(
        self,
        runtime_entity,
        runtime_state,
        behavior_defs,
        modulation_runtime_state=None,
        tick=None
    ):

        if modulation_runtime_state is None:

            modulation_runtime_state = {}

        # =================================
        # Context Integration
        # =================================

        global_context = self._build_global_context(
            runtime_entity,
            runtime_state,
            modulation_runtime_state
        )

        deception_delta = (
            modulation_runtime_state.get(
                "hir_interpretation_delta",
                {}
            )
        ) or {}

        # =================================
        # Perception Layer
        # =================================


        perceived_context = self._build_perception(
            global_context,
            deception_delta
        )

        # =================================
        # Interpretation
        # =================================

        adjusted_context = self._adjust_interpretation(

            perceived_context,

            deception_delta,

            runtime_entity
        )

        # =================================
        # Fate Progression
        # =================================

        fate_progression = self._compute_fate(

            adjusted_context,
            runtime_entity
        )

        # =================================
        # Physiological Constraint
        # =================================

        physiological_constraints = self._compute_constraints(

            adjusted_context,
            fate_progression,
            runtime_entity
        )

        # =================================
        # Behavior Budget
        # =================================

        behavior_budget = self._allocate_budget(

            behavior_defs,

            physiological_constraints
        )
        # =================================
        # Behavior Budget
        # =================================
        regulated_behaviors = self._regulate_behaviors(

            behavior_defs,

            physiological_constraints,

            behavior_budget,

            fate_progression,

            adjusted_context
        )
 
        # =================================
        # State Labels
        # =================================

        state_labels = self._evaluate_labels(

            adjusted_context,
            fate_progression,
            runtime_entity
        )

        # =================================
        # Runtime Output
        # =================================

        hir_output = self._build_output(

            tick=tick,

            global_context=global_context,
            
            perceived_context=perceived_context,

            adjusted_context=adjusted_context,

            fate_progression=fate_progression,

            physiological_constraints=physiological_constraints,

            behavior_budget=behavior_budget,

            state_labels=state_labels,

            regulated_behaviors=regulated_behaviors
        )

        return hir_output

    # =====================================
    # Context
    # =====================================

    def _build_global_context(
        self,
        runtime_entity,
        runtime_state,
        modulation_runtime_state
    ):

        return integrate_global_context(

            runtime_entity=runtime_entity,

            runtime_state=runtime_state,

            modulation_runtime_state=modulation_runtime_state
        )

    # =====================================
    # Perception
    # =====================================

    def _build_perception(
        self,
        global_context,
        deception_delta
    ):

        return build_perceived_context(

            global_context,
  
            deception_delta
        )

    # =====================================
    # Interpretation
    # =====================================

    def _adjust_interpretation(

        self,

        perceived_context,
   
        deception_delta,

        runtime_entity
    ):

        return adjust_physiological_interpretation(

            perceived_context=
                perceived_context,

            hir_interpretation_delta=
                deception_delta,

            runtime_entity=
                runtime_entity
        )

    # =====================================
    # Fate
    # =====================================

    def _compute_fate(
        self,
        adjusted_context,
        runtime_entity
    ):

        return compute_fate_progression(

            adjusted_context,

            runtime_entity
        )

    # =====================================
    # Constraint
    # =====================================

    def _compute_constraints(
        self,
        adjusted_context,
        fate_progression,
        runtime_entity
    ):

        return compute_physiological_constraints(

            adjusted_context,

            fate_progression,

            runtime_entity
        )
        
    # =====================================
    # Behavior Regulation
    # =====================================

    def _regulate_behaviors(
        self,
        behavior_defs,
        physiological_constraints,
        behavior_budget,
        fate_progression,
        adjusted_context
    ):

        return regulate_behaviors(

            behavior_defs=
                behavior_defs,

            physiological_constraints=
                physiological_constraints,

            behavior_budget=
                behavior_budget,

            fate_progression=
                fate_progression,

            adjusted_context=
                adjusted_context
        )

    # =====================================
    # Behavior Budget
    # =====================================

    def _allocate_budget(
        self,
        behavior_defs,
        physiological_constraints
    ):

        return allocate_behavior_budget(

            behavior_defs=
                behavior_defs,

            physiological_constraints=
                physiological_constraints
        )

    # =====================================
    # State Labels
    # =====================================

    def _evaluate_labels(
        self,
        adjusted_context,
        fate_progression,
        runtime_entity
    ):

        return evaluate_state_labels(

            adjusted_context=
                adjusted_context,

            fate_progression=
                fate_progression,

            runtime_entity=
                runtime_entity
        )
        
    # =====================================
    # Runtime Output
    # =====================================

    def _build_output(
        self,
        tick,
        global_context,
        perceived_context,
        adjusted_context,
        fate_progression,
        physiological_constraints,
        behavior_budget,
        state_labels,
        regulated_behaviors
    ):

        return build_hir_output(

            tick=
                tick,

            global_context=
                global_context,
                
            perceived_context=
                perceived_context,

            adjusted_context=
                adjusted_context,

            fate_progression=
                fate_progression,

            physiological_constraints=
                physiological_constraints,

            behavior_budget=
                behavior_budget,

            state_labels=
                state_labels,

            regulated_behaviors=
                regulated_behaviors
        )
