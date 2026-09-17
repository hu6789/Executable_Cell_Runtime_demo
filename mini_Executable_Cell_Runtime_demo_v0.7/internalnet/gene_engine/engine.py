# internalnet/gene_engine/engine.py

from typing import Dict, Optional

from internalnet.node_engine.schema import NodeRuntimeState

from .formulation import GeneFormulationEngine
from .repository import GeneRepository
from internalnet.runtime.state import GeneState
from internalnet.runtime.delta import GeneDelta


class GeneEngine:
    """
    Thin façade for Gene runtime calculation.

    Responsibilities:
    - retrieve GeneDefinition from GeneRepository
    - delegate Node -> Gene calculation to GeneFormulationEngine

    Does NOT:
    - resolve Graph
    - resolve TF -> Element relationships
    - perform HIR regulation
    - tune Behavior
    - access World
    """

    def __init__(
        self,
        repository: GeneRepository,
        formulation: Optional[GeneFormulationEngine] = None,
    ):
        self._repository = repository
        self._formulation = (
            formulation
            if formulation is not None
            else GeneFormulationEngine()
        )

    def get(self, name: str):
        return self._repository.get(name)

    def has(self, name: str) -> bool:
        return self._repository.has(name)

    def names(self):
        return self._repository.names()

    def run(
        self,
        gene_name,
        gene_state,
        node_states,
    )-> GeneDelta:
        gene = self._repository.get(gene_name)

        return self._formulation.evaluate(
            gene=gene,
            gene_state=gene_state,
            node_states=node_states,
        )
