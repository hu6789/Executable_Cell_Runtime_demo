# cellmaster/internalnet/runtime_graph/graph_normalizer.py


# =========================================
# Runtime Graph Normalizer
# =========================================

class RuntimeGraphNormalizer:

    """
    runtime graph schema normalizer

    responsibilities:
        - normalize graph edges
        - normalize node definitions
        - normalize runtime metadata
        - apply default runtime semantics
        - expose unified runtime contract

    DOES NOT:
        - execute graph logic
        - validate biology correctness
        - build runtime indexes
    """

    def __init__(self):

        pass

    # =====================================
    # normalize runtime graph
    # =====================================

    def normalize_runtime_graph(
        self,
        merged_graph
    ):

        normalized = {}

        for group_name, group_data in merged_graph.items():

            # 🧯 FIX: tolerate bad structure
            if isinstance(group_data, list):
                group_data = {
                    "nodes": group_data,
                    "edges": [],
                    "metadata": {},
                    "sources": []
                }

            normalized[
                group_name
            ] = self.normalize_graph_group(

                group_name,

                group_data
            )

        return normalized

    # =====================================
    # normalize graph group
    # =====================================

    def normalize_graph_group(
        self,
        group_name,
        group_data
    ):

        return {

            "nodes":

                (

                    self.normalize_behaviors(

                        group_data.get(
                            "behaviors",
                            []
                        )

                    )

                    if group_name == "behavior_graphs"

                    else

                    self.normalize_nodes(

                        group_data.get(
                            "nodes",
                            []
                        )
                    )
                ),

            "edges":

                self.normalize_edges(

                    group_data.get(
                        "edges",
                        []
                    )
                ),

            "metadata":

                group_data.get(
                    "metadata",
                    []
                ),

            "sources":

                group_data.get(
                    "sources",
                    []
                )
        }

    # =====================================
    # normalize nodes
    # =====================================

    def normalize_nodes(
        self,
        nodes
    ):

        normalized = []

        for node in nodes:

            # =========================
            # FIX: allow string nodes
            # =========================
            if isinstance(node, str):
                normalized.append({
                    "node_id": node,
                    "node_type": "continuous",
                    "default_value": 0.0,
                    "runtime_enabled": True,
                    "metadata": {}
                })
                continue

            normalized.append({
                "node_id": node.get("node_id"),
                "node_type": node.get("node_type", "continuous"),
                "default_value": node.get("default_value", 0.0),
                "runtime_enabled": node.get("runtime_enabled", True),
                "metadata": node.get("metadata", {})
            })

        return normalized
    # =====================================
    # normalize behaviors
    # =====================================

    def normalize_behaviors(
        self,
        behaviors
    ):

        normalized = []

        for behavior in behaviors:
 
            normalized.append({

                "name":

                    behavior.get(
                        "name"
                    ),

                "behavior_type":

                    behavior.get(
                        "behavior_type"
                    ),

                "behavior_category":

                    behavior.get(
                        "behavior_category"
                    ),

                "runtime_enabled":

                    behavior.get(
                        "runtime_enabled",
                        True
                    ),

                "behavior_gate":
 
                    behavior.get(
                        "behavior_gate",
                        {}
                    ),

                "resource_cost":

                    behavior.get(
                        "resource_cost",
                        {}
                    ),
  
                "external_outputs":

                    behavior.get(
                        "external_outputs",
                        []
                    ),

                "metadata":

                    behavior.get(
                        "metadata",
                        {}
                    )
            })

        return normalized
    # =====================================
    # normalize edges
    # =====================================

    def normalize_edges(
        self,
        edges
    ):

        normalized = []

        for edge in edges:

            normalized.append({

                # =========================
                # topology
                # =========================

                "source":

                    edge.get(
                        "source"
                    ),

                "target":

                    edge.get(
                        "target"
                    ),

                # =========================
                # edge typing
                # =========================

                "edge_type":

                    edge.get(
                        "edge_type",
                        "node_to_node"
                    ),

                # =========================
                # contribution semantics
                # =========================

                "weight":

                    edge.get(
                        "weight",
                        1.0
                    ),

                "transform":

                    edge.get(
                        "transform",
                        "identity"
                    ),

                "contribution_category":

                    edge.get(
                        "contribution_category",
                        "activation"
                    ),

                "contribution_gate":

                    edge.get(
                        "contribution_gate",
                        None
                    ),

                "participation_requirement":

                    edge.get(
                        "participation_requirement",
                        "optional"
                    ),

                # =========================
                # runtime flags
                # =========================

                "runtime_enabled":

                    edge.get(
                        "runtime_enabled",
                        True
                    ),

                # =========================
                # metadata
                # =========================

                "metadata":

                    edge.get(
                        "metadata",
                        {}
                    )
            })

        return normalized
