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

    if modulation_runtime_state is None:

        modulation_runtime_state = {}

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

    # =====================================
    # HIR Outputs
    # =====================================

    context = hir_output.get(
        "context",
        {}
    )

    regulation = hir_output.get(
        "regulation",
        {}
    )

    runtime = hir_output.get(
        "runtime",
        {}
    )

    summary = hir_output.get(
        "summary",
        {}
    )

    global_context = context.get(
        "global_context",
        {}
    )

    perceived_context = context.get(
        "perceived_context",
        {}
    )

    adjusted_context = context.get(
        "adjusted_context",
        {}
    )
    
    interpretation_labels = (
        adjusted_context.get(

            "interpretation_labels",

            []
        )
    )

    physiological_constraints = regulation.get(
        "constraints",
        {}
    )

    behavior_budget = regulation.get(
        "behavior_budget",
        {}
    ) 

    regulated_behaviors = regulation.get(
        "regulated_behaviors",
        {}
    )

    fate_progression = runtime.get(
        "fate",
        {}
    )

    state_label_output = runtime.get(
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

    behavior_defs = (
        graph_context.get_behavior_defs()
    )

    behavior_edges = (
        graph_context.get_runtime_edges()
    )

    # =====================================
    # runtime ecology context
    # =====================================

    ecology_context = build_runtime_ecology(

        runtime_state,

        physiological_constraints,

        state_labels,

        fate_progression
    )
    
    identity = safe_get_identity(
        runtime_entity
    )
    
    cell_id = safe_get_id(
        runtime_entity
    )
    
    position = safe_get_position(
        runtime_entity
    )

    return {

        "cell_id":
            cell_id,

        "cell_type":
            identity.get("cell_type"),
            
        "position":
            position,

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

        "global_context":
            global_context,

        "perceived_context":
            perceived_context,

        "adjusted_context":
            adjusted_context,

        "physiological_constraints":
            physiological_constraints,

        "behavior_budget":
            behavior_budget,

        "regulated_behaviors":
            regulated_behaviors,

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

    physiological_constraints,

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
        physiological_constraints.get(
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
                physiological_constraints.get(
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
    
def safe_get_identity(runtime_entity):

    if hasattr(runtime_entity, "identity"):

        return runtime_entity.identity

    if isinstance(runtime_entity, dict):

        return runtime_entity.get(
            "identity",
            {}
        )

    return {}
        
def safe_get_id(runtime_entity):

    if hasattr(runtime_entity, "id"):

        return runtime_entity.id

    if isinstance(runtime_entity, dict):

        return runtime_entity.get(
            "id"
        )

    return None
    
def safe_get_position(runtime_entity):

    if hasattr(runtime_entity, "position"):

        return runtime_entity.position

    if isinstance(runtime_entity, dict):

        return runtime_entity.get(
            "position"
        )

    return None
