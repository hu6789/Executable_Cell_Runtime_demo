# cellmaster/scheduler/merge_runtime_inputs.py

"""
Merge Runtime Inputs

Responsibilities
----------------
- merge scheduler inputs by target_id
- combine node_inputs from multiple sources
- preserve all other metadata

DOES NOT
--------
- evaluate priority
- filter triggers
- modify signal semantics
"""


from copy import deepcopy


# =========================================
# Merge Runtime Inputs
# =========================================

def merge_runtime_inputs(
    *input_groups
):
    """
    Merge runtime input packages by target_id.

    Parameters
    ----------
    *input_groups
        Multiple runtime input lists.

    Returns
    -------
    list

        One runtime input package per target cell.
    """

    merged = {}

    for group in input_groups:

        if not group:
            continue

        for package in group:

            target_id = package.get(
                "target_id"
            )

            if target_id is None:
                continue

            #
            # first package
            #

            if target_id not in merged:

                merged[target_id] = deepcopy(
                    package
                )

                merged[target_id].setdefault(
                    "node_inputs",
                    []
                )

                continue

            #
            # merge node inputs
            #

            merged[target_id].setdefault(
                "node_inputs",
                []
            )

            merged[target_id]["node_inputs"].extend(

                package.get(
                    "node_inputs",
                    []
                )

            )

            #
            # preserve additional metadata
            #

            for key, value in package.items():

                if key in (
                    "target_id",
                    "node_inputs"
                ):
                    continue

                if key not in merged[target_id]:

                    merged[target_id][key] = deepcopy(
                        value
                    )

    return list(
        merged.values()
    )
