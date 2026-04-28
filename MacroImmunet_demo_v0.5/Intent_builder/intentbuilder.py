# Cell_master/IntentBuilder/intentbuilder.py

import itertools

class IntentBuilder:

    def __init__(self):
        self._counter = itertools.count()

    # =========================
    # 🚪 主入口（统一入口！！！）
    # =========================
    def build(
        self,
        cell_outputs=None,        # dict: cell_id -> internalnet result
        substance_actions=None,   # list of actions
        tick=0
    ):
        intents = []

        # -------------------------
        # 1️⃣ CellMaster → intents
        # -------------------------
        if cell_outputs:
            for cell_id, out in cell_outputs.items():

                behaviors = out.get("behaviors", [])
                state_delta = out.get("state_delta", {})
                hir_output = out.get("hir", {})

                intents += self._from_behaviors(cell_id, behaviors, tick)
                intents += self._from_state(cell_id, state_delta, tick)
                intents += self._from_fate(cell_id, hir_output, tick)

        # -------------------------
        # 2️⃣ SubstanceMaster → intents ⭐
        # -------------------------
        if substance_actions:
            intents += self._from_substance(substance_actions, tick)

        return intents

    # =========================
    # 🧩 behavior → intent
    # =========================
    def _from_behaviors(self, cell_id, behaviors, tick):

        intents = []

        for b in behaviors:

            for out in b.get("outputs", []):

                if out.get("type") != "intent":
                    continue

                val = out.get("value", 1.0)

                intent = self._make_intent(
                    itype="add_field",
                    source=cell_id,
                    target=None,
                    payload={
                        "field": out.get("field"),
                        "value": val
                    },
                    tick=tick
                )

                intents.append(intent)

        return intents

    # =========================
    # 🧬 state update
    # =========================
    def _from_state(self, cell_id, state_delta, tick):

        intents = []

        for node, val in state_delta.items():

            intents.append(
                self._make_intent(
                    itype="cell_state",
                    source=cell_id,
                    target=cell_id,
                    payload={
                        "node": node,
                        "op": "add",
                        "delta": val
                    },
                    tick=tick
                )
            )

        return intents

    # =========================
    # ☠️ fate
    # =========================
    def _from_fate(self, cell_id, hir_output, tick):

        intents = []

        if hir_output.get("fate") == "dying":

            intents.append(
                self._make_intent(
                    itype="death",
                    source=cell_id,
                    target=cell_id,
                    payload={"kind": "default"},
                    tick=tick
                )
            )

        return intents

    # =========================
    # 💥 SubstanceMaster → intent（🔥核心新增）
    # =========================
    def _from_substance(self, actions, tick):

        intents = []

        for act in actions:

            # 🔥 新架构：SubstanceMaster 已经生成的是 intent request
            if act.get("type") == "intent":
                intents.append(act)
                continue

            # 🔥 fallback（兼容旧数据，可选保留）
            if act.get("type") == "effect":

                intents.append(
                    self._make_intent(
                        itype="effect",
                        source=act.get("source"),
                        target=act.get("target_id"),
                        payload={
                            "kind": act.get("kind"),
                            "value": act.get("value")
                        },
                        tick=tick
                    )
                )

        return intents
    def build_intents(behavior_outputs, cell):

        intents = []

        for b in behavior_outputs:

            for emit in b.get("emit", []):

                if emit["type"] == "direct_effect":

                    effect_name = emit["effect"]
                    cfg = DIRECT_EFFECT_MAP.get(effect_name)

                    if not cfg:
                        continue

                    target_id = resolve_target(cell, emit["target"])

                    intents.append({
                        "type": "effect",
                        "source": cell.cell_id,
                        "target": target_id,
                        "payload": {
                            "kind": cfg["kind"],
                            "value": cfg.get("scale", 1.0)
                        }
                    })

        return intents
    # =========================
    # 🏗 构造器
    # =========================
    def _make_intent(self, itype, source, target, payload, tick):

        iid = f"{itype}_{tick}_{next(self._counter)}"

        return {
            "intent_id": iid,
            "type": itype,
            "source": source,
            "target": target,
            "payload": payload,
            "meta": {
                "tick": tick
            }
        }
