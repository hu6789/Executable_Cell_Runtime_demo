# cellinstance/factory/runtime_assembler.py


from cellmaster.internalnet.runtime_graph.graph_merge import (
    RuntimeGraphMerger
)

from cellmaster.internalnet.runtime_graph.graph_normalizer import (
    RuntimeGraphNormalizer
)

from cellmaster.internalnet.runtime_graph.graph_indexer import (
    RuntimeGraphIndexer
)

from cellmaster.internalnet.runtime_graph.graph_context import (
    RuntimeGraphContext
)


# =========================================
# Runtime Assembler
# =========================================

class RuntimeAssembler:

    """
    runtime biological graph assembler

    responsibilities:
        - load graph fragments
        - merge graph structures
        - normalize graph schema
        - build runtime graph indexes
        - construct runtime graph context

    DOES NOT:
        - execute runtime logic
        - evaluate biology
        - mutate runtime state
    """
    def __init__(self, runtime_graph_loader):

        self.loader = runtime_graph_loader

        # =========================
        # FIX: inject dependencies
        # =========================
        self.graph_merger = RuntimeGraphMerger()
        self.graph_normalizer = RuntimeGraphNormalizer()
        self.graph_indexer = RuntimeGraphIndexer()

    # =========================
    # safe load
    # =========================
    def _load(self, path):
        data = self.loader.load_json(path)
        return data if data is not None else {}

    # =========================
    # main entry
    # =========================
    def assemble_runtime_graph(self, graph_refs):

        # =================================================
        # 1. load fragments
        # =================================================
        graph_fragments = []

        for key in ["base", "specific", "viral"]:
            for name in graph_refs.get(key, []):
                frag = self._load(
                    f"cellmaster/internalnet/graph/{name}.json"
                    )
                if frag:
                    graph_fragments.append(frag)

        # =================================================
        # 2. MERGE (FLAT STRUCTURE)
        # =================================================
        merged = self.graph_merger.merge_graph_group(graph_fragments)
        
        # =================================================
        # 3. BUILD NODE LIST
        # =================================================
        nodes = list(set(merged.get("nodes", [])))

        # =================================================
        # 4. BUILD BEHAVIOR LIST
        # =================================================
        behaviors = list(set(merged.get("behaviors", [])))

        # =================================================
        # 5. BUILD EDGE LIST
        # =================================================
        edges = merged.get("edges", [])

        # =================================================
        # 6. FINAL RUNTIME GRAPH (IMPORTANT)
        # =================================================
        runtime_graph = {

            "nodes": nodes,

            "behaviors": behaviors,

            "edges": edges,

            "metadata":
                merged.get(
                    "metadata",
                    {}
                ),

            "sources":
                merged.get(
                    "sources",
                    []
                )
        }

        # =================================================
        # 7. NORMALIZE
        # =================================================
        normalized = self.graph_normalizer.normalize_runtime_graph(runtime_graph)

        # =================================================
        # 8. INDEX
        # =================================================
        indexed = self.graph_indexer.build_indexes(normalized)

        # =================================================
        # 9. CONTEXT
        # =================================================
        return RuntimeGraphContext(indexed)
