# internalnet/graph_engine/composer.py

from __future__ import annotations

from collections.abc import Iterable

from .repository import GraphRepository
from .schema import GraphDefinition


class GraphComposer:
    """Compose the graph definitions required by a cell.

    The composer selects and orders existing graph definitions.
    It does not modify, merge, validate, or execute graphs.
    """

    def __init__(self, repository: GraphRepository) -> None:
        self._repository = repository

    def compose(
        self,
        graph_names: Iterable[str],
    ) -> tuple[GraphDefinition, ...]:
        """Return the requested graph definitions in the given order."""
        return tuple(
            self._repository.get(name)
            for name in graph_names
        )
