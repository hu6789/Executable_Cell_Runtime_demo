# Substance/master/perforin_master.py

class PerforinMaster:

    def __init__(self, world, field_defs):
        self.world = world

        cfg = field_defs.get("perforin", {})
        self.interaction = cfg.get("interaction", {})
        self.conversion = self.interaction.get("conversion", {})

    # =========================
    # 主逻辑
    # =========================
    def step(self, interactions):

        intents = []

        acc = {}   # 🔴 每个 cell 累积

        for it in interactions:

            target_id = it.get("target_id")
            if target_id is None:
                continue

            cell = self.world.cells.get(target_id)
            if not cell:
                continue

            if not cell.state_flags.get("infected", False):
                continue

            value = it.get("value", 0.0)

            scale = self.conversion.get("scale", 1.0)
            value *= scale

            threshold = self.conversion.get("threshold")
            if threshold is not None and abs(value) < threshold:
                continue

            acc[target_id] = acc.get(target_id, 0.0) + abs(value)

        # 🔥 clamp（关键）
        max_damage = 0.15

        for cid, total in acc.items():

            dmg = min(total, max_damage)
 
            intents.append({
                "type": "effect",
                "source": "perforin",
                "target": cid,
                "payload": {
                    "node": "membrane",
                    "op": "add",
                    "delta": -dmg
                }
            })

        return intents
