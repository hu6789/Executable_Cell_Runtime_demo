# cellmaster/internalnet/node_engine/external_contribution.py


# =========================================
# Runtime Input Contributions
# =========================================

def collect_runtime_contributions(
    node_id,
    runtime_context
):

    """
    Convert runtime inputs into node contributions.

    responsibilities:
        - consume standardized runtime inputs
        - match node activation semantics
        - generate contribution objects

    does NOT:
        - perform graph traversal
        - modify runtime state
        - execute gates
    """

    runtime_inputs = runtime_context.get(
        "node_inputs",
        []
    )

    contributions = []

    expected_signal = (
        f"{node_id}_activation"
    )

    for item in runtime_inputs:

        if item.get(
            "internal_signal"
        ) != expected_signal:

            continue

        contributions.append({

            "category":
                "activation",

            "value":
                item.get(
                    "strength",
                    0.0
                ),

            "source":
                item.get(
                    "source_id"
                ),

            "source_type":
                "runtime_input"
        })

    return contributions
