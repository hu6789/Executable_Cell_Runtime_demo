# aip/viral_behavior_engine/viral_behavior_engine.py

from aip.viral_behavior_engine.viral_category_allocator import allocate_behavior_categories
from aip.viral_behavior_engine.viral_intra_category_competition import perform_intra_category_competition
from aip.viral_behavior_engine.viral_runtime_scaling import apply_runtime_scaling
from aip.viral_behavior_engine.viral_behavior_output import build_viral_behavior_output
from aip.viral_behavior_engine.viral_behavior_gate import (
    evaluate_viral_behavior_gate
)
from cellmaster.internalnet.behavior_engine.skeleton import compute_behavior_skeleton


# =========================================
# Viral Behavior Engine (ENTRY POINT)
# =========================================
class ViralBehaviorEngine:

    def process(
        self,
        runtime_entity,
        viral_context,          # ← MUST come from VML
        behavior_defs,
        viral_cycle_state,
        vml_context=None,
        tick=None
    ):

        # =================================
        # 2. category allocation (viral only)
        # =================================

        allocation_context = (
            allocate_behavior_categories(
                viral_cycle_state=
                    viral_cycle_state,

                viral_context=
                    viral_context
            )
        )
        
        allocation_context["behavior_defs"] = (
            behavior_defs
        )

        # =================================
        # 3. intra-category competition
        # =================================

        competition_context = perform_intra_category_competition(
            allocation_context
        )

        # =================================
        # 4. skeleton compute (PURE math layer)
        # =================================

        skeleton_results = {}

        for behavior_name, behavior_def in behavior_defs.items():

            skeleton_result = skeleton_results[
                behavior_name
            ]

            if evaluate_behavior_gate(
                behavior_def,
                skeleton_result,
                viral_cycle_state
            ):
                gated_behaviors[
                    behavior_name
                ] = skeleton_result

        # =================================
        # 5. REMOVE HIR GATE ❗
        # replace with viral gate ONLY
        # =================================

        gated_behaviors = {}

        for behavior_name, skeleton_result in skeleton_results.items():

            if evaluate_viral_behavior_gate(
                behavior_name,
                skeleton_result,
                competition_context,
                viral_context
            ):
                gated_behaviors[behavior_name] = skeleton_result

        # =================================
        # 6. runtime scaling (viral only)
        # =================================

        scaled_results = {}

        for behavior_name, skeleton_result in gated_behaviors.items():

            scaled_results[behavior_name] = apply_runtime_scaling(
                behavior_name,
                skeleton_result,
                competition_context
            )

        # =================================
        # 7. output
        # =================================

        output_result = build_viral_behavior_output(
            viral_context=viral_context,
            behavior_results=scaled_results,
            cycle_state=viral_cycle_state,
            resource_usage=viral_context
        )

        return {
            "runtime_type": "viral_modulation",
            "tick": tick,
            "output": output_result
        }
