# cellmaster/internalnet/hir/behavior_regulation.py

from cellmaster.internalnet.runtime_graph.behavior_definition_loader import (
    BehaviorDefinitionLoader
)

# =========================================
# Behavior Regulation Layer
# =========================================

def regulate_behaviors(

    behavior_defs,

    physiological_constraints,

    fate_progression,

    adjusted_context
):

    """
    HIR behavior permission layer

    responsibilities:

        - remove impossible behaviors
        - remove fate-conflicting behaviors
        - generate allowed behavior set

    DOES NOT:

        - compute behavior strength
        - modify behavior drive
        - execute behaviors
    """

    regulated_behaviors = {}

    progression_context = (

        fate_progression.get(
            "progression_context",
            {}
        )
    )

    fate = progression_context.get(
        "fate",
        "stable"
    )

    loader = BehaviorDefinitionLoader()

    for behavior_name in behavior_defs:

        behavior_def = loader.load(
            behavior_name
        )

        behavior_name = (

            behavior_def.get(
                "behavior_type"
            )

            or

            behavior_def.get(
                "name"
            )
        )

        if behavior_name is None:

            continue

        if is_behavior_blocked(

            behavior_name=
                behavior_name,

            behavior_def=
                behavior_def,

            physiological_constraints=
                physiological_constraints,

            fate=
                fate
        ):

            continue

        regulated_behaviors[
            behavior_name
        ] = behavior_def

    return regulated_behaviors

# =========================================
# Behavior Blocking Rules
# =========================================

def is_behavior_blocked(

    behavior_name,

    behavior_def,

    physiological_constraints,

    fate
):

    # -----------------------------
    # dead cell
    # -----------------------------

    if fate == "necrosis":

        return True

    # -----------------------------
    # proliferation forbidden
    # -----------------------------

    if (

        behavior_name == "proliferate"

        and

        physiological_constraints.get(
            "proliferation_limit",
            1.0
        ) <= 0.0

    ):

        return True

    return False
