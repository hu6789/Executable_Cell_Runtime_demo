from typing import List, Optional

from .determination import TypeEvidenceStatus
from .repository import LineageRepository


class TypeSelection:
    def __init__(self, lineage_repository: LineageRepository):
        self._lineage_repository = lineage_repository

    def select(
        self,
        current_type: Optional[str],
        statuses: List[TypeEvidenceStatus],
    ) -> Optional[str]:
        """
        Select the persistent type for the current tick.

        Rules:
        1. If the current type has complete identity evidence,
           keep the current type.
        2. If exactly one complete candidate exists, switch only
           when that candidate is a descendant of the current type.
        3. If there is no valid descendant candidate, keep current.
        4. If multiple complete candidates exist, keep current.
        """
        if current_type is not None:
            current_status = self._find_status(
                statuses,
                current_type,
            )

            if (
                current_status is not None
                and current_status.evidence == "complete"
            ):
                return current_type

        complete_candidates = [
            status
            for status in statuses
            if status.evidence == "complete"
        ]

        if len(complete_candidates) != 1:
            return current_type

        candidate = complete_candidates[0].type_name

        if current_type is None:
            return candidate

        relation = self._lineage_repository.relation(
            current_type,
            candidate,
        )

        if relation == "descendant":
            return candidate

        return current_type

    @staticmethod
    def _find_status(
        statuses: List[TypeEvidenceStatus],
        type_name: str,
    ) -> Optional[TypeEvidenceStatus]:
        for status in statuses:
            if status.type_name == type_name:
                return status

        return None
