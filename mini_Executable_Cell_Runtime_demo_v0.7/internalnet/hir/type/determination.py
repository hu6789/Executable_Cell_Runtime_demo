from typing import Dict, Optional

from internalnet.runtime.state import GeneState, NodeState
from internalnet.hir.type.repository import TypeCriterion


class TypeDetermination:

    def determine(
        self,
        criteria,
        node_states: Dict[str, NodeState],
        gene_states: Dict[str, GeneState],
    ) -> Optional[str]:

        for criterion in criteria:
            if self._requirements_satisfied(
                criterion.required,
                node_states,
                gene_states,
            ):
                return criterion.type_name

        return None

    @staticmethod
    def _requirements_satisfied(
        requirements,
        node_states,
        gene_states,
    ) -> bool:

        for requirement in requirements:
            name = requirement["name"]
            source = requirement.get("source")
            threshold = float(requirement.get("threshold", 0.0))

            if source == "node":
                state = node_states.get(name)
                if state is None:
                    return False
                value = state.total

            elif source == "gene":
                state = gene_states.get(name)
                if state is None:
                    return False
                value = state.value

            else:
                return False

            if value < threshold:
                return False

        return True
