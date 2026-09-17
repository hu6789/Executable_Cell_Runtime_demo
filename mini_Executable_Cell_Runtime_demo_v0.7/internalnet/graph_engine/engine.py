# internalnet/graph_engine/engine.py

from __future__ import annotations

from collections.abc import Iterable

from .composer import GraphComposer
from .repository import GraphRepository
from .resolver import GraphResolver
from .schema import GraphDefinition, GraphEdge
from .validator import GraphValidator


class GraphEngine:
    """Facade for graph definition management and structural resolution.

    GraphEngine coordinates repository, validation, composition,
    and structural resolution.

    It does not execute biological logic, inspect RuntimeState,
    access World, evaluate thresholds, or execute behaviors.
    """

    def __init__(
        self,
        repository: GraphRepository | None = None,
        validator: GraphValidator | None = None,
    ) -> None:
        self._repository = repository or GraphRepository()
        self._validator = validator or GraphValidator()

        self._composer = GraphComposer(self._repository)

    def register(self, graph: GraphDefinition) -> None:
        """Validate and register a graph definition."""
        self._validator.validate(graph)
        self._repository.register(graph)

    def validate(self, graph: GraphDefinition) -> None:
        """Validate a graph definition."""
        self._validator.validate(graph)

    def get(self, name: str) -> GraphDefinition:
        """Return a registered graph definition."""
        return self._repository.get(name)

    def has(self, name: str) -> bool:
        """Return whether a graph is registered."""
        return self._repository.has(name)

    def names(self) -> tuple[str, ...]:
        """Return the names of all registered graphs."""
        return self._repository.names()

    def compose(
        self,
        graph_names: Iterable[str],
    ) -> tuple[GraphDefinition, ...]:
        """Compose the graph definitions required by a cell."""
        return self._composer.compose(graph_names)

    def resolver(
        self,
        graph_names: Iterable[str],
    ) -> GraphResolver:
        """Create a resolver for the composed graphs."""
        graphs = self.compose(graph_names)
        return GraphResolver(graphs)

    def all_edges(
        self,
        graph_names: Iterable[str],
    ) -> tuple[GraphEdge, ...]:
        """Return all structural edges from the composed graphs."""
        return self.resolver(graph_names).all_edges()
