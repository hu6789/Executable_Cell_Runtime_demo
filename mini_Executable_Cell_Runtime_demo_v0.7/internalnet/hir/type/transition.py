from dataclasses import dataclass
from typing import List, Optional

from internalnet.hir.type.determination import (
    TypeEvidenceStatus,
)
from internalnet.hir.type.repository import (
    LineageRepository,
    TypeTransitionRepository,
)


@dataclass(frozen=True)
class TypeTransitionResult:
    type_name: str
    state: str


class TypeTransition:

    def __init__(
        self,
        lineage_repository: LineageRepository,
        transition_repository: TypeTransitionRepository,
    ):
        self._lineage_repository = lineage_repository
        self._transition_repository = transition_repository

    def resolve(
        self,
        current_type: Optional[str],
        statuses: List[TypeEvidenceStatus],
    ) -> List[TypeTransitionResult]:

        results = []

        for status in statuses:
            state = self._resolve_state(
                current_type=current_type,
                status=status,
            )

            if state is None:
                continue

            results.append(
                TypeTransitionResult(
                    type_name=status.type_name,
                    state=state,
                )
            )

        return results

    def _resolve_state(
        self,
        current_type: Optional[str],
        status: TypeEvidenceStatus,
    ) -> Optional[str]:

        rule = self._find_rule(
            evidence=status.evidence,
            current_type=current_type,
            target_type=status.type_name,
        )

        if rule is None:
            return None

        return rule.state

    def _find_rule(
        self,
        evidence: str,
        current_type: Optional[str],
        target_type: str,
    ):

        if evidence == "complete":
            return self._find_transition_rule(
                evidence="complete",
                lineage_relation=None,
            )

        if evidence != "partial":
            return None

        if current_type is None:
            return None

        relation = self._lineage_repository.relation(
            current_type,
            target_type,
        )

        if relation is None:
            return None

        return self._find_transition_rule(
            evidence="partial",
            lineage_relation=relation,
        )

    def _find_transition_rule(
        self,
        evidence: str,
        lineage_relation: Optional[str],
    ):

        for rule in self._transition_repository.all():
            if rule.evidence != evidence:
                continue

            if rule.lineage_relation != lineage_relation:
                continue

            return rule

        return None
