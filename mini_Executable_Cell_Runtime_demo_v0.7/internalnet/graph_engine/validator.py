# internalnet/graph_engine/validator.py

from __future__ import annotations

from dataclasses import dataclass

from .schema import GraphDefinition, GraphEdge


class GraphValidationError(ValueError):
    """Raised when a graph definition is structurally invalid."""


@dataclass(frozen=True)
class ValidationIssue:
    message: str


class GraphValidator:
    """Validate the structural integrity of a graph definition.

    This validator checks graph structure and references only.
    It does not execute biological logic or determine whether a
    biological relationship is scientifically correct.
    """

    _VALID_GRAPH_TYPES: set[str] = {
        "common",
        "cell_specific",
    }

    _VALID_EDGE_TYPES: set[str] = {
        "node-node",
        "node-gene",
        "node-behavior",
        "gene-behavior",
    }

    def validate(self, graph: GraphDefinition) -> None:
        """Validate a graph.

        Raises:
            GraphValidationError: if the graph is structurally invalid.
        """
        issues = self.collect_issues(graph)

        if issues:
            messages = "\n".join(
                f"- {issue.message}" for issue in issues
            )
            raise GraphValidationError(
                f"Invalid graph '{graph.name}':\n{messages}"
            )

    def collect_issues(
        self,
        graph: GraphDefinition,
    ) -> tuple[ValidationIssue, ...]:
        """Return all structural validation issues."""
        issues: list[ValidationIssue] = []

        self._validate_graph_metadata(graph, issues)
        self._validate_member_names(graph, issues)
        self._validate_edges(graph, issues)

        return tuple(issues)

    def _validate_graph_metadata(
        self,
        graph: GraphDefinition,
        issues: list[ValidationIssue],
    ) -> None:
        if not graph.name.strip():
            issues.append(
                ValidationIssue("Graph name cannot be empty.")
            )

        if graph.type not in self._VALID_GRAPH_TYPES:
            issues.append(
                ValidationIssue(
                    f"Invalid graph type: {graph.type!r}."
                )
            )

    def _validate_member_names(
        self,
        graph: GraphDefinition,
        issues: list[ValidationIssue],
    ) -> None:
        collections = {
            "node": graph.nodes,
            "gene": graph.genes,
            "behavior": graph.behaviors,
        }

        for category, names in collections.items():
            seen: set[str] = set()

            for name in names:
                if not name.strip():
                    issues.append(
                        ValidationIssue(
                            f"Empty {category} name is not allowed."
                        )
                    )
                    continue

                if name in seen:
                    issues.append(
                        ValidationIssue(
                            f"Duplicate {category}: {name!r}."
                        )
                    )

                seen.add(name)

    def _validate_edges(
        self,
        graph: GraphDefinition,
        issues: list[ValidationIssue],
    ) -> None:
        edge_names: set[str] = set()

        for edge in graph.edges:
            self._validate_edge(
                graph,
                edge,
                edge_names,
                issues,
            )

    def _validate_edge(
        self,
        graph: GraphDefinition,
        edge: GraphEdge,
        edge_names: set[str],
        issues: list[ValidationIssue],
    ) -> None:
        if not edge.name.strip():
            issues.append(
                ValidationIssue("Edge name cannot be empty.")
            )
        elif edge.name in edge_names:
            issues.append(
                ValidationIssue(
                    f"Duplicate edge name: {edge.name!r}."
                )
            )

        edge_names.add(edge.name)

        if edge.type not in self._VALID_EDGE_TYPES:
            issues.append(
                ValidationIssue(
                    f"Invalid edge type {edge.type!r} "
                    f"for edge {edge.name!r}."
                )
            )
            return

        if not edge.source.strip():
            issues.append(
                ValidationIssue(
                    f"Edge {edge.name!r} has an empty source."
                )
            )

        if not edge.target.strip():
            issues.append(
                ValidationIssue(
                    f"Edge {edge.name!r} has an empty target."
                )
            )

