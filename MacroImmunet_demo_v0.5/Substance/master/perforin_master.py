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

        for it in interactions:

            target_id = it.get("target_id")
            if target_id is None:
                continue

            cell = self.world.cells.get(target_id)
            if not cell:
                continue

            # =========================
            # 1️⃣ infected 判定（🔥关键就在这里）
            # =========================
            if not cell.state_flags.get("infected", False):
                continue

            # =========================
            # 2️⃣ 数值转换
            # =========================
            value = it.get("value", 0.0)

            scale = self.conversion.get("scale", 1.0)
            value *= scale

            threshold = self.conversion.get("threshold")
            if threshold is not None and abs(value) < threshold:
                continue

            # =========================
            # 3️⃣ 直接生成 intent（🔥核心）
            # =========================
            intents.append({
                "type": "cell_state",
                "source": "perforin",
                "target": target_id,
                "payload": {
                    "node": "membrane",
                    "op": "add",
                    "delta": -abs(value)   # 🔴 perforin = 减 membrane
                }
            })

        return intents
