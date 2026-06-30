# cellmaster/stateupdate/context_integrator.py

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
       
"""
Runtime Context Integration

Consumes:

    runtime_state
    hir_output
    behavior_output

Produces:

    projected_runtime_state
    public_runtime_labels
    exposure_context

Purpose:

    bridge InternalNet
    and PublicExposure
"""
# =========================================
# Runtime Context Integration
# =========================================

def integrate_runtime_context(
    runtime_output,
    cell,
    tick=None
):

    behavior_output = runtime_output.get(
        "behavior_output",
        {}
    )

    hir_output = runtime_output.get(
        "hir_output",
        {}
    )

    # =====================================
    # latest executable runtime state
    # =====================================

    executable_runtime_state = runtime_output.get(
        "modulated_runtime_state",
        {}
    )

    physiological_cost = (
        behavior_output.get(
            "merged_physiological_cost",
            {}
        )
    )  
    
    behavior_packages = (
        behavior_output.get(
            "behavior_packages",
            []
        )
    )

    label_flags = getattr(
        cell,
        "label_flags",
        {}
    )

    # =====================================
    # projected runtime state
    # =====================================
 
    projected_runtime_state = (
        apply_physiological_cost(
            executable_runtime_state,
            physiological_cost
        )
    )
    
    debug_print()
    debug_print("=" * 60)
    debug_print("STATE UPDATE")
    debug_print("=" * 60)

    debug_print("INPUT STATE")
    debug_print(executable_runtime_state)

    debug_print()

    debug_print("PHYSIOLOGICAL COST")
    debug_print(physiological_cost)

    debug_print()

    debug_print("PROJECTED STATE")
    debug_print(projected_runtime_state)
    
    # =====================================
    # runtime labels
    # =====================================

    runtime_labels = build_runtime_labels(

        projected_runtime_state,
        hir_output,
        label_flags
    ) 
    
    # =====================================
    # outward context package
    # =====================================

    context = {

        "cell_id":
            runtime_output.get(
                "cell_id"
            ),

        "tick":
            tick,

        "runtime_state":
            executable_runtime_state,

        "projected_runtime_state":
            projected_runtime_state,

        "hir_output":
            hir_output,

        "runtime_labels":
            runtime_labels,

        "fate_progression":
            hir_output.get(
                "fate_progression",
                {}
            ),

        "behavior_packages":
            behavior_packages,

        "external_requests":
            behavior_output.get(
                "external_requests",
                []
            ),

        "label_flags":
            label_flags
    }

    return context


# =========================================
# Runtime Labels
# =========================================

def build_runtime_labels(
    projected_runtime_state,
    hir_output,
    label_flags
):

    """
    lightweight runtime semantic labels

    future:
        HIR/VML/SIO integrated
    """

    labels = {}

    # =====================================
    # ATP stress
    # =====================================

    runtime_labels = hir_output.get(
        "state_labels",
        []
    ) 
    
    # =====================================
    # infection
    # =====================================

    labels["infected"] = (

        label_flags.get(
            "infected",
            False
        )
    )

    # =====================================
    # activation
    # =====================================

    runtime_labels = hir_output.get(
        "state_labels",
        []
    )

    labels["activated"] = (
        "activated" in runtime_labels
    )

    return labels

# =====================================
# cost
# =====================================a

def apply_physiological_cost(
    runtime_state,
    physiological_cost
):

    projected = dict(
        runtime_state
    )

    for node_name, delta in (
        physiological_cost.items()
    ):

        projected[node_name] = (

            projected.get(
                node_name,
                0.0
            )

            + delta
        )

    return projected
