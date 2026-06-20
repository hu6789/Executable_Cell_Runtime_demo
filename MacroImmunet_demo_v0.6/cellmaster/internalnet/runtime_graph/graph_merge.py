# cellmaster/internalnet/runtime_graph/graph_merge.py

"""
v0.6+

Graph is now a flat merged runtime graph.

Passive systems are NOT graph components.

HIR profiles are NOT graph components.

RuntimeGraphMerger only merges:

    nodes
    behaviors
    edges
"""
# =========================================
# Runtime Graph Merge
# =========================================

class RuntimeGraphMerger:

    """
    runtime graph fragment merger

    responsibilities:
        - merge graph fragments
        - preserve overlay ordering
        - collect graph lineage

    DOES NOT:
        - normalize graph schema
        - build runtime indexes
        - validate graph semantics
    """

    def __init__(self):

        pass

    # =====================================
    # merge graph fragments
    # =====================================

    def merge_graph_group(
        self,
        graph_fragments
    ):

        merged = {

            "nodes": [],

            "behaviors": [],

            "edges": [],

            "metadata": {},

            "sources": []
        }

        for fragment in graph_fragments:

            if fragment is None:
                continue

            if not isinstance(
                fragment,
                dict
            ):
                continue

            # -------------------------
            # lineage
            # -------------------------

            merged["sources"].append(

                fragment.get(
                    "name",
                    "unknown"
                )
            )

            # -------------------------
            # topology
            # -------------------------

            merged["nodes"].extend(

                fragment.get(
                    "nodes",
                    []
                )
            )

            merged["behaviors"].extend(

                fragment.get(
                    "behaviors",
                    []
                )
            )

            merged["edges"].extend(

                fragment.get(
                    "edges",
                    []
                )
            )

            # -------------------------
            # metadata
            # -------------------------

            metadata = fragment.get(
                "metadata",
                {}
            )

            if isinstance(
                metadata,
                dict
            ):
                merged["metadata"].update(
                    metadata
                )

        return merged
