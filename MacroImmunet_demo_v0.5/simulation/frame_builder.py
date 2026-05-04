# simulation/frame_builder.py

# =========================
# 🔹 main frame builder
# =========================
def build_frame(world, cell_outputs, events, intents, tick):

    # 🔥 转换为“可视化语义事件”
    visual_events = convert_events(events, intents)

    frame = {
        "tick": tick,
        "cells": {},
        "fields": serialize_fields(world.fields),  # ⭐ 建议序列化
        "events": convert_events(events, intents),
        "intent_log": list(intents)
    }

    for cid, cell in world.cells.items():

        # 🔥 优先用输出（如果没有就 fallback）
        output = cell_outputs.get(cid, {})

        node_state = output.get("node", cell.node_state)
        behaviors = output.get("behaviors", [])
        fate = output.get("fate", cell.hir_state.get("fate", "normal"))

        frame["cells"][str(cid)] = {
            "type": cell.cell_type,
            "pos": cell.position,
            "node": node_state,
            "behaviors": behaviors,
            "fate": fate,
            "intents": intents,
            "status": "alive" if cell.flags.get("alive", True) else "dead"
        }

    return frame


# =========================
# 🔹 fields 序列化
# =========================
def serialize_fields(fields):

    out = {}

    for fname, grid in fields.items():
        out[fname] = {
            str(pos): val
            for pos, val in grid.items()
        }

    return out


# =========================
# 🔹 Intent → 可视化事件
# =========================
def convert_events(events, intents):

    visual_events = []

    # =========================
    # 🔴 1️⃣ intents → 真实行为
    # =========================
    for it in intents:

        # 🩸 membrane damage
        if it.get("type") == "cell_state":
            payload = it.get("payload", {})

            if payload.get("node") == "membrane":
                delta = payload.get("delta", 0)

                if delta < 0:
                    visual_events.append({
                        "type": "damage_cell",
                        "target": it.get("target"),
                        "value": abs(delta),
                        "source": it.get("source", "?")
                    })

        # ☠ death
        elif it.get("type") == "death":
            visual_events.append({
                "type": "cell_die",
                "target": it.get("target")
            })

        # 🟣 signal（非常重要）
        elif it.get("type") == "field":
            visual_events.append({
                "type": "signal",
                "field": it.get("field"),
                "target": it.get("target"),
                "value": it.get("value")
            })

    # =========================
    # 🟡 可选：scan events fallback
    # =========================
    # 👉 防止你某些机制还没intent化
    for eg in events:
        if not isinstance(eg, dict):
            continue

        for e in eg.get("events", []):
            if not isinstance(e, dict):
                continue

            # 👉 给没有type的补type（避免崩）
            if "type" not in e:
                e["type"] = "raw"

            visual_events.append(e)

    return visual_events
