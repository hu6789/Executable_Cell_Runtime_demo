
# compute_plan/builder.py

from __future__ import annotations

from collections.abc import Iterable

from internalnet.graph_engine.engine import GraphEngine

from .schema import CellComputePlan


class ComputePlanBuilder:
    """Build a cell-specific compute plan from graph definitions.

    The builder adapts GraphEngine output into CellComputePlan
    and resolves execution dependencies between nodes.

    It does not access World or RuntimeState, or execute biological
    calculations.
    """

    def __init__(self, graph_engine: GraphEngine) -> None:
        self._graph_engine = graph_engine

    def build(
        self,
        cell_id: str,
        graph_ids: Iterable[str],
    ) -> CellComputePlan:
        """Build a compute plan for one cell."""

        graph_ids = tuple(graph_ids)

        graphs = self._graph_engine.compose(graph_ids)

        edges = self._graph_engine.all_edges(graph_ids)

        candidate_nodes = self._unique(
            name
            for graph in graphs
            for name in graph.nodes
        )

        candidate_genes = self._unique(
            name
            for graph in graphs
            for name in graph.genes
        )

        candidate_behavior_names = (
            [
                name
                for graph in graphs
                for name in graph.behaviors
            ]
            + [
                edge.target
                for edge in edges
                if edge.type in {"node-behavior", "gene-behavior"}
            ]
        )

        candidate_behaviors = self._unique(candidate_behavior_names)

        node_execution_order = self._resolve_node_execution_order(
            candidate_nodes=candidate_nodes,
            edges=edges,
        )

        return CellComputePlan(
            cell_id=cell_id,
            graph_ids=graph_ids,
            candidate_nodes=candidate_nodes,
            candidate_genes=candidate_genes,
            candidate_behaviors=candidate_behaviors,
            edges=edges,
            node_execution_order=node_execution_order,
        )

    @staticmethod
    def _resolve_node_execution_order(
        candidate_nodes: tuple[str, ...],
        edges,
    ) -> tuple[str, ...]:
        """Resolve node execution order from node-node dependencies."""

        dependencies: dict[str, set[str]] = {
            node: set()
            for node in candidate_nodes
        }

        dependents: dict[str, set[str]] = {
            node: set()
            for node in candidate_nodes
        }

        for edge in edges:
            if edge.type != "node-node":
                continue

            if edge.source not in dependencies:
                raise ValueError(
                    f"Node dependency source not found: {edge.source}"
                )

            if edge.target not in dependencies:
                raise ValueError(
                    f"Node dependency target not found: {edge.target}"
                )

            dependencies[edge.target].add(edge.source)
            dependents[edge.source].add(edge.target)

        ready = [
            node
            for node in candidate_nodes
            if not dependencies[node]
        ]

        order: list[str] = []

        while ready:
            node = ready.pop(0)
            order.append(node)

            for dependent in candidate_nodes:
                if node not in dependencies[dependent]:
                    continue

                dependencies[dependent].remove(node)

                if not dependencies[dependent]:
                    ready.append(dependent)

        if len(order) != len(candidate_nodes):
            raise ValueError(
                "Circular node dependency detected"
            )

        return tuple(order)

    @staticmethod
    def _unique(
        values: Iterable[str],
    ) -> tuple[str, ...]:
        """Return values in first-seen order without duplicates."""

        seen: set[str] = set()
        result: list[str] = []

        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)

        return tuple(result)

