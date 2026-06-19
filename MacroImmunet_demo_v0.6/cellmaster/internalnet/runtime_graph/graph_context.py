# cellmaster/internalnet/runtime_graph/graph_context.py


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
        - provide unified graph traversal interface

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

    # =====================================
    # node outgoing edges
    # =====================================

    def get_outgoing_edges(
        self,
        group_name,
        source_node
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        edges_by_source = group.get(
            "edges_by_source",
            {}
        )

        return edges_by_source.get(
            source_node,
            []
        )

    # =====================================
    # node incoming edges
    # =====================================

    def get_incoming_edges(
        self,
        group_name,
        target_node
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        edges_by_target = group.get(
            "edges_by_target",
            {}
        )

        return edges_by_target.get(
            target_node,
            []
        )

    # =====================================
    # edge type lookup
    # =====================================

    def get_edges_by_type(
        self,
        group_name,
        edge_type
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        indexed = group.get(
            "edges_by_type",
            {}
        )

        return indexed.get(
            edge_type,
            []
        )

    # =====================================
    # contribution category lookup
    # =====================================

    def get_edges_by_category(
        self,
        group_name,
        category
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        indexed = group.get(
            "edges_by_category",
            {}
        )

        return indexed.get(
            category,
            []
        )

    # =====================================
    # runtime node lookup
    # =====================================

    def get_runtime_nodes(
        self,
        group_name
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        return group.get(
            "nodes",
            []
        )
    # =====================================
    # runtime edge lookup
    # =====================================

    def get_runtime_edges(
        self,
        group_name
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        return group.get(
            "edges",
            []
        )
    # =====================================
    # graph metadata
    # =====================================

    def get_metadata(
        self,
        group_name
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        return group.get(
            "metadata",
            []
        )

    # =====================================
    # graph sources
    # =====================================

    def get_sources(
        self,
        group_name
    ):

        group = self.graph.get(
            group_name,
            {}
        )

        return group.get(
            "sources",
            []
        )

    # =====================================
    # behavior
    # =====================================

    def get_behavior_defs(self):

        nodes = self.get_runtime_nodes(
            "behavior_graphs"
        )

        result = {}

        for node in nodes:

            name = node.get(
                "name"
            )

            if name:

                result[name] = node

        return result
    def get_behavior_edges(self):

        return (
            self.graph
            .get("behavior_graphs", {})
            .get("edges", [])
        )  
    # =====================================
    # Compatibility Alias Layer (A-PLAN)
    # =====================================

    def get_nodes(self, group_name):
        return self.get_runtime_nodes(group_name)


    def get_edges(self, group_name):
        return self.get_runtime_edges(group_name)


    def get_incoming(self, group_name, node_id):
        return self.get_incoming_edges(group_name, node_id)


    def get_outgoing(self, group_name, node_id):
        return self.get_outgoing_edges(group_name, node_id)      
        
    def get_runtime_edges(self, group_name):
        return self.graph.get(group_name, {}).get("edges", []) or []
         
    def get_passive_graph(self):
        return self.indexed_graph.get("passive_graphs", {})
