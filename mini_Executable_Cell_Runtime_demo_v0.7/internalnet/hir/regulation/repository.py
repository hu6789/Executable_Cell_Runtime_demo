from dataclasses import dataclass
import json
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class TFElementRelation:
    name: str
    tf: str
    element: str
    category: str
    effect: str
    value: float


class TFElementRelationRepository:

    def __init__(self, path: Path):
        self._path = path
        self._relations = self._load()

    def _load(self) -> List[TFElementRelation]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            TFElementRelation(
                name=item["name"],
                tf=item["tf"],
                element=item["element"],
                category=item["category"],
                effect=item["effect"],
                value=float(item["value"]),
            )
            for item in data.get("relations", [])
        ]

    def find_by_tf(self, tf_name: str) -> List[TFElementRelation]:
        return [
            relation
            for relation in self._relations
            if relation.tf == tf_name
        ]

    def find_by_element(
        self,
        element_name: str,
    ) -> List[TFElementRelation]:
        return [
            relation
            for relation in self._relations
            if relation.element == element_name
        ]
