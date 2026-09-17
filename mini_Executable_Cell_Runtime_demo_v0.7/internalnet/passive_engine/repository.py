# internalnet/passive_engine/repository.py

from __future__ import annotations

from typing import Iterable

from .schema import PassiveDefinition


class PassiveRepository:
    """Repository for registered passive definitions.

    The repository only stores and retrieves passive definitions.
    It does not evaluate formulas, inspect node runtime state,
    or decide when a passive should execute.
    """

    def __init__(
        self,
        passives: Iterable[PassiveDefinition] | None = None
    ) -> None:
        self._passives: dict[str, PassiveDefinition] = {}

        if passives is not None:
            for passive in passives:
                self.register(passive)

    def register(self, passive: PassiveDefinition) -> None:
        """Register a passive definition by name."""
        if passive.name in self._passives:
            raise ValueError(
                f"Passive already registered: {passive.name}"
            )

        self._passives[passive.name] = passive

    def get(self, name: str) -> PassiveDefinition:
        """Return a registered passive definition."""
        try:
            return self._passives[name]
        except KeyError as exc:
            raise KeyError(
                f"Passive not found: {name}"
            ) from exc

    def has(self, name: str) -> bool:
        """Return whether a passive is registered."""
        return name in self._passives

    def names(self) -> tuple[str, ...]:
        """Return registered passive names."""
        return tuple(self._passives.keys())

    def all(self) -> tuple[PassiveDefinition, ...]:
        """Return all registered passive definitions."""
        return tuple(self._passives.values())

    def remove(self, name: str) -> PassiveDefinition:
        """Remove and return a registered passive definition."""
        try:
            return self._passives.pop(name)
        except KeyError as exc:
            raise KeyError(
                f"Passive not found: {name}"
            ) from exc

    def clear(self) -> None:
        """Remove all registered passive definitions."""
        self._passives.clear()

    def __len__(self) -> int:
        return len(self._passives)

    def __contains__(self, name: str) -> bool:
        return name in self._passives
