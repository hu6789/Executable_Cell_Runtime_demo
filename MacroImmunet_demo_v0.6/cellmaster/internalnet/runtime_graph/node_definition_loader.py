# cellmaster/internalnet/runtime_graph/node_definition_loader.py

import json
from pathlib import Path


class NodeDefinitionLoader:

    BASE_DIRS = [

        Path(
            "cellmaster/internalnet/node"
        ),

        Path(
            "aip/viral_node"
        )
    ]

    def load(
        self,
        node_name
    ):

        for base_dir in self.BASE_DIRS:

            path = (
                base_dir
                / f"{node_name}.json"
            )

            if not path.exists():
                continue

            with open(path, "r") as f:

                data = json.load(f)

            data["node_id"] = node_name

            data.setdefault(
                "node_name",
                node_name
            )

            return data

        raise FileNotFoundError(

            f"node definition not found: "
            f"{node_name}"
        )
