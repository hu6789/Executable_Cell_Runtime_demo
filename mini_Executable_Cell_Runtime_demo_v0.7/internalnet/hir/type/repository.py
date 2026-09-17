import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class TypeCriterion:
    type_name: str
    required: List[Dict[str, Any]] = field(default_factory=list)
    supporting: List[Dict[str, Any]] = field(default_factory=list)


class TypeCriteriaRepository:

    def __init__(self, path: Path):
        self._path = path
        self._criteria = self._load()

    def _load(self) -> List[TypeCriterion]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            TypeCriterion(
                type_name=item["type"],
                required=item.get("required", []),
                supporting=item.get("supporting", []),
            )
            for item in data.get("criteria", [])
        ]

    def find_by_type(self, type_name: str) -> TypeCriterion:
        for criterion in self._criteria:
            if criterion.type_name == type_name:
                return criterion

        raise KeyError(
            "Type criteria not found: {}".format(type_name)
        )

    def all(self) -> List[TypeCriterion]:
        return list(self._criteria)
