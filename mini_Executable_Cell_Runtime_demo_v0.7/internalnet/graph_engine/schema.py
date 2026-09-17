from dataclasses import dataclass, field
from typing import List, Literal

GraphType = Literal["common", "cell_specific"]

EdgeType = Literal[
    "node-node",
    "node-gene",
    "node-behavior",
    "gene-behavior",
]


@dataclass(frozen=True)
class GraphEdge:
    name: str
    type: EdgeType
    source: str
    target: str
    required: bool = True


@dataclass(frozen=True)
class GraphDefinition:
    name: str
    type: GraphType
    nodes: List[str] = field(default_factory=list)
    genes: List[str] = field(default_factory=list)
    behaviors: List[str] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
