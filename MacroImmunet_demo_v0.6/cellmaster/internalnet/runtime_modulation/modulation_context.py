# cellmaster/internalnet/runtime_modulation/modulation_context.py


# =========================================
# Build Runtime Modulation Context
# =========================================

def build_modulation_context(

    runtime_entity,
    runtime_state,
    node_runtime_results,
    passive_runtime_results,
    runtime_graph,
    node_inputs,
    tick=None
):

    """
    unified modulation runtime context

    responsibilities:
        - expose runtime entity info
        - expose current runtime state
        - expose node/passive outputs
        - expose graph/runtime metadata
        - provide hook-safe read context

    DOES NOT:
        - modify runtime state
        - execute modulation
        - apply world writes
    """

    # =====================================
    # runtime identity
    # =====================================

    identity = runtime_entity.identity or {}

    runtime_identity = {

        "cell_id":
            runtime_entity.id,

        "cell_type":
            identity.get(
                "cell_type"
            ),

        "genotype":
            identity.get(
                "genotype"
            ),
 
        "runtime_tags":
            identity.get(
                "runtime_tags",
                []
            )
    }

    # =====================================
    # runtime profiles
    # =====================================

    runtime_profiles = {

        "hir_profile":

            runtime_entity.hir_capabilities.get(
                "hir_profile"
            ),

        "exposure_profile":

            runtime_entity.exposure_rules.get(
                "exposure_profile"
            )
    } 

    # =====================================
    # node summaries
    # =====================================
    
    node_result_map = {}


    for result in node_runtime_results:

        node_id = result.get("node_id")

        if node_id is None:
            continue

        node_result_map[node_id] = result

    # =====================================
    # passive summaries
    # =====================================

    passive_result_map = {}

    for result in passive_runtime_results:

        passive_name = result.get(
            "passive_name"
        )

        if passive_name is None:

            continue

        passive_result_map[
            passive_name
        ] = result

    # =====================================
    # graph metadata
    # =====================================

    graph_metadata = {

        "node_count":
            len(
                runtime_graph.get_runtime_nodes()
            ),

        "edge_count":
            len(
                runtime_graph.get_edges_by_type(
                    "node_to_node"
                )
            ),

        "behavior_count":
            len(
                runtime_graph.get_runtime_behaviors()
            )
    }

    # =====================================
    # final context
    # =====================================

    return {

        "tick":
            tick,
            
        "runtime_entity":
            runtime_entity,

        "runtime_identity":
            runtime_identity,

        "runtime_state":
            runtime_state,

        "runtime_profiles":
            runtime_profiles,

        "node_inputs":
            node_inputs,

        "node_runtime_results":
            node_result_map,

        "passive_runtime_results":
            passive_result_map,

        "runtime_graph":
            runtime_graph,

        "graph_metadata":
            graph_metadata
    }
