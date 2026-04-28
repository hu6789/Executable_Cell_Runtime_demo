# cellmaster/cell/cell_factory.py
#cell.meta["execution_profile"] = template.get("execution_profile", {})
#cell.meta["spatial"] = template.get("spatial", {})

import json
import os
import random
import numpy as np
from .cell_instance import Cell

from .cell_instance import Cell
import random

class CellFactory:

    def __init__(self):
        self._id_counter = 0

    def _generate_id(self):
        self._id_counter += 1
        return self._id_counter

    def create_cell(self, name, position):

        # ✅ 1. load template
        template = self.load_template(name)

        # ✅ 2. create cell
        cid = self._generate_id()
        cell = Cell(cid, template["cell_type"], position)

        # node state
        cell.node_state = self._init_node_state(
            template.get("init_node_state", {})
        )

        # params
        cell.params["feature"] = template.get("params", {}).get("feature", {}).copy()
        cell.params["node"] = template.get("params", {}).get("node", {}).copy()
        cell.params["behavior"] = template.get("params", {}).get("behavior", {}).copy()

        # flags
        cell.state_flags = template.get("state_flags", {"alive": True}).copy()

        # subtype
        self._apply_subtype(cell, template)

        return cell
    def _init_node_state(self, config):
        state = {}

        for node, spec in config.items():
  
            if isinstance(spec, dict) and "mean" in spec:
                state[node] = self._sample_param(spec)
            else:
                state[node] = spec
        for k in ["ATP", "stress", "damage"]:
            state.setdefault(k, 0.0)
        return state
    def _sample_param(self, spec):
        """
        支持：
        - {"mean": x, "std": y}
        - 可选 min / max 截断
        """

        mean = spec.get("mean", 0.0)
        std = spec.get("std", 0.0)

        # 1️⃣ 采样
        if std > 0:
            val = random.gauss(mean, std)
        else:
            val = mean

        # 2️⃣ 截断（可选）
        if "min" in spec:
            val = max(spec["min"], val)
        if "max" in spec:
            val = min(spec["max"], val)

        return val
    def _apply_subtype(self, cell, template):

        subtypes = template.get("subtypes", {})

        if not subtypes:
            cell.meta["subtype"] = None
            return

        import random
        name = random.choice(list(subtypes.keys()))
        subtype = subtypes[name]

        # feature
        for k, spec in subtype.get("hir_params", {}).items():
            cell.params["feature"][k] = self._sample_param(spec)

        # node
        for k, v in subtype.get("node_params", {}).items():
            cell.params["node"][k] = v

        # behavior
        for k, v in subtype.get("behavior_params", {}).items():
            cell.params["behavior"][k] = v

        cell.meta["subtype"] = name
    def load_template(self, name):
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "cell", f"{name}.json")

        with open(path) as f:
            return json.load(f)
