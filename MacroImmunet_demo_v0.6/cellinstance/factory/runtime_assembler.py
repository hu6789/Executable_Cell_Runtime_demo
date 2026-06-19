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
        # 2. passive fragments
        # =================================================
        passive_fragments = []
        for name in graph_refs.get("passive", []):
            frag = self._load(
                f"cellmaster/internalnet/passive_graph/{name}.json"
            )
            if frag:
                passive_fragments.append(frag)

        # =================================================
        # 3. MERGE (FLAT STRUCTURE)
        # =================================================
        merged = self.graph_merger.merge_graph_group(graph_fragments)
        passive = self.graph_merger.merge_graph_group(passive_fragments)

        # =================================================
        # 4. BUILD NODE LIST
        # =================================================
        nodes = list(set(merged.get("nodes", [])))

        # =================================================
        # 5. BUILD BEHAVIOR LIST
        # =================================================
        behaviors = list(set(merged.get("behaviors", [])))

        # =================================================
        # 6. BUILD EDGE LIST
        # =================================================
        edges = merged.get("edges", [])

        # =================================================
        # 7. PASSIVE
        # =================================================
        passive_nodes = list(set(passive.get("nodes", [])))
        passive_systems = passive.get("behaviors", [])

        # =================================================
        # 8. FINAL RUNTIME GRAPH (IMPORTANT)
        # =================================================
        runtime_graph = {
            "nodes": nodes,
            "behaviors": behaviors,
            "edges": edges,

            "passive_nodes": passive_nodes,
            "passive_systems": passive_systems,
        }

        # =================================================
        # 9. NORMALIZE
        # =================================================
        normalized = self.graph_normalizer.normalize_runtime_graph(runtime_graph)

        # =================================================
        # 10. INDEX
        # =================================================
        indexed = self.graph_indexer.build_indexes(normalized)

        # =================================================
        # 11. CONTEXT
        # =================================================
        return RuntimeGraphContext(indexed)
