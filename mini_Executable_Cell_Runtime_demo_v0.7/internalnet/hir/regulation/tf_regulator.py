from typing import Dict, Sequence

from internalnet.gene_engine.schema import GeneDefinition
from internalnet.node_engine.schema import NodeRuntimeState

from internalnet.hir.schema import (
    BehaviorIntention,
    TFRegulationDelta,
)
from internalnet.hir.regulation.repository import (
    TFElementRelationRepository,
)


class TFRegulator:

    def __init__(
        self,
        relation_repository: TFElementRelationRepository,
    ):
        self._relations = relation_repository

    def regulate(
        self,
        intention: BehaviorIntention,
        behavior_genes: Sequence[str],
        node_states: Dict[str, NodeRuntimeState],
        gene_definitions: Dict[str, GeneDefinition],
    ) -> TFRegulationDelta:

        delta = 0.0

        for gene_name in behavior_genes:
            gene_definition = gene_definitions.get(gene_name)

            if gene_definition is None:
                continue

            for element in gene_definition.elements:
                element_name = element["name"]

                element_value = float(
                    element.get("value", 1.0)
                )

                distance = float(
                    element.get("distance", 0.0)
                )

                distance_factor = self._distance_factor(
                    distance
                )

                relations = (
                    self._relations.find_by_element(
                        element_name
                    )
                )

                for relation in relations:
                    tf_state = node_states.get(relation.tf)

                    if tf_state is None:
                        continue

                    tf_activity = tf_state.states.get("nuclear", 0.0)

                    delta += (
                        tf_activity
                        * relation.value
                        * element_value
                        * distance_factor
                    )

        return TFRegulationDelta(
            behavior_name=intention.behavior_name,
            delta=delta,
        )

    @staticmethod
    def _distance_factor(distance: float) -> float:
        return 1.0 / (1.0 + max(distance, 0.0))
