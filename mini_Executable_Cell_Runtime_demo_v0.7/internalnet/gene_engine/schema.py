# internalnet/gene_engine/schema.py

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class GeneDefinition:
    """
    Static definition of a gene.

    Responsibilities:
    - define gene identity
    - define possible gene polymorphism / modification states
    - define regulatory elements associated with the gene
    - define the Node -> Gene calculation formula

    TF -> Element relationships are intentionally NOT stored here.
    Those relationships belong to the later HIR/regulation layer.
    """

    name: str
    category: Optional[str] = None
    polymorphism: List[str] = field(default_factory=list)
    elements: List[Dict[str, Any]] = field(default_factory=list)
    formula: Dict[str, Any] = field(default_factory=dict)



