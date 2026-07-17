"""
HIR Runtime Output

Position

    final stage of HIR

Purpose

    package HIR runtime result

Produces

    HIR Runtime Artifact

Does NOT

    execute behaviors

    modify runtime state

    write world
"""

# =========================================
# HIR Runtime Output
# =========================================

def build_hir_output(
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
    """
    package HIR runtime artifact

    responsibilities

        - package physiological context

        - package interpretation

        - package regulation

        - package runtime state

        - generate runtime summary

    DOES NOT

        - execute behaviors

        - modify runtime state

        - write world
    """

    context = build_context_output(

        global_context,

        perceived_context,

        adjusted_context
    )

    regulation = build_regulation_output(
        physiological_constraints,
        behavior_budget,
        regulated_behaviors
    )

    runtime = build_runtime_output(
        tick,
        fate_progression,
        state_labels
    )

    summary = build_runtime_summary(
        fate_progression,
        state_labels,
        regulated_behaviors
    )

    return {

        "runtime_type":
            "hir",

        "context":
            context,

        "regulation":
            regulation,

        "runtime":
            runtime,

        "summary":
            summary
    }


# =========================================
# Context Output
# =========================================

def build_context_output(
    global_context,
    perceived_context,
    adjusted_context
):
    """
    package physiological
    and interpreted context
    """

    return {

        "global_context":
            global_context,

        "perceived_context":
            perceived_context,

        "adjusted_context":
            adjusted_context
    }


# =========================================
# Regulation Output
# =========================================

def build_regulation_output(
    physiological_constraints,
    behavior_budget,
    regulated_behaviors
):
    """
    package behavior regulation
    """

    return {

        "constraints":
            physiological_constraints,

        "behavior_budget":
            behavior_budget,

        "regulated_behaviors":
            regulated_behaviors
    }


# =========================================
# Runtime Output
# =========================================

def build_runtime_output(
    tick,
    fate_progression,
    state_labels
):
    """
    package runtime state
    """

    return {

        "tick":
            tick,

        "fate":
            fate_progression,

        "state_labels":
            state_labels
    }


# =========================================
# Runtime Summary
# =========================================

def build_runtime_summary(
    fate_progression,
    state_labels,
    regulated_behaviors
):
    """
    lightweight summary

    for observer
    logger
    debug
    """

    progression = fate_progression.get(
        "progression_context",
        {}
    )

    labels = state_labels.get(
        "state_labels",
        []
    )

    public = state_labels.get(
        "public_labels",
        []
    )

    return {

        "fate":
            progression.get(
                "fate",
                "stable"
            ),

        "progression":
            progression.get(
                "progression",
                0.0
            ),

        "state":
            labels,

        "public_state":
            public,

        "behavior_count":
            len(regulated_behaviors),

        "active_behaviors":
            list(
                regulated_behaviors.keys()
            )
    }
