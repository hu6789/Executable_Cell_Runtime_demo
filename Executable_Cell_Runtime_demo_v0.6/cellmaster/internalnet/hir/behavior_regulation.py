# cellmaster/internalnet/hir/behavior_regulation.py

from cellmaster.internalnet.runtime_graph.behavior_definition_loader import (
    BehaviorDefinitionLoader
)

# =========================================
# Behavior Regulation
# =========================================

def regulate_behaviors(
    behavior_defs,
    physiological_constraints,
    behavior_budget,
    fate_progression,
    adjusted_context
):
    """
    final HIR permission layer

    responsibilities

        - remove forbidden behaviors

        - apply fate restrictions

        - apply schema-level switches

        - generate executable behavior set

    DOES NOT

        - compute behavior strength

        - compute behavior budget

        - execute behaviors
    """

    loader = BehaviorDefinitionLoader()

    regulated_behaviors = {}

    progression_context = fate_progression.get(
        "progression_context",
        {}
    )

    fate = progression_context.get(
        "fate",
        "stable"
    )

    for behavior_name in behavior_defs:

        behavior_def = loader.load(
            behavior_name
        )

        profile = extract_behavior_profile(
            behavior_name,
            behavior_def,
            behavior_budget
        )

        if not is_behavior_allowed(
            profile,
            physiological_constraints,
            fate
        ):

            continue

        regulated_behaviors[
            behavior_name
        ] = behavior_def

    return regulated_behaviors


# =========================================
# Behavior Profile
# =========================================

def extract_behavior_profile(
    behavior_name,
    behavior_def,
    behavior_budget
):
    """
    collect runtime information
    required for regulation
    """

    category = behavior_def.get(
        "behavior_category",
        "default"
    )

    budget = behavior_budget.get(
        behavior_name,
        {}
    )

    return {

        "name":
            behavior_name,

        "category":
            category,

        "execution_limit":
            budget.get(
                "execution_limit",
                1.0
            ),

        "priority":
            budget.get(
                "priority",
                1.0
            ),

        "preferred":
            budget.get(
                "preferred",
                False
            ),

        "enabled":
            behavior_def.get(
                "enabled",
                True
            )
    }


# =========================================
# Permission Evaluation
# =========================================

def is_behavior_allowed(
    behavior_profile,
    physiological_constraints,
    fate
):
    """
    evaluate whether
    behavior is permitted
    """

    if not check_schema_permission(
        behavior_profile
    ):
        return False

    if not check_fate_permission(
        behavior_profile,
        fate
    ):
        return False

    if not check_budget_permission(
        behavior_profile
    ):
        return False

    return True


# =========================================
# Schema Permission
# =========================================

def check_schema_permission(
    behavior_profile
):
    """
    schema-level enable switch
    """

    return behavior_profile.get(
        "enabled",
        True
    )


# =========================================
# Fate Permission
# =========================================

def check_fate_permission(
    behavior_profile,
    fate
):
    """
    fate-specific behavior gate
    """

    category = behavior_profile.get(
        "category",
        "default"
    )

    # -------------------------------------
    # dead cells
    # -------------------------------------

    if fate == "necrosis":

        return False

    # -------------------------------------
    # apoptosis
    # -------------------------------------

    if fate == "apoptosis":

        forbidden = {

            "translation",
            "mobility",
            "proliferation",
            "secretion"
        }

        if category in forbidden:

            return False

    return True


# =========================================
# Budget Permission
# =========================================

def check_budget_permission(
    behavior_profile
):
    """
    budget performs scaling.

    only completely depleted
    behaviors are blocked.
    """

    execution_limit = behavior_profile.get(
        "execution_limit",
        1.0
    )

    return execution_limit > 0.0
