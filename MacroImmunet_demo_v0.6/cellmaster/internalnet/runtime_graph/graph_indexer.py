# cellmaster/internalnet/runtime_graph/graph_indexer.py


# =========================================
# Runtime Graph Indexer
# =========================================

class RuntimeGraphIndexer:

    """
    runtime graph execution indexer

    responsibilities:
        - index graph edges
        - build runtime lookup tables
        - accelerate runtime traversal
        - expose execution-oriented graph views

    DOES NOT:
        - execute runtime logic
        - validate graph semantics
        - modify graph structure
    """

    def __init__(self):

        pass

    # =====================================
    # build runtime graph indexes
    # =====================================

    def build_indexes(
        self,
        normalized_graph
    ):

        indexed_graph = {}

        for group_name, group_data in (

            normalized_graph.items()
        ):

            indexed_graph[
                group_name
            ] = self.index_graph_group(
                group_data
            )

        return indexed_graph

    # =====================================
    # index graph group
    # =====================================

    def index_graph_group(
        self,
        group_data
    ):

        edges = group_data.get(
            "edges",
            []
        )

        return {

            # =============================
            # original normalized graph
            # =============================

            "nodes":

                group_data.get(
                    "nodes",
                    []
                ),

            "edges":
                edges,

            "metadata":

                group_data.get(
                    "metadata",
                    []
                ),

            "sources":

                group_data.get(
                    "sources",
                    []
                ),

            # =============================
            # execution indexes
            # =============================

            "edges_by_source":

                self.index_by_source(
                    edges
                ),

            "edges_by_target":

                self.index_by_target(
                    edges
                ),

            "edges_by_type":

                self.index_by_type(
                    edges
                ),

            "edges_by_category":

                self.index_by_category(
                    edges
                )
        }

    # =====================================
    # source index
    # =====================================

    def index_by_source(
        self,
        edges
    ):

        indexed = {}

        for edge in edges:

            source = edge.get(
                "source"
            )

            if source is None:

                continue

            indexed.setdefault(
                source,
                []
            ).append(edge)

        return indexed

    # =====================================
    # target index
    # =====================================

    def index_by_target(
        self,
        edges
    ):

        indexed = {}

        for edge in edges:

            target = edge.get(
                "target"
            )

            if target is None:

                continue

            indexed.setdefault(
                target,
                []
            ).append(edge)

        return indexed

    # =====================================
    # edge type index
    # =====================================

    def index_by_type(
        self,
        edges
    ):

        indexed = {}

        for edge in edges:

            edge_type = edge.get(
                "edge_type",
                "unknown"
            )

            indexed.setdefault(
                edge_type,
                []
            ).append(edge)

        return indexed

    # =====================================
    # contribution category index
    # =====================================

    def index_by_category(
        self,
        edges
    ):

        indexed = {}

        for edge in edges:

            category = edge.get(
                "contribution_category",
                "activation"
            )

            indexed.setdefault(
                category,
                []
            ).append(edge)

        return indexed
