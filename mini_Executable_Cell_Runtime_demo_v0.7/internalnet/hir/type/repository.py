import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TypeIdentity:
    upstream: List[str] = field(default_factory=list)
    regulatory: List[str] = field(default_factory=list)
    output: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class TypeEvidence:
    type_name: str
    identity: TypeIdentity


@dataclass(frozen=True)
class TypeDefinition:
    type_name: str
    current_graphs: List[str] = field(default_factory=list)
    latent_graphs: List[str] = field(default_factory=list)
    legacy_graphs: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class TypeTransitionRule:
    name: str
    evidence: str
    lineage_relation: Optional[str]
    state: str


class TypeEvidenceRepository:

    def __init__(self, path: Path):
        self._path = path
        self._evidence = self._load()

    def _load(self) -> List[TypeEvidence]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        evidence = []

        for item in data.get("types", []):
            identity_data = item.get("identity", {})

            identity = TypeIdentity(
                upstream=identity_data.get("upstream", []),
                regulatory=identity_data.get("regulatory", []),
                output=identity_data.get("output", []),
            )

            evidence.append(
                TypeEvidence(
                    type_name=item["name"],
                    identity=identity,
                )
            )

        return evidence

    def find_by_type(self, type_name: str) -> TypeEvidence:
        for evidence in self._evidence:
            if evidence.type_name == type_name:
                return evidence

        raise KeyError(
            "Type evidence not found: {}".format(type_name)
        )

    def all(self) -> List[TypeEvidence]:
        return list(self._evidence)


class TypeDefinitionRepository:

    def __init__(self, path: Path):
        self._path = path
        self._definitions = self._load()

    def _load(self) -> List[TypeDefinition]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        definitions = []

        for item in data.get("types", []):
            graphs = item.get("graphs", {})

            definitions.append(
                TypeDefinition(
                    type_name=item["name"],
                    current_graphs=graphs.get("current", []),
                    latent_graphs=graphs.get("latent", []),
                    legacy_graphs=graphs.get("legacy", []),
                )
            )

        return definitions

    def find_by_type(self, type_name: str) -> TypeDefinition:
        for definition in self._definitions:
            if definition.type_name == type_name:
                return definition

        raise KeyError(
            "Type definition not found: {}".format(type_name)
        )

    def all(self) -> List[TypeDefinition]:
        return list(self._definitions)


class TypeTransitionRepository:

    def __init__(self, path: Path):
        self._path = path
        self._rules = self._load()

    def _load(self) -> List[TypeTransitionRule]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        rules = []

        for item in data.get("rules", []):
            condition = item.get("condition", {})
            result = item.get("result", {})

            rules.append(
                TypeTransitionRule(
                    name=item["name"],
                    evidence=condition["evidence"],
                    lineage_relation=condition.get(
                        "lineage_relation"
                    ),
                    state=result["state"],
                )
            )

        return rules

    def find_by_name(self, name: str) -> TypeTransitionRule:
        for rule in self._rules:
            if rule.name == name:
                return rule

        raise KeyError(
            "Type transition rule not found: {}".format(name)
        )

    def all(self) -> List[TypeTransitionRule]:
        return list(self._rules)
        
        
@dataclass(frozen=True)
class LineageNode:
    type_name: str
    parent: Optional[str]
    children: List[str] = field(default_factory=list)


class LineageRepository:

    def __init__(self, path: Path):
        self._path = path
        self._nodes = self._load()

    def _load(self) -> List[LineageNode]:
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = []

        for item in data.get("nodes", []):
            nodes.append(
                LineageNode(
                    type_name=item["name"],
                    parent=item.get("parent"),
                    children=item.get("children", []),
                )
            )

        return nodes

    def find_by_type(self, type_name: str) -> LineageNode:
        for node in self._nodes:
            if node.type_name == type_name:
                return node

        raise KeyError(
            "Lineage node not found: {}".format(type_name)
        )

    def all(self) -> List[LineageNode]:
        return list(self._nodes)

    def relation(
        self,
        source_type: str,
        target_type: str,
    ) -> Optional[str]:

        if source_type == target_type:
            return None

        source = self.find_by_type(source_type)
        target = self.find_by_type(target_type)

        if target_type in source.children:
            return "descendant"

        if source_type in target.children:
            return "ancestor"

        return None
