# internalnet/graph_engine/resolver.py

from __future__ import annotations

from collections.abc import Iterable

from .schema import EdgeType, GraphDefinition, GraphEdge


class GraphResolver:
    """Resolve structural relationships from composed graph definitions.

    The resolver only answers structural graph queries.
    It does not inspect biological values, calculate activity,
    evaluate thresholds, or execute behaviors.
    """

    def __init__(
        self,
        graphs: Iterable[GraphDefinition],
    ) -> None:
        self._graphs = tuple(graphs)

    def all_edges(self) -> tuple[GraphEdge, ...]:
        """Return all edges from the composed graphs."""
        return tuple(
            edge
            for graph in self._graphs
            for edge in graph.edges
        )

    def edges_from(
        self,
        source: str,
    ) -> tuple[GraphEdge, ...]:
        """Return all edges originating from a source."""
        return tuple(
            edge
            for edge in self.all_edges()
            if edge.source == source
        )

    def edges_to(
        self,
        target: str,
    ) -> tuple[GraphEdge, ...]:
        """Return all edges pointing to a target."""
        return tuple(
            edge
            for edge in self.all_edges()
            if edge.target == target
        )

    def edges_by_type(
        self,
        edge_type: EdgeType,
    ) -> tuple[GraphEdge, ...]:
        """Return all edges of a given type."""
        return tuple(
            edge
            for edge in self.all_edges()
            if edge.type == edge_type
        )

    def edges_from_by_type(
        self,
        source: str,
        edge_type: EdgeType,
    ) -> tuple[GraphEdge, ...]:
        """Return edges of a given type originating from a source."""
        return tuple(
            edge
            for edge in self.edges_from(source)
            if edge.type == edge_type
        )

    def edges_to_by_type(
        self,
        target: str,
        edge_type: EdgeType,
    ) -> tuple[GraphEdge, ...]:
        """Return edges of a given type pointing to a target."""
        return tuple(
            edge
            for edge in self.edges_to(target)
            if edge.type == edge_type
        )

    def has_source(self, source: str) -> bool:
        """Return whether the source participates in any edge."""
        return any(
            edge.source == source
            for edge in self.all_edges()
        )

    def has_target(self, target: str) -> bool:
        """Return whether the target participates in any edge."""
        return any(
            edge.target == target
            for edge in self.all_edges()
        )
