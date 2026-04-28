from World.Registry_library import REGISTRY
class InputBuilder:

    def __init__(self, node_defs, registry, asi=None):
        self.node_defs = node_defs
        self.registry = registry
        self.asi = asi

    def build(self, events, cells=None, world=None):

        perception_map = self._dispatch_events(events)

        cell_outputs = {}
        substance_outputs = []

        for tid, perception in perception_map.items():

            cell = cells.get(tid) if cells else None
            node_input = {}

            for ev in perception.get("events", []):

                payload = ev.get("payload", {})
                field = payload.get("field")
                val = payload.get("value", 0.0)

                if not field:
                    continue

                cfg = self.registry.get(field)
                if not cfg:
                    continue

                interaction = cfg.get("interaction", {})
                itype = interaction.get("type")

                # =========================
                # signal → cell
                # =========================
                if itype == "signal":

                    node_id = cfg.get("translation", {}).get("node")
                    if not node_id:
                        continue

                    processed = self._apply_receptor(node_id, val)
                    node_input[node_id] = node_input.get(node_id, 0.0) + processed

                # =========================
                # binding → cell
                # =========================
                elif itype == "binding":

                    node_id = cfg.get("translation", {}).get("node")
                    if not node_id:
                        continue

                    node_input[node_id] = node_input.get(node_id, 0.0) + val

                # =========================
                # effector → substance master
                # =========================
                elif itype == "effector":

                    # target filter（关键！）
                    if cell:
                        allowed = interaction.get("target_filter")
                        if allowed and not any(cell.state_flags.get(f, False) for f in allowed):
                            continue

                    substance_outputs.append({
                        "type": "substance",
                        "substance": field,
                        "target_id": cell.cell_id if cell else None,
                        "value": val,
                        "meta": ev.get("meta", {})
                    })

            # -------------------------
            # ASI
            # -------------------------
            if self.asi:
                node_input = self.asi.apply(node_input, perception)

            if node_input:
                cell_outputs[tid] = {
                    "type": "cell",
                    "node_input": node_input,
                    "status": "delivered"
                }

        return {
            "cell": cell_outputs,
            "substance": substance_outputs
        }

    def _apply_receptor(self, node_id, raw_value):

        node_def = self.node_defs.get(node_id, {})
        receptor = node_def.get("receptor")

        if not receptor:
            return raw_value

        t = receptor.get("type")

        if t == "sigmoid":
            import math
            s = receptor.get("sensitivity", 1.0)
            th = receptor.get("threshold", 0.0)
            k = receptor.get("slope", 1.0)
            return (1 / (1 + math.exp(-k * (raw_value - th)))) * s

        elif t == "binding":
            affinity = receptor.get("affinity", 1.0)
            max_act = receptor.get("max_activation", 1.0)
            return min(raw_value * affinity, max_act)

        return raw_value

    def _dispatch_events(self, events):

        perception_map = {}

        for ev in events:
            target = ev.get("target", {})
            tid = target.get("id")

            if tid is None:
                continue

            perception_map.setdefault(tid, {"events": []})
            perception_map[tid]["events"].append(ev)

        return perception_map
