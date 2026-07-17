# cellmaster/internalnet/node_engine/node_runtime_result.py


# =========================================
# Generate Node Runtime Result
# =========================================

def build_node_runtime_result(
    node_definition,
    previous_value,
    computed_value,
    final_value,
    gate_passed,
    aggregated_contributions,
    runtime_metadata=None
):

    """
    generate finalized node runtime output

    responsibilities:
        - preserve runtime calculation result
        - preserve runtime provenance
        - expose runtime metadata
        - provide downstream runtime propagation

    DOES NOT:
        - write runtime state
        - mutate world state
    """

    node_name = (
        node_definition.get("node_name")
        or
        node_definition.get("node_id")
    )

    runtime_active = bool(
        gate_passed
    )

    return {

        # =================================
        # node identity
        # =================================

        "node_name":
            node_name,

        # =================================
        # runtime values
        # =================================

        "previous_value":
            previous_value,

        "computed_value":
            computed_value,

        "final_value":
            final_value,

        # =================================
        # runtime state
        # =================================

        "runtime_active":
            runtime_active,

        "gate_passed":
            gate_passed,

        # =================================
        # contribution summary
        # =================================

        "aggregated_contributions":
            aggregated_contributions,

        # =================================
        # runtime metadata
        # =================================

        "runtime_metadata":
            runtime_metadata or {}
    }


# =========================================
# Build Runtime Metadata
# =========================================

def build_runtime_metadata(
    node_definition,
    runtime_context=None,
    extra_metadata=None
):

    """
    optional helper for
    runtime provenance/debugging
    """

    metadata = {

        "node_type":
            node_definition.get(
                "node_type",
                "continuous"
            ),

        "skeleton_formula":
            node_definition.get(
                "skeleton_formula"
            ),

        "runtime_clamp":
            {

                "min":
                    node_definition.get(
                        "runtime_min"
                    ),

                "max":
                    node_definition.get(
                        "runtime_max"
                    )
            }
    }

    if runtime_context is not None:

        metadata[
            "tick"
        ] = runtime_context.get(
            "tick"
        )

    if extra_metadata:

        metadata.update(
            extra_metadata
        )

    return metadata
