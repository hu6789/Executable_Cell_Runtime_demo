# internalnet/behavior_engine/input_resolver.py

from dataclasses import dataclass, field
from typing import Dict

from internalnet.compute_plan.schema import CellComputePlan
from internalnet.runtime.state import GeneState, NodeState


@dataclass(frozen=True)
class BehaviorInputs:
    """Runtime inputs resolved for a behavior."""

    nodes: Dict[str, NodeState] = field(default_factory=dict)
    genes: Dict[str, GeneState] = field(default_factory=dict)

@dataclass(frozen=True)
class BehaviorExecution:
    """One independent execution of a behavior."""

    behavior_name: str
    source_type: str
    source_name: str
    inputs: BehaviorInputs

class BehaviorInputResolver:
    """Resolve behavior inputs from Graph edges in a CellComputePlan."""

    def resolve(
        self,
        behavior_name: str,
        plan: CellComputePlan,
        node_states: Dict[str, NodeState],
        gene_states: Dict[str, GeneState],
    ) -> BehaviorInputs:
        nodes = {}
        genes = {}

        for edge in plan.edges:
            if edge.target != behavior_name:
                continue

            if edge.type == "node-behavior":
                if edge.source not in node_states:
                    raise KeyError(
                        f"Missing NodeState for behavior input: "
                        f"{edge.source}"
                    )
                nodes[edge.source] = node_states[edge.source]

            elif edge.type == "gene-behavior":
                if edge.source not in gene_states:
                    raise KeyError(
                        f"Missing GeneState for behavior input: "
                        f"{edge.source}"
                    )
                genes[edge.source] = gene_states[edge.source]

        return BehaviorInputs(
            nodes=nodes,
            genes=genes,
        )
        
        
    def resolve_executions(
        self,
        behavior_name: str,
        plan: CellComputePlan,
        node_states: Dict[str, NodeState],
        gene_states: Dict[str, GeneState],
    ) -> list:
        executions = []

        for edge in plan.edges:
            if edge.target != behavior_name:
                continue

            if edge.type == "node-behavior":
                if edge.source not in node_states:
                    raise KeyError(
                        f"Missing NodeState for behavior input: "
                        f"{edge.source}"
                    )

                executions.append(
                    BehaviorExecution(
                        behavior_name=behavior_name,
                        source_type="node",
                        source_name=edge.source,
                        inputs=BehaviorInputs(
                            nodes={
                                edge.source: node_states[edge.source],
                            }
                        ),
                    )
                )

            elif edge.type == "gene-behavior":
                if edge.source not in gene_states:
                    raise KeyError(
                        f"Missing GeneState for behavior input: "
                        f"{edge.source}"
                    )

                executions.append(
                    BehaviorExecution(
                        behavior_name=behavior_name,
                        source_type="gene",
                        source_name=edge.source,
                        inputs=BehaviorInputs(
                            genes={
                                edge.source: gene_states[edge.source],
                            }
                        ),
                    )
                )

        return executions
