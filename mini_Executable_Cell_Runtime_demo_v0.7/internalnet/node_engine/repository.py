# internalnet/node_engine/repository.py

from __future__ import annotations

from typing import Iterable

from .schema import NodeDefinition


class NodeRepository:
    """Repository for registered node definitions.

    The repository only stores and retrieves node definitions.
    It does not calculate formulations, execute transitions,
    resolve graphs, or access runtime state.
    """

    def __init__(
        self,
        nodes: Iterable[NodeDefinition] | None = None
    ) -> None:
        self._nodes: dict[str, NodeDefinition] = {}

        if nodes is not None:
            for node in nodes:
                self.register(node)

    def register(self, node: NodeDefinition) -> None:
        """Register a node definition by name."""
        if node.name in self._nodes:
            raise ValueError(
                f"Node already registered: {node.name}"
            )

        self._nodes[node.name] = node

    def get(self, name: str) -> NodeDefinition:
        """Return a registered node definition."""
        try:
            return self._nodes[name]
        except KeyError as exc:
            raise KeyError(
                f"Node not found: {name}"
            ) from exc

    def has(self, name: str) -> bool:
        """Return whether a node is registered."""
        return name in self._nodes

    def names(self) -> tuple[str, ...]:
        """Return registered node names."""
        return tuple(self._nodes.keys())

    def all(self) -> tuple[NodeDefinition, ...]:
        """Return all registered node definitions."""
        return tuple(self._nodes.values())

    def remove(self, name: str) -> NodeDefinition:
        """Remove and return a registered node definition."""
        try:
            return self._nodes.pop(name)
        except KeyError as exc:
            raise KeyError(
                f"Node not found: {name}"
            ) from exc

    def clear(self) -> None:
        """Remove all registered node definitions."""
        self._nodes.clear()

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, name: str) -> bool:
        return name in self._nodes
