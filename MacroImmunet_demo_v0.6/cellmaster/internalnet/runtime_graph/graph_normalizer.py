# cellmaster/internalnet/runtime_graph/graph_normalizer.py


# =========================================
# Runtime Graph Normalizer
# =========================================

class RuntimeGraphNormalizer:

    """
    runtime graph schema normalizer

    responsibilities:
        - normalize graph topology
        - normalize graph edges
        - apply graph defaults

    DOES NOT:
        - load node definitions
        - load behavior definitions
        - validate biology
        - build indexes
    """

    def __init__(self):

        pass

    # =====================================
    # normalize runtime graph
    # =====================================

    def normalize_runtime_graph(
        self,
        runtime_graph
    ):

        return {

            "nodes":

                runtime_graph.get(
                    "nodes",
                    []
                ),

            "behaviors":

                runtime_graph.get(
                    "behaviors",
                    []
                ),

            "edges":

                self.normalize_edges(

                    runtime_graph.get(
                        "edges",
                        []
                    )
                ),

            "metadata":

                runtime_graph.get(
                    "metadata",
                    {}
                ),

            "sources":

                runtime_graph.get(
                    "sources",
                    []
                )
        }

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

                # -------------------------
                # topology
                # -------------------------

                "source":

                    edge.get(
                        "source"
                    ),

                "target":

                    edge.get(
                        "target"
                    ),

                # -------------------------
                # edge typing
                # -------------------------

                "edge_type":

                    edge.get(
                        "edge_type",
                        "node_to_node"
                    ),

                # -------------------------
                # contribution semantics
                # -------------------------

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

                # -------------------------
                # runtime
                # -------------------------

                "runtime_enabled":

                    edge.get(
                        "runtime_enabled",
                        True
                    ),

                # -------------------------
                # metadata
                # -------------------------

                "metadata":

                    edge.get(
                        "metadata",
                        {}
                    )
            })

        return normalized
