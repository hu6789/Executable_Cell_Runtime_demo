# internalnet/graph_engine/repository.py

from __future__ import annotations

from typing import Iterable

from .schema import GraphDefinition


class GraphRepository:
    """Repository for registered graph definitions.

    The repository only stores and retrieves graph definitions.
    It does not compose, validate, resolve, or execute graphs.
    """

    def __init__(self, graphs: Iterable[GraphDefinition] | None = None) -> None:
        self._graphs: dict[str, GraphDefinition] = {}

        if graphs is not None:
            for graph in graphs:
                self.register(graph)

    def register(self, graph: GraphDefinition) -> None:
        """Register a graph definition by name."""
        if graph.name in self._graphs:
            raise ValueError(
                f"Graph already registered: {graph.name}"
            )

        self._graphs[graph.name] = graph

    def get(self, name: str) -> GraphDefinition:
        """Return a registered graph definition."""
        try:
            return self._graphs[name]
        except KeyError as exc:
            raise KeyError(
                f"Graph not found: {name}"
            ) from exc

    def has(self, name: str) -> bool:
        """Return whether a graph is registered."""
        return name in self._graphs

    def names(self) -> tuple[str, ...]:
        """Return registered graph names."""
        return tuple(self._graphs.keys())

    def all(self) -> tuple[GraphDefinition, ...]:
        """Return all registered graph definitions."""
        return tuple(self._graphs.values())

    def remove(self, name: str) -> GraphDefinition:
        """Remove and return a registered graph definition."""
        try:
            return self._graphs.pop(name)
        except KeyError as exc:
            raise KeyError(
                f"Graph not found: {name}"
            ) from exc

    def clear(self) -> None:
        """Remove all registered graph definitions."""
        self._graphs.clear()

    def __len__(self) -> int:
        return len(self._graphs)

    def __contains__(self, name: str) -> bool:
        return name in self._graphs
