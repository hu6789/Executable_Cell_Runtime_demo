# cellmaster/internalnet/runtime_graph/graph_merge.py


# =========================================
# Runtime Graph Merge
# =========================================

class RuntimeGraphMerger:

    """
    runtime graph fragment merger

    responsibilities:
        - merge runtime graph fragments
        - preserve graph lineage
        - unify runtime graph package
        - preserve overlay ordering

    DOES NOT:
        - normalize graph schema
        - validate graph semantics
        - build runtime indexes
    """

    def __init__(self):

        pass

    # =====================================
    # merge runtime graph package
    # =====================================

    def merge_runtime_graphs(
        self,
        runtime_graph_package
    ):

        merged_graph = {

            # =============================
            # merged node graph
            # =============================

            "node_graphs":

                self.merge_graph_group(

                    runtime_graph_package.get(
                        "node_graphs",
                        []
                    )
                ),

            # =============================
            # merged behavior graph
            # =============================

            "behavior_graphs":

                self.merge_graph_group(

                    runtime_graph_package.get(
                        "behavior_graphs",
                        []
                    )
                ),

            # =============================
            # merged passive graph
            # =============================

            "passive_graphs":

                self.merge_graph_group(

                    runtime_graph_package.get(
                        "passive_graphs",
                        []
                    )
                ),
            
            # =============================
            # merged HIR profiles
            # =============================

            "hir_profiles":

                self.merge_graph_group(

                    runtime_graph_package.get(
                        "hir_profiles",
                        []
                    )
                )
        }

        return merged_graph

    # =====================================
    # merge graph group
    # =====================================

    def merge_graph_group(self, graph_fragments):

        merged = {
            "nodes": [],
            "behaviors": [],
            "edges": [],
            "metadata": {},   # ❗必须是 dict
            "sources": []
        }

        for fragment in graph_fragments:

            if fragment is None:
                continue

            if not isinstance(fragment, dict):
                continue

            merged["sources"].append(
                fragment.get("graph_name", fragment.get("name", "unknown"))
            )
  
            merged["nodes"].extend(fragment.get("nodes", []))
            merged["behaviors"].extend(fragment.get("behaviors", []))
            merged["edges"].extend(fragment.get("edges", []))

            # ❗ metadata 改成 dict merge，而不是 list append
            merged["metadata"].update(fragment.get("metadata", {}))

        return merged
