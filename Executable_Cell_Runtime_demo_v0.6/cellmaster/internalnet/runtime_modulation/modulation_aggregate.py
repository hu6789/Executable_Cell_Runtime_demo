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

    aggregated = {

        "modulations": {},

        "payloads": []
    }
    # =====================================
    # normalize input formats (viral / cell / passive)
    # =====================================

    normalized_results = []

    for item in modulation_results:

        # ---------------------------------
        # viral contribution format
        # ---------------------------------

        if isinstance(item, dict) and "modulations" in item:

            for target, mod in item["modulations"].items():

                normalized_results.append({
                    "target": target,
                    "operation": "multiply",
                    "value": mod.get("multiply", 1.0),
                    "source": mod.get("sources", ["viral"])[0]
                })

            # handle payloads
            for p in item.get("payloads", []):
                normalized_results.append({
                    "_payload_type": p.get("type", "viral_payload"),
                    "source": "viral",
                    "value": p
                })

            continue

        # ---------------------------------
        # already flat format (existing system)
        # ---------------------------------

        normalized_results.append(item)
    
    # =====================================
    # process modulation results
    # =====================================

    for result in normalized_results:

        if not isinstance(
            result,
            dict
        ):
            continue

        payload_type = result.get(
            "_payload_type"
        )

        if payload_type is not None:

            aggregated[
                "payloads"
            ].append(
                result
            )

            continue

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

        if target not in aggregated["modulations"]:

            aggregated[
                "modulations"
            ][target] = {

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
            "modulations"
        ][
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
