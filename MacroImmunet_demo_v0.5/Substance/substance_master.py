# Substance/master/substance_master.py

from Substance.master.perforin_master import PerforinMaster


class SubstanceMaster:

    def __init__(self, world, field_defs):
        self.world = world
        self.field_defs = field_defs

        self.masters = {
            "perforin": PerforinMaster(world, field_defs),
        }

    # =========================
    # 主入口
    # =========================
    def step(self, substance_outputs):

        intents = []

        # 按 substance 分组
        grouped = {}
        for it in substance_outputs:
            kind = it.get("substance")   # 🔥 新结构：用 substance
            if not kind:
                continue
            grouped.setdefault(kind, []).append(it)

        # 分发给对应 master
        for kind, its in grouped.items():

            master = self.masters.get(kind)

            if master:
                intents += master.step(its)

            else:
                # 没有 master → 忽略（或以后扩展）
                continue

        return intents
