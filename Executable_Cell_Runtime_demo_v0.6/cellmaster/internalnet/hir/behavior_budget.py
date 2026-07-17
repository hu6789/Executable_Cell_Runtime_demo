# cellmaster/internalnet/hir/behavior_budget.py

from cellmaster.internalnet.runtime_graph.behavior_definition_loader import (
    BehaviorDefinitionLoader
)

# =========================================
# Behavior Budget Allocation
# =========================================

def allocate_behavior_budget(
    behavior_defs,
    physiological_constraints
):
    """
    translate physiological constraint profiles
    into per-behavior execution budgets

    responsibilities

        - allocate execution budget
        - preserve behavior independence
        - expose runtime execution limits

    DOES NOT

        - execute behaviors
        - suppress behaviors
        - modify runtime state
    """

    loader = BehaviorDefinitionLoader()

    budgets = {}

    for behavior_name in behavior_defs:

        behavior_def = loader.load(
            behavior_name
        )

        category = behavior_def.get(
            "behavior_category",
            "default"
        )

        execution_limit = resolve_execution_limit(
            category,
            physiological_constraints
        )

        budgets[behavior_name] = {

            "execution_limit":
                execution_limit,

            "priority":
                resolve_behavior_priority(
                    category,
                    physiological_constraints
                ),

            "preferred":
                resolve_behavior_preference(
                    category,
                    physiological_constraints
                )
        }

    return budgets


# =========================================
# Execution Limit
# =========================================

def resolve_execution_limit(
    category,
    physiological_constraints
):

    resource = physiological_constraints.get(
        "resource_constraint",
        {}
    )

    functional = physiological_constraints.get(
        "functional_constraint",
        {}
    )

    repair = physiological_constraints.get(
        "repair_constraint",
        {}
    )

    mapping = {

        "metabolism":
            resource.get(
                "metabolism_capacity",
                1.0
            ),

        "translation":
            resource.get(
                "translation_capacity",
                1.0
            ),

        "mobility":
            functional.get(
                "mobility_capacity",
                1.0
            ),

        "secretion":
            functional.get(
                "secretion_capacity",
                1.0
            ),

        "proliferation":
            functional.get(
                "proliferation_capacity",
                1.0
            ),

        "repair":
            repair.get(
                "repair_capacity",
                1.0
            )
    }

    return mapping.get(
        category,
        1.0
    )


# =========================================
# Priority Allocation
# =========================================

def resolve_behavior_priority(
    category,
    physiological_constraints
):
    """
    determine scheduling priority

    priority is independent from
    execution_limit

    future versions may include

        immune mode
        starvation mode
        viral hijacking
    """

    repair = physiological_constraints.get(
        "repair_constraint",
        {}
    )

    emergency = repair.get(
        "emergency_repair",
        False
    )

    if emergency:

        if category == "repair":
            return 2.0

        return 0.8

    return 1.0


# =========================================
# Preferred Behavior
# =========================================

def resolve_behavior_preference(
    category,
    physiological_constraints
):
    """
    preferred behaviors
    receive scheduling advantage

    currently only repair
    may become preferred
    """

    repair = physiological_constraints.get(
        "repair_constraint",
        {}
    )

    if category == "repair":

        return repair.get(
            "repair_preferred",
            False
        )

    return False
