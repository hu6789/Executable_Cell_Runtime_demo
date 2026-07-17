# aip/viral_behavior_engine/viral_behavior_engine.py

from aip.viral_behavior_engine.viral_category_allocator import allocate_behavior_categories
from aip.viral_behavior_engine.viral_intra_category_competition import perform_intra_category_competition
from aip.viral_behavior_engine.viral_runtime_scaling import apply_runtime_scaling
from aip.viral_behavior_engine.viral_behavior_output import build_viral_behavior_output
from aip.viral_behavior_engine.viral_behavior_gate import evaluate_viral_behavior_gate
from aip.viral_behavior_engine.viral_to_skeleton_adapter import (
    build_viral_skeleton_inputs
)
from cellmaster.internalnet.behavior_engine.behavior_skeleton import apply_behavior_skeleton


# =========================================
# Viral Behavior Engine
# OUTPUT: modulation_runtime_state ONLY
# =========================================

class ViralBehaviorEngine:

    def process(
        self,
        runtime_entity,
        viral_context,
        behavior_defs,
        viral_cycle_state,
        vml_context=None,
        tick=None
    ):

        # =================================
        # 1. allocation
        # =================================
        allocation = allocate_behavior_categories(
            viral_cycle_state=viral_cycle_state,
            viral_context=viral_context
        )

        allocation["behavior_defs"] = behavior_defs

        # =================================
        # 2. competition
        # =================================
        competition = perform_intra_category_competition(allocation)

        # =================================
        # 3. skeleton
        # =================================
        skeleton_results = {}

        for name, behavior_def in behavior_defs.items():

            inputs = build_viral_skeleton_inputs(
                behavior_name=name,
                behavior_def=behavior_def,
                viral_context=viral_context,
                competition_context=competition,
                viral_cycle_state=viral_cycle_state
            )

            skeleton_results[name] = apply_behavior_skeleton(
                behavior_def,
                inputs
            )
       

        # =================================
        # 4. gate (FIXED)
        # =================================
        gated = {}

        for name, skeleton in skeleton_results.items():

            if evaluate_viral_behavior_gate(
                behavior_def=behavior_defs[name],
                skeleton_result=skeleton,
                viral_cycle_state=viral_cycle_state
            ):
                gated[name] = skeleton

        # =================================
        # 5. scaling
        # =================================
        scaled = {}

        for name, skeleton in gated.items():

            scaled[name] = apply_runtime_scaling(
                name,
                skeleton,
                competition
            )

        # =================================
        # 6. OUTPUT FIX (关键修复)
        # =================================
        output = build_viral_behavior_output(
            viral_context=viral_context,
            behavior_results=scaled,
            cycle_state=viral_cycle_state,
            resource_usage=viral_context.get(
                "resource_projection",
                {}
            )
        )

        return {
            "runtime_type": "viral_modulation",
            "tick": tick,
            "modulation_runtime_state": output["modulation_runtime_state"]
        }
