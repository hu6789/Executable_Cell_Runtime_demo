# cellmaster/internalnet/behavior_engine/behavior_output.py

"""
Behavior Engine Output

Position:

    final output layer
    of Behavior Engine

Purpose:

    aggregate behavior packages

Produces:

    physiological_cost
    external_requests
    runtime_snapshot

Important:

    physiological_cost
    is NOT applied here

    external_requests
    are NOT executed here

Downstream layers decide
how to consume these outputs
"""
# =========================================
# Behavior Engine Output
# =========================================

def build_behavior_output(
    behavior_packages,
    behavior_context,
    tick=None
):

    """
    build unified behavior runtime output

    responsibilities:
        - collect executable behaviors
        - merge internal runtime deltas
        - collect external runtime requests
        - expose behavior runtime snapshot

    DOES NOT:
        - directly execute behaviors
        - directly modify runtime state
        - directly write world
    """

    merged_physiological_cost = {}
    merged_internal_outputs = {}
    external_requests = []
    behavior_trace = []

    # =====================================
    # merge behavior packages
    # =====================================

    for package in behavior_packages:

        merge_physiological_cost(

            merged_physiological_cost,

            package.get(
                "physiological_cost",
                {}
            )
        )

        merge_internal_outputs(

            merged_internal_outputs,

            package.get(
                "internal_outputs",
                {}
            )
        )

        for request in package.get(
            "external_requests",
            []
        ):

            request = dict(request)

            request.setdefault(

                "source_id",

                behavior_context.get(
                    "cell_id"
                )
            )

            request.setdefault(

                "position",

                behavior_context.get(
                    "position"
                )
            )

            external_requests.append(
                request
            )
        
        behavior_trace.append({

            "behavior":
                package.get("behavior_name"),

            "strength":
                package.get("scaled_drive", 0.0)

        })

    # =====================================
    # build runtime snapshot
    # =====================================

    runtime_snapshot = {

        "active_behaviors": [

            package.get(
                "behavior_name"
            )

            for package
            in behavior_packages
        ],

        "behavior_count":
            len(behavior_packages),

        "external_request_count":
            len(external_requests),
            
        "physiological_cost":
            merged_physiological_cost
            }

    # =====================================
    # final output
    # =====================================

    return {

        "tick":
            tick,

        "cell_id":
            behavior_context.get(
                "cell_id"
            ),

        "cell_type":
            behavior_context.get(
                "cell_type"
            ),

        # =================================
        # behavior execution
        # =================================

        "behavior_packages":
            behavior_packages,

        # =================================
        # behavior-generated
        # physiological cost
        # =================================

        "merged_physiological_cost":
            merged_physiological_cost,
            
        "merged_internal_outputs":
            merged_internal_outputs,

        "external_requests":
            external_requests,

        # =================================
        # runtime snapshot
        # =================================

        "runtime_snapshot":
            runtime_snapshot,
            
        "internal_outputs":
            merged_internal_outputs,
        
        "behavior_trace":
            behavior_trace
            
    }


# =========================================
# Merge Physiological Cost
# =========================================

def merge_physiological_cost(
    merged,
    delta
):

    for node_name, value in (
        delta.items()
    ):

        merged[
            node_name
        ] = (

            merged.get(
                node_name,
                0.0
            )

            + value
        )
        
# =========================================
# Merge Internal Outputs
# =========================================
def merge_internal_outputs(
    merged,
    delta
):

    for node_name, value in (
        delta.items()
    ):

        merged[node_name] = (

            merged.get(
                node_name,
                0.0
            )

            + value
        )
