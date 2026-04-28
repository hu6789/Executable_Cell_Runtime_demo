import os
import json

class GraphLoader:

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.graph_dir = os.path.join(base_dir, "graph")

    # =========================
    # 🔹 Node Graph
    # =========================
    def load_node_graph(self, graph_names):

        graph = {
            "nodes": {},
            "edges": []
        }

        for name in graph_names:

            path = os.path.join(self.graph_dir, f"{name}.json")

            with open(path) as f:
                g = json.load(f)

            # nodes
            nodes = g.get("nodes", {})

            if isinstance(nodes, dict):
                graph["nodes"].update(nodes)

            elif isinstance(nodes, list):
                for n in nodes:
                    if isinstance(n, str):
                        graph["nodes"][n] = {"node_id": n}
                    elif isinstance(n, dict):
                        graph["nodes"][n["node_id"]] = n

            # node edges
            graph["edges"].extend(g.get("edges", []))

        return graph

    # =========================
    # 🔹 Behavior Graph
    # =========================
    def load_behavior_graph(self, graph_names):
        if isinstance(graph_names, str):
            graph_names = [graph_names]

        graph = {
            "edges": [],
            "default_drive_normalize": False
        }

        for name in graph_names:

            path = os.path.join(self.graph_dir, f"{name}.json")

            with open(path) as f:
                g = json.load(f)

            graph["edges"].extend(g.get("edges", []))
 
            if g.get("default_drive_normalize"):
                graph["default_drive_normalize"] = True

        return graph
