from dataclasses import dataclass, field
from typing import Dict

from internalnet.runtime.state import GeneState, NodeState


@dataclass
class Runtime:
    """
    Complete working snapshot of one cell.

    Runtime stores the current state of all Nodes and Genes.

    Engine calculations are not stored directly here.
    Engines produce Delta objects, and Runtime receives merged states.
    """

    id: str
    type: str

    node_states: Dict[str, NodeState] = field(
        default_factory=dict
    )

    gene_states: Dict[str, GeneState] = field(
        default_factory=dict
    )

    def get_node(self, name: str) -> NodeState:
        if name not in self.node_states:
            raise KeyError(
                "Node runtime state not found: {}".format(name)
            )

        return self.node_states[name]

    def has_node(self, name: str) -> bool:
        return name in self.node_states

    def set_node(self, state: NodeState) -> None:
        self.node_states[state.name] = state

    def get_gene(self, name: str) -> GeneState:
        if name not in self.gene_states:
            raise KeyError(
                "Gene runtime state not found: {}".format(name)
            )

        return self.gene_states[name]

    def has_gene(self, name: str) -> bool:
        return name in self.gene_states

    def set_gene(self, state: GeneState) -> None:
        self.gene_states[state.name] = state
