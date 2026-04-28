import itertools


class ScanMaster:

    def __init__(self, world, event_lib):
        self.world = world
        self.event_lib = event_lib
        self.event_defs = {e["type"]: e for e in event_lib}
        self._event_counter = itertools.count()

    # =========================
    # 主入口
    # =========================
    def scan(self, tick=0):
        events = []
        for cell in self.world.cells.values():
            pos = tuple(cell.position)
            events.extend(self._scan_fields(cell, pos, tick))
            events.extend(self._scan_contacts(cell, pos, tick))
            events.extend(self._scan_context(cell, pos, tick))
        return events

    # =========================
    # 事件构造（统一出口）
    # =========================
    def _make_event(self, etype, source, target, payload, pos, tick, dist=None):
        self._validate_payload(etype, payload)
        eid = f"{etype}_{tick}_{next(self._event_counter)}"
        return {
            "event_id": eid,
            "event_type": etype,
            "source": source,
            "target": target,
            "payload": payload,
            "meta": {
                "position": pos,
                "distance": dist,
                "tick": tick
            }
        }

    # =========================
    # 事件匹配规则
    # =========================
    def _match_event_rule(self, etype, source, target):
        """返回 True/False，检查 source/target 是否符合 event_lib 定义"""
        if etype not in self.event_defs:
            return False
        rule = self.event_defs[etype]

        # 检查 source_type
        if "source_type" in rule:
            if source["type"] != rule["source_type"]:
                return False

        # 检查 target_type
        if "target_type" in rule:
            if target.get("type") != rule["target_type"]:
                return False

        # 可扩展： receptor/field/其他条件
        if "target_receptor" in rule:
            if not getattr(self.world.cells[target["id"]], "receptors", {}).get(rule["target_receptor"], False):
                return False

        return True

    # =========================
    # 1️⃣ field signal
    # =========================
    def _scan_fields(self, cell, pos, tick):
        events = []
        for fname, grid in self.world.fields.items():
            val = grid.get(pos, 0.0)
            if val <= 0:
                continue

            source = {"type": "field", "id": fname}
            target = {"type": "cell", "id": cell.cell_id, "type": cell.cell_type}

            # 匹配 event_lib
            if not self._match_event_rule("signal", source, target):
                continue

            payload = {
                "field": fname,
                "value": val,
                "target_id": cell.cell_id
            }

            ev = self._make_event(
                etype="signal",
                source=source,
                target=target,
                payload=payload,
                pos=pos,
                tick=tick
            )
            events.append(ev)
        return events

    # =========================
    # 2️⃣ cell contact
    # =========================
    def _scan_contacts(self, cell, pos, tick):
        events = []
        neighbors = self.world.get_neighbors(cell)
        for nb in neighbors:
            nb_pos = tuple(nb.position)
            dist = self._distance(pos, nb_pos)

            source = {"type": "cell", "id": nb.cell_id, "type": nb.cell_type}
            target = {"type": "cell", "id": cell.cell_id, "type": cell.cell_type}

            if not self._match_event_rule("contact", source, target):
                continue

            payload = {
                "target_type": nb.cell_type,
                "distance": dist
            }

            ev = self._make_event(
                etype="contact",
                source=source,
                target=target,
                payload=payload,
                pos=pos,
                tick=tick,
                dist=dist
            )
            events.append(ev)
        return events

    # =========================
    # 3️⃣ context（hotspot等）
    # =========================
    def _scan_context(self, cell, pos, tick):
        events = []
        for fname, grid in self.world.fields.items():
            cfg = self.world.field_defs.get(fname, {})
            threshold = cfg.get("hotspot_threshold")
            if threshold is None:
                continue
            val = grid.get(pos, 0.0)
            if val >= threshold:
                source = {"type": "field", "id": fname}
                target = {"type": "cell", "id": cell.cell_id, "type": cell.cell_type}

                if not self._match_event_rule("context", source, target):
                    continue

                payload = {"tag": f"{fname}_hotspot"}

                ev = self._make_event(
                    etype="context",
                    source=source,
                    target=target,
                    payload=payload,
                    pos=pos,
                    tick=tick
                )
                events.append(ev)
        return events

    # =========================
    # payload 校验
    # =========================
    def _validate_payload(self, etype, payload):
        if etype not in self.event_defs:
            raise ValueError(f"Unknown event type: {etype}")
        schema = self.event_defs[etype].get("payload_schema", {})
        for key in schema:
            if key not in payload:
                raise ValueError(f"{etype} missing field: {key}")

    # =========================
    # 工具函数
    # =========================
    def _distance(self, p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5
