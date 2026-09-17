# internalnet/gene_engine/repository.py

from typing import Dict, Iterable, Optional, Tuple

from .schema import GeneDefinition


class GeneRepository:
    """Repository for static GeneDefinition objects."""

    def __init__(
        self,
        genes: Optional[Iterable[GeneDefinition]] = None,
    ):
        self._genes: Dict[str, GeneDefinition] = {}

        if genes is not None:
            for gene in genes:
                self.register(gene)

    def register(self, gene: GeneDefinition) -> None:
        if gene.name in self._genes:
            raise ValueError(
                f"Gene already registered: {gene.name}"
            )

        self._genes[gene.name] = gene

    def get(self, name: str) -> GeneDefinition:
        try:
            return self._genes[name]
        except KeyError:
            raise KeyError(f"Unknown gene: {name}") from None

    def has(self, name: str) -> bool:
        return name in self._genes

    def names(self) -> Tuple[str, ...]:
        return tuple(self._genes.keys())
