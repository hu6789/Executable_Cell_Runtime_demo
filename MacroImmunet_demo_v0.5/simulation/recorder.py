# simulation/recorder.py

import json
import os


class Recorder:

    def __init__(self):
        self.timeline = []
        self.last_cells = {}

    def record(self, frame):

        frame = self._sanitize(frame)

        current_cells = frame.get("cells", {})

        # 标 alive
        for cid, cell in current_cells.items():
            cell["status"] = "alive"

        # 标 dead（消失的）
        dead_cells = {}
        for cid, old in self.last_cells.items():
            if cid not in current_cells:
                dead = old.copy()
                dead["status"] = "dead"
                dead_cells[cid] = dead

        merged = {**current_cells, **dead_cells}
        frame["cells"] = merged

        self.last_cells = merged
        self.timeline.append(frame)

    def export(self, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(self.timeline, f, indent=2)

    def _sanitize(self, obj):

        if isinstance(obj, dict):
            return {
                str(k): self._sanitize(v)
                for k, v in obj.items()
            }

        if isinstance(obj, list):
            return [self._sanitize(i) for i in obj]

        return obj
