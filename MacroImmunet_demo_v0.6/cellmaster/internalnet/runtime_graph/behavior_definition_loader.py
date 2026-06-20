# cellmaster/internalnet/runtime_graph/behavior_definition_loader.py

import json
from pathlib import Path


class BehaviorDefinitionLoader:

    BASE_DIR = Path(
        "cellmaster/internalnet/behavior"
    )

    def load(
        self,
        behavior_name
    ):

        path = (
            self.BASE_DIR
            / f"{behavior_name}.json"
        )

        with open(path, "r") as f:

            data = json.load(f)

        data.setdefault(
            "behavior_name",
            behavior_name
        )

        data.setdefault(
            "behavior_id",
            behavior_name
        )

        return data
