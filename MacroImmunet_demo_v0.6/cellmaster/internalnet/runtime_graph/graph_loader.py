# cellmaster/internalnet/runtime_graph/graph_loader.py

import json
from pathlib import Path

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
       
# =========================================
# Runtime Graph Loader
# =========================================

class RuntimeGraphLoader:

    """
    runtime graph schema loader

    responsibilities:
        - load node graph schemas
        - load behavior graph schemas
        - load passive graph schemas
        - load HIR profiles
        - expose raw graph fragments

    DOES NOT:
        - merge graph fragments
        - normalize graph structure
        - build runtime indexes
        - execute graph logic
    """

    def __init__(self):
        pass

    # =====================================
    # load runtime graph package
    # =====================================

    def load_runtime_graph(
        self,
        graph_dir
    ):

        graph_dir = Path(graph_dir)

        runtime_graph = {

            "node_graphs":
                self.load_graph_group(
                    graph_dir / "nodes"
                ),

            "behavior_graphs":
                self.load_graph_group(
                    graph_dir / "behaviors"
                ),

            "passive_graphs":
                self.load_graph_group(
                    graph_dir / "passives"
                ) + self.load_graph_group(
                    graph_dir.parent / "aip" / "viral_passive"
                ),

            "hir_profiles":
                self.load_graph_group(
                    graph_dir / "hir"
                )
        }

        return runtime_graph

    # =====================================
    # load graph group
    # =====================================

    def load_graph_group(
        self,
        group_dir
    ):

        loaded_graphs = []

        if not group_dir.exists():
            return loaded_graphs

        for path in sorted(group_dir.glob("*.json")):

            graph = self.load_json(path)

            if graph is None:
                continue

            loaded_graphs.append(graph)

            debug_print(
                "[RuntimeGraphLoader]",
                "loaded:",
                path.name
            )

        return loaded_graphs

    # =====================================
    # load json file
    # =====================================

    def load_json(
        self,
        path
    ):

        try:
            with open(path, "r") as f:
                return json.load(f)

        except Exception as e:

            debug_print("[RuntimeGraphLoader] failed:", path)
            debug_print(e)

            return None
