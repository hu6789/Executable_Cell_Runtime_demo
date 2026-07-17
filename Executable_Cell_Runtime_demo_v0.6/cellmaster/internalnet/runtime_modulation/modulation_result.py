# cellmaster/internalnet/runtime_modulation/modulation_result.py


# =========================================
# Build Modulation Result
# =========================================

def build_modulation_result(

    modulation_type,
    target,
    operation,
    value,
    source=None,
    metadata=None
):

    """
    unified runtime modulation output

    responsibilities:
        - standardize modulation structure
        - expose runtime intervention
        - provide downstream-compatible output

    DOES NOT:
        - apply modulation
        - mutate runtime state
    """

    return {

        "runtime_type":
            "modulation",

        "modulation_type":
            modulation_type,

        "target":
            target,

        "operation":
            operation,

        "value":
            value,

        "source":
            source,

        "metadata":
            metadata or {}
    }


# =========================================
# Merge Modulation Results
# =========================================

def merge_modulation_results(
    modulation_results
):

    """
    merge modulation outputs
    into grouped runtime structure

    responsibilities:
        - group by target
        - preserve ordering
        - simplify downstream application
    """

    merged = {}

    for result in modulation_results:

        target = result.get(
            "target"
        )

        if target is None:

            continue

        if target not in merged:

            merged[target] = []

        merged[target].append(
            result
        )

    return merged
