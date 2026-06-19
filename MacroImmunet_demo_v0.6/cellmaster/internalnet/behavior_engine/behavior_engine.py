# cellmaster/internalnet/behavior_engine/behavior_engine.py

"""
Behavior Engine Pipeline

BehaviorContext
↓
EcologyBias
↓
CategoryAllocator
↓
IntraCategoryCompetition
↓
ContributionGate
↓
Transform
↓
Group
↓
Aggregate
↓
Skeleton
↓
BehaviorGate
↓
RuntimeScaling
↓
BehaviorPackage
↓
BehaviorOutput
"""
from cellmaster.internalnet.behavior_engine.behavior_context import (
    build_behavior_context
)

from cellmaster.internalnet.behavior_engine.ecology_bias import (
    apply_ecology_bias
)

from cellmaster.internalnet.behavior_engine.category_allocator import (
    allocate_behavior_categories
)

from cellmaster.internalnet.behavior_engine.intra_category_competition import (
    perform_intra_category_competition
)

from cellmaster.internalnet.behavior_engine.behavior_contribution_gate import (
    evaluate_behavior_contribution_gate
)

from cellmaster.internalnet.behavior_engine.behavior_transform import (
    apply_behavior_transform
)

from cellmaster.internalnet.behavior_engine.behavior_group import (
    group_behavior_contributions
)

from cellmaster.internalnet.behavior_engine.behavior_aggregate import (
    aggregate_behavior_groups
)

from cellmaster.internalnet.behavior_engine.behavior_skeleton import (
    apply_behavior_skeleton
)

from cellmaster.internalnet.behavior_engine.behavior_gate import (
    evaluate_behavior_gate
)

from cellmaster.internalnet.behavior_engine.runtime_scaling import (
    apply_runtime_scaling
)

from cellmaster.internalnet.behavior_engine.behavior_package import (
    build_behavior_package
)

from cellmaster.internalnet.behavior_engine.behavior_output import (
    build_behavior_output
)


# =========================================
# Behavior Engine
# =========================================

class BehaviorEngine:

    """
    high-level behavior runtime layer

    responsibilities:
        - construct behavior ecology
        - compute behavior competition
        - evaluate graph contributions
        - compute behavior drive
        - generate runtime behavior packages

    DOES NOT:
        - directly modify runtime state
        - directly write world
        - directly execute behaviors
    """

    def __init__(self):

        pass

    # =====================================
    # main runtime entry
    # =====================================

    def run_behaviors(
        self,
        runtime_entity,
        node_runtime_state,
        modulation_runtime_state,
        graph_context,
        hir_output,
        tick=None
    ):

        behavior_outputs = []

        # =================================
        # build behavior runtime context
        # =================================

        behavior_context = (
            build_behavior_context(

                runtime_entity=
                    runtime_entity,

                node_runtime_state=
                    node_runtime_state,

                modulation_runtime_state=
                    modulation_runtime_state,

                graph_context=
                    graph_context,

                hir_output=
                    hir_output,

                tick=
                    tick
            )
        )
        print()
        print("BEHAVIOR CONTEXT")
        print(
            behavior_context["runtime_state"]
        )
        # =================================
        # apply ecology shaping
        # =================================

        ecology_context = (
            apply_ecology_bias(
                behavior_context
            )
        )
        print()
        print("ECOLOGY CONTEXT")
        print(
            ecology_context["runtime_state"]
        )
        # =================================
        # category allocation
        # =================================

        allocation_context = (
            allocate_behavior_categories(
                ecology_context
            )
        )
        print()
        print("ALLOCATION CONTEXT")
        print(
            allocation_context["runtime_state"]
        )
        # =================================
        # intra-category competition
        # =================================

        competition_context = (
            perform_intra_category_competition(
                allocation_context
            )
        )
        print()
        print("COMPETITION CONTEXT")
        print(
            competition_context["runtime_state"]
        )
        # =================================
        # iterate behaviors
        # =================================

        behaviors = graph_context.get_behavior_defs()

        for behavior_name, behavior_def in (
            behaviors.items()
        ):

            # -----------------------------
            # evaluate contribution gates
            # -----------------------------

            gated_contributions = (
                evaluate_behavior_contribution_gate(

                    behavior_name,
                    competition_context,
                    graph_context
                )
            )

            # -----------------------------
            # transform contributions
            # -----------------------------

            transformed = (
                apply_behavior_transform(
                    gated_contributions
                )
            )

            # -----------------------------
            # group contributions
            # -----------------------------

            grouped = (
                group_behavior_contributions(
                    transformed
                )
            )

            # -----------------------------
            # aggregate grouped signals
            # -----------------------------

            aggregated = (
                aggregate_behavior_groups(
                    grouped
                )
            )

            # -----------------------------
            # compute skeleton drive
            # -----------------------------

            skeleton_result = (
                apply_behavior_skeleton(

                    behavior_def,
                    aggregated
                )
            )

            # -----------------------------
            # final behavior gate
            # -----------------------------

            allowed = (
                evaluate_behavior_gate(

                    behavior_def,
                    skeleton_result,
                    competition_context
                )
            )

            if not allowed:

                continue
            print()
            print("==== BEHAVIOR ====")
            print(behavior_name)

            print("gated:")
            print(gated_contributions)

            print("aggregated:")
            print(aggregated)

            print("skeleton:")
            print(skeleton_result)

            print("allowed:")
            print(allowed)
            # -----------------------------
            # runtime scaling
            # -----------------------------

            scaled_result = (
                apply_runtime_scaling(
                    behavior_name,
                    skeleton_result,
                    competition_context
                )
            )
            print()
            print("scaled_result")
            print(scaled_result)

            # -----------------------------
            # build behavior package
            # -----------------------------

            behavior_package = (
                build_behavior_package(

                    behavior_name,
                    behavior_def,
                    scaled_result
                )
            )
            print()
            print("behavior_package")
            print(behavior_package)
            # -----------------------------
            # append package
            # -----------------------------

            behavior_outputs.append(
                behavior_package
            )

        # =================================
        # build final output
        # =================================

        return build_behavior_output(

            behavior_outputs,
            behavior_context,
            tick
        )
