# cellmaster/internalnet/passive_engine/passive_loader.py

import json
from pathlib import Path


class PassiveLoader:

    """
    passive definition loader

    responsibilities:
        - load passive definitions
        - merge cell passive + viral passive
        - provide runtime passive registry

    DOES NOT:
        - execute passives
        - evaluate formulas
        - modify runtime state
    """

    def load_all_passives(self):

        result = []

        result.extend(
            self._load_directory(
                "cellmaster/internalnet/passive"
            )
        )

        result.extend(
            self._load_directory(
                "aip/viral_passive"
            )
        )

        return result

    def _load_directory(self, path):

        loaded = []

        directory = Path(path)

        if not directory.exists():
            return loaded

        for file in sorted(
            directory.glob("*.json")
        ):

            with open(file, "r") as f:

                loaded.append(
                    json.load(f)
                )

        return loaded
