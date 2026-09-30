from dataclasses import dataclass
from typing import Dict, List

from internalnet.runtime.state import NodeState
from internalnet.hir.type.repository import TypeEvidence


@dataclass(frozen=True)
class TypeEvidenceStatus:
    type_name: str
    upstream_complete: bool
    regulatory_complete: bool
    output_complete: bool
    complete: bool
    matched_count: int
    total_count: int

    @property
    def evidence(self) -> str:
        if self.complete:
            return "complete"

        if self.matched_count > 0:
            return "partial"

        return "none"


class TypeDetermination:

    def determine(
        self,
        evidence_list: List[TypeEvidence],
        node_states: Dict[str, NodeState],
    ) -> List[TypeEvidenceStatus]:

        return [
            self._evaluate_type(
                evidence=evidence,
                node_states=node_states,
            )
            for evidence in evidence_list
        ]

    @classmethod
    def _evaluate_type(
        cls,
        evidence: TypeEvidence,
        node_states: Dict[str, NodeState],
    ) -> TypeEvidenceStatus:

        identity = evidence.identity

        upstream_complete = cls._all_nodes_present(
            identity.upstream,
            node_states,
        )

        regulatory_complete = cls._all_nodes_present(
            identity.regulatory,
            node_states,
        )

        output_complete = cls._all_nodes_present(
            identity.output,
            node_states,
        )

        matched_count = (
            cls._matched_count(identity.upstream, node_states)
            + cls._matched_count(identity.regulatory, node_states)
            + cls._matched_count(identity.output, node_states)
        )

        total_count = (
            len(identity.upstream)
            + len(identity.regulatory)
            + len(identity.output)
        )

        complete = (
            upstream_complete
            and regulatory_complete
            and output_complete
        )

        return TypeEvidenceStatus(
            type_name=evidence.type_name,
            upstream_complete=upstream_complete,
            regulatory_complete=regulatory_complete,
            output_complete=output_complete,
            complete=complete,
            matched_count=matched_count,
            total_count=total_count,
        )

    @staticmethod
    def _all_nodes_present(
        node_names: List[str],
        node_states: Dict[str, NodeState],
    ) -> bool:
        return all(
            name in node_states
            and any(value != 0.0 for value in node_states[name].states.values())
            for name in node_names
        )

    @staticmethod
    def _matched_count(
        node_names: List[str],
        node_states: Dict[str, NodeState],
    ) -> int:
        return sum(
            1
            for name in node_names
            if name in node_states
            and any(value != 0.0 for value in node_states[name].states.values())
        )
