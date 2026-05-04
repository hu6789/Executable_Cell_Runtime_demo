from collections import Counter

from World.world import World
from Label_center.labelcenter import LabelCenter
from Intent_builder.intentbuilder import IntentBuilder

from Cell_master.cell_instance.cell_factory import CellFactory
from Cell_master.Internalnet.cellmaster_engine import InternalNet
from Input_builder.inputbuilder import InputBuilder
from Cell_master.Internalnet.node_engine import load_nodes


# ===== DEBUG 开关 =====
DEBUG_VERBOSE = False


# ===== 初始化 =====
world = World()
label = LabelCenter()
builder = IntentBuilder()

factory = CellFactory()
net = InternalNet(behaviors=None)

node_defs = {n["node_id"]: n for n in load_nodes()}
input_builder = InputBuilder(node_defs=node_defs)


# ===== 创建多种 cell =====
cells = []

# CD4 cluster
for i in range(5):
    cells.append(factory.create_cell("cd4_t", (10 + i, 10)))

# CD8 cluster
for i in range(5):
    cells.append(factory.create_cell("cd8_t", (10 + i, 11)))

# host cells
for i in range(5):
    cells.append(factory.create_cell("host_cell", (10 + i, 12)))

for c in cells:
    world.add_cell(c)


# ===== world field =====
world.fields = {
    "IL2": {
        (10, 10): 1.0,
        (11, 10): 1.0,
        (12, 10): 1.0
    }
}


# ===== TICK LOOP =====
for tick in range(3):

    print(f"\n================ TICK {tick} ================")

    # =========================
    # 1️⃣ scan events
    # =========================
    events = []

    for c in cells:
        pos = c.position

        il2_val = world.fields.get("IL2", {}).get(pos, 0.0)

        events.extend([
            {
                "event_type": "field_signal",
                "target": {"id": c.cell_id},
                "payload": {
                    "field": "IL2_field",
                    "value": il2_val
                }
            },
            {
                "event_type": "contact",
                "target": {"id": c.cell_id},
                "payload": {
                    "signals": {
                        "pMHC_external": 1.0
                    }
                }
            }
        ])

    # =========================
    # 2️⃣ input builder
    # =========================
    node_inputs = input_builder.build(events, cells=world.cells)

    # =========================
    # 3️⃣ internal net
    # =========================
    for c in cells:

        result = net.step(
            c,
            node_inputs.get(c.cell_id, {}).get("node_input", {})
        )

        behaviors = result.get("behaviors", [])
        state_delta = result.get("state_delta", {})

        # 👉 记录行为（给 summary 用）
        c.last_behaviors = behaviors

        # ===== 可选详细打印 =====
        if DEBUG_VERBOSE:
            print(f"\n--- CELL {c.cell_type} (id={c.cell_id}) ---")
            print("[STATE DELTA]", state_delta)
            print("[BEHAVIORS]")
            for b in behaviors:
                print(" ", b["behavior_id"])

        # =========================
        # 4️⃣ intent builder
        # =========================
        intents = builder.build(
            cell_id=c.cell_id,
            behavior_outputs=behaviors,
            state_update=state_delta,
            hir_output=result.get("hir", {}),
            tick=tick
        )

        for i in intents:
            label.collect([i])

    # =========================
    # 5️⃣ apply
    # =========================
    label.apply(world)

    # =========================
    # 6️⃣ 🔥 SYSTEM SUMMARY（核心）
    # =========================

    # ===== 行为统计 =====
    behavior_counter = Counter()
    for c in cells:
        for b in getattr(c, "last_behaviors", []):
            behavior_counter[b["behavior_id"]] += 1

    # ===== 平均状态 =====
    def avg(key):
        return sum(c.node_state.get(key, 0) for c in cells) / len(cells)

    # ===== field 总量 =====
    def field_sum(field_name):
        return sum(world.fields.get(field_name, {}).values())

    print("\n===== SUMMARY =====")

    print("[BEHAVIOR COUNT]", dict(behavior_counter))

    print("[AVG STATE]",
          "ATP:", round(avg("ATP"), 3),
          "stress:", round(avg("stress"), 3),
          "IL2_signal:", round(avg("IL2_signal"), 3),
          "viral_load:", round(avg("viral_load"), 3))

    print("[FIELD TOTAL]",
          "IL2:", round(field_sum("IL2"), 3))

    # ===== 系统阶段判断 =====
    if not behavior_counter:
        phase = "💀 inactive"
    elif behavior_counter.get("release_IL2", 0) > 0:
        phase = "🔥 activating"
    elif avg("IL2_signal") < 0.2:
        phase = "❄️ decaying"
    else:
        phase = "⚖️ steady"

    print("[SYSTEM PHASE]", phase)

    # =========================
    # （可选）详细 world 输出
    # =========================
    if DEBUG_VERBOSE:
        print("\n[WORLD FIELDS]", world.fields)

        print("\n[IL2 MAP]")
        for pos, val in sorted(world.fields.get("IL2", {}).items()):
            print(pos, round(val, 3))

        for c in cells:
            print(f"[CELL {c.cell_type} STATE]", c.node_state)
