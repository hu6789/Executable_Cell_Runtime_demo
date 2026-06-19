# cellmaster/internalnet/behavior_engine/behavior_context.py


# =========================================
# Behavior Runtime Context
# =========================================

def build_behavior_context(

    runtime_entity,

    node_runtime_state,

    modulation_runtime_state,

    graph_context,

    hir_output,

    tick=None
):
    """
    construct unified behavior runtime context

    responsibilities:
        - expose runtime physiological state
        - expose HIR interpretation
        - expose fate progression
        - expose behavior graph
        - expose runtime resource ecology

    DOES NOT:
        - compute behavior strength
        - perform graph propagation
        - execute behaviors
    """

    runtime_state = {

        **node_runtime_state,

        "node_modulations":
            modulation_runtime_state.get(
                "node_modulations",
                {}
            ),

        "passive_modulations":
            modulation_runtime_state.get(
                "passive_modulations",
                {}
            ),

        "behavior_modulations":
            modulation_runtime_state.get(
                "behavior_modulations",
                {}
            ),

        "hir_modulations":
            modulation_runtime_state.get(
                "hir_modulations",
                {}
            ),

        "global_modulations":
            modulation_runtime_state.get(
                "global_modulations",
                {}
            )
    }

    hir_constraints = hir_output.get(
        "physiological_constraints",
        {}
    )

    fate_progression = hir_output.get(
        "fate_progression",
        {}
    )

    adjusted_context = hir_output.get(
        "adjusted_context",
        {}
    )

    interpretation_labels = (
        adjusted_context.get(
        "interpretation_labels",
            []
        )
    )
    state_label_output = hir_output.get(
        "state_labels",
        {}
    )

    state_labels = (
        state_label_output.get(
            "state_labels",
            []
        )
    )

    # =====================================
    # behavior graph context
    # =====================================

    behavior_group = graph_context.get_runtime_nodes(
        "behavior_graphs"
    )

    behavior_defs = behavior_group

    behavior_edges = graph_context.get_runtime_edges("behavior_graphs") or []

    # =====================================
    # runtime ecology context
    # =====================================

    ecology_context = build_runtime_ecology(

        runtime_state,
        hir_constraints,
        state_labels,
        fate_progression
    )
    
    identity = runtime_entity.identity

    return {

        "cell_id":
            runtime_entity.id,

        "cell_type":
            identity.get("cell_type"),

        "tick":
            tick,

        # =================================
        # runtime state
        # =================================

        "runtime_state":
            runtime_state,

        "modulation_state":
            modulation_runtime_state,
        # =================================
        # HIR
        # =================================

        "hir_constraints":
            hir_constraints,

        "fate_progression":
            fate_progression,

        "interpretation_labels":
            interpretation_labels,

        "state_labels":
            state_labels,

        # =================================
        # graph
        # =================================

        "behavior_edges":
            behavior_edges,

        "behavior_defs":
            behavior_defs,

        # =================================
        # ecology
        # =================================

        "ecology_context":
            ecology_context
    }


# =========================================
# Runtime Ecology Construction
# =========================================

def build_runtime_ecology(
    runtime_state,
    hir_constraints,
    state_labels,
    fate_progression
):

    """
    construct global behavior ecology

    ecology:
        - resource availability
        - stress ecology
        - activation ecology
        - suppression ecology
    """

    ATP = runtime_state.get(
        "ATP",
        0.0
    )

    activation = runtime_state.get(
        "activation_level",
        0.0
    )

    infection = runtime_state.get(
        "infection_burden",
        0.0
    )

    global_suppression = (
        hir_constraints.get(
            "global_behavior_suppression",
            0.0
        )
    )
    
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

    return {

        "resource_ecology": {

            "ATP":
                ATP,

            "translation_limit":
                hir_constraints.get(
                    "translation_limit",
                    1.0
                )
        },

        "activation_ecology": {

            "activation_level":
                activation,

            "activated":
                "activated" in state_labels
        },

        "stress_ecology": {

            "suppressed":
                global_suppression > 0.5,

            "global_suppression":
                global_suppression
        },

        "infection_ecology": {

            "infection_burden":
                infection,

            "infected":
                "infected" in state_labels
        },
        
        "fate_ecology": {

            "fate":
                fate,

            "progressing":
                progression_context.get(
                    "progressing",
                    False
                )
        }
    }
