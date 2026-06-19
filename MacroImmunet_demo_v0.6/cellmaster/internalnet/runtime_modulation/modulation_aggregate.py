# cellmaster/internalnet/runtime_modulation/modulation_aggregate.py


# =========================================
# Aggregate Runtime Modulations
# =========================================

def aggregate_modulation_results(
    modulation_results
):

    """
    aggregate runtime modulation outputs

    responsibilities:
        - merge modulation semantics
        - combine multiple hook outputs
        - build runtime-effective modulation state
        - preserve modulation provenance

    DOES NOT:
        - execute modulation
        - mutate runtime state
        - apply world writes
    """

    aggregated = {}

    # =====================================
    # process modulation results
    # =====================================

    for result in modulation_results:

        target = result.get(
            "target"
        )

        if target is None:

            continue

        operation = result.get(
            "operation"
        )

        value = result.get(
            "value",
            0.0
        )

        source = result.get(
            "source"
        )

        # =================================
        # initialize target state
        # =================================

        if target not in aggregated:

            aggregated[target] = {

                "target":
                    target,

                "multiply":
                    1.0,

                "add":
                    0.0,

                "override":
                    None,

                "blocked":
                    False,

                "sources":
                    []
            }

        target_state = aggregated[
            target
        ]

        # =================================
        # multiply
        # =================================

        if operation == "multiply":

            target_state[
                "multiply"
            ] *= value

        # =================================
        # add
        # =================================

        elif operation == "add":

            target_state[
                "add"
            ] += value

        # =================================
        # override
        # =================================

        elif operation == "override":

            target_state[
                "override"
            ] = value

        # =================================
        # block
        # =================================

        elif operation == "block":

            target_state[
                "blocked"
            ] = True

        # =================================
        # preserve provenance
        # =================================

        target_state[
            "sources"
        ].append({

            "operation":
                operation,

            "value":
                value,

            "source":
                source
        })

    return aggregated
