# cellmaster/internalnet/behavior_engine/behavior_package.py

'''
Behavior Runtime Package

Position:

    final stage of Behavior Engine

Purpose:

    package behavior outcome
    for downstream execution layers

Produces:

    physiological_cost
    runtime_requests

Consumes:

    behavior strength

Does NOT:

    modify runtime state
    execute behavior
    write world
Behavior Package

Behavior Package represents
behavior outcome only.

Physiological cost is NOT
applied here.

External requests are NOT
executed here.

Application occurs in
downstream layers.
'''
# =========================================
# Behavior Runtime Package
# =========================================

def build_behavior_package(
    behavior_name,
    behavior_def,
    scaled_result
):

    """
    generate executable behavior package

    responsibilities:
        - package runtime behavior result
        - generate internal runtime delta
        - generate outward runtime requests
        - attach runtime metadata

    DOES NOT:
        - directly execute behavior
        - directly write runtime state
        - directly write world
    """

    # =====================================
    # behavior metadata
    # =====================================

    behavior_category = (
        behavior_def.get(
            "behavior_category",
            "misc"
        )
    )

    behavior_type = behavior_def.get(
        "behavior_type",
        behavior_name
    )
    
    scaled_drive = scaled_result.get(
        "scaled_drive",
        0.0
    )
    
    # =====================================
    # generate behavior consequences
    # =====================================


    physiological_cost = generate_physiological_cost(

        behavior_def,
        scaled_drive
    )
    
    internal_outputs = generate_internal_outputs(
        behavior_def,
        scaled_drive
    )

    external_requests = (
        generate_external_requests(

            behavior_def,
            scaled_drive
        )
    )
    
    # =====================================
    # build package
    # =====================================

    return {

        "behavior_name":
            behavior_name,
            
        "scaled_drive":
            scaled_result["scaled_drive"],

        "behavior_type":
            behavior_type,

        "behavior_category":
            behavior_category,

        "behavior_strength":
            scaled_drive,
        
        # generate physiological
        # and outward consequences
        "physiological_cost":
            physiological_cost,
            
        "internal_outputs":
            internal_outputs,

        "external_requests":
            external_requests,

        "runtime_metadata": {

            "raw_drive":
                scaled_result.get(
                    "raw_drive",
                    0.0
                ),

            "scaled_drive":
                scaled_result.get(
                    "scaled_drive",
                    0.0
                ),

            "behavior_formula":
                behavior_def.get(
                    "behavior_skeleton",
                    {}
                ).get(
                    "formula",
                    "default"
                )
        }
    }


# =========================================
# Physiological Cost Generation
# =========================================
# physiological execution cost
"""
legacy naming

represents physiological cost
associated with behavior execution

does not directly modify
runtime state
"""
def generate_physiological_cost(
    behavior_def,
    scaled_drive
):

    """
    generate internal physiological cost
    """

    physiological_cost = {}

    resource_cost = (
        behavior_def.get(
            "resource_cost",
            {}
        )
    )

    for node_name, cost in (
        resource_cost.items()
    ):

        physiological_cost[
            node_name
        ] = -(
            cost * scaled_drive
        )

    return physiological_cost


# =========================================
# External Request Generation
# =========================================

def generate_external_requests(
    behavior_def,
    scaled_drive
):

    """
    generate outward runtime requests
    """

    requests = []

    external_outputs = (
        behavior_def.get(
            "external_outputs",
            []
        )
    )

    for output in external_outputs:

        request_type = output.get(
            "request_type"
        )

        request = {

            "request_type":
                request_type,

            "strength":
                scaled_drive,

            "payload":
                dict(
                    output.get(
                        "payload",
                        {}
                    )
                )
        }

        requests.append(
            request
        )

    return requests
    
# =========================================
# Internal Request Generation
# =========================================
def generate_internal_outputs(
    behavior_def,
    scaled_drive
):

    outputs = {}

    internal_outputs = (
        behavior_def.get(
            "internal_outputs",
            {}
        )
    )

    for node_name, amount in (
        internal_outputs.items()
    ):

        outputs[node_name] = (
            amount * scaled_drive
        )

    return outputs
