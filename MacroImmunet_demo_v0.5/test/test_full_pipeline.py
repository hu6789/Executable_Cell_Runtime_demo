from World.world import World
from Label_center.labelcenter import LabelCenter
from Intent_builder.intentbuilder import IntentBuilder

from Cell_master.cell_instance.cell_factory import CellFactory
from Cell_master.Internalnet.cellmaster_engine import InternalNet
from Input_builder.inputbuilder import InputBuilder
from Cell_master.Internalnet.node_engine import load_nodes

# ===== 初始化 =====
world = World()
label = LabelCenter()
builder = IntentBuilder()

factory = CellFactory()
net = InternalNet(behaviors=None)

node_defs = {n["node_id"]: n for n in load_nodes()}
input_builder = InputBuilder(node_defs=node_defs)

# ===== 创建 cell =====
cell = factory.create_cell("cd8_t", (10, 10))
world.add_cell(cell)

# ===== 模拟 world field =====
world.fields = {
    "IL2": {(10, 10): 1.0}
}

# ===== TICK =====
for tick in range(3):

    print(f"\n===== TICK {tick} =====")

    # =========================
    # 1️⃣ scan（简化版）
    # =========================
    events = [
        {
            "event_type": "field_signal",
            "target": {"id": cell.cell_id},
            "payload": {
                "field": "IL2_field",
                "value": 1.0
            }
        },
        {
            "event_type": "contact",
            "target": {"id": cell.cell_id},
            "payload": {
                "signals": {
                    "pMHC_external": 1.0
                }
            }
        }
    ]

    # =========================
    # 2️⃣ input builder
    # =========================
    node_input_map = input_builder.build(events)
    node_input = node_input_map.get(cell.cell_id, {}).get("node_input", {})

    print("[INPUT]", node_input)

    # =========================
    # 3️⃣ internal net
    # =========================
    node_inputs = input_builder.build(events, cells=world.cells)

    result = net.step(
        cell,
        node_inputs.get(cell.cell_id, {}).get("node_input", {})
    )

    behaviors = result.get("behaviors", [])
    hir = result.get("hir", {})
    state_delta = result.get("state_delta", {})  # ⚠️你需要让 net 输出这个

    print("[STATE DELTA]", state_delta)
    print("[RAW BEHAVIOR OUTPUT]", behaviors)
    print("[BEHAVIORS]", behaviors)

    # =========================
    # 4️⃣ intent builder
    # =========================
    intents = builder.build(
        cell_id=cell.cell_id,
        behavior_outputs=behaviors,
        state_update=state_delta,
        hir_output=hir,
        tick=tick
    )

    print("[INTENTS]")
    for i in intents:
        print(i)

    # =========================
    # 5️⃣ label center apply
    # =========================
    label.collect(intents)
    label.apply(world)

    print("[WORLD FIELDS]", world.fields)
    print("[CELL STATE]", world.cells[cell.cell_id].node_state)
