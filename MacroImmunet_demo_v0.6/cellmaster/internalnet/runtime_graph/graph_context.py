# cellmaster/internalnet/runtime_graph/graph_context.py

from .behavior_definition_loader import (
    BehaviorDefinitionLoader
)

# =========================================
# Runtime Graph Context
# =========================================

class RuntimeGraphContext:

    """
    runtime execution graph context

    responsibilities:
        - expose runtime graph access API
        - provide execution-oriented graph lookup
        - isolate runtime engines from graph storage

    DOES NOT:
        - execute graph logic
        - modify graph structure
        - validate runtime semantics
    """

    def __init__(
        self,
        indexed_graph
    ):

        self.graph = indexed_graph
        
        self.behavior_loader = (
            BehaviorDefinitionLoader()
        )

    # =====================================
    # topology
    # =====================================

    def get_runtime_nodes(
        self
    ):

        return self.graph.get(
            "nodes",
            []
        )

    def get_runtime_behaviors(
        self
    ):

        return self.graph.get(
            "behaviors",
            []
        )

    def get_runtime_edges(
        self
    ):

        return self.graph.get(
            "edges",
            []
        )

    # =====================================
    # edge lookup
    # =====================================

    def get_outgoing_edges(
        self,
        source_node
    ):

        return (

            self.graph
            .get(
                "edges_by_source",
                {}
            )
            .get(
                source_node,
                []
            )
        )

    def get_incoming_edges(
        self,
        target_node
    ):

        return (

            self.graph
            .get(
                "edges_by_target",
                {}
            )
            .get(
                target_node,
                []
            )
        )

    def get_edges_by_type(
        self,
        edge_type
    ):

        return (

            self.graph
            .get(
                "edges_by_type",
                {}
            )
            .get(
                edge_type,
                []
            )
        )

    def get_edges_by_category(
        self,
        category
    ):

        return (

            self.graph
            .get(
                "edges_by_category",
                {}
            )
            .get(
                category,
                []
            )
        )
    
    def get_behavior_defs(self):

        result = {}

        for behavior_name in self.graph.get(
            "behaviors",
            []
        ):

            try:

                result[
                    behavior_name
                ] = self.behavior_loader.load(
                    behavior_name
                )

            except FileNotFoundError:

                pass
  
        return result
    
    # =====================================
    # metadata
    # =====================================

    def get_metadata(
        self
    ):

        return self.graph.get(
            "metadata",
            {}
        )

    def get_sources(
        self
    ):

        return self.graph.get(
            "sources",
            []
        )

    # =====================================
    # compatibility aliases
    # =====================================

    def get_nodes(self):

        return self.get_runtime_nodes()

    def get_behaviors(self):

        return self.get_runtime_behaviors()

    def get_edges(self):

        return self.get_runtime_edges()

    def get_incoming(
        self,
        node_id
    ):

        return self.get_incoming_edges(
            node_id
        )

    def get_outgoing(
        self,
        node_id
    ):

        return self.get_outgoing_edges(
            node_id
        )
