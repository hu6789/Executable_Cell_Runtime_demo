# simulation/simulation_runner.py

import json
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
from scan_master.scan_master import ScanMaster
from scan_master.event_loader import load_event_lib

from Input_builder.inputbuilder import InputBuilder
from Substance.substance_master import SubstanceMaster
from Intent_builder.intentbuilder import IntentBuilder
from Label_center.labelcenter import LabelCenter
from Cell_master.cell_instance.cell_factory import CellFactory
from Cell_master.Internalnet.cellmaster_engine import InternalNet
from Cell_master.Internalnet.node_engine import load_nodes

from World.world import World
from World.Registry_library import REGISTRY

from simulation.recorder import Recorder

from simulation.frame_builder import build_frame


# =========================
# 🔹 scenario loader
# =========================
def load_scenario(path):
    with open(path) as f:
        return json.load(f)


# 🔥 放在文件最上面（class 外面）
def extract_events_from_intents(intents, tick):

    events = []

    for it in intents:
        t = it.get("type")

        if t == "effect":
            payload = it.get("payload", {})
            node = payload.get("node")
            delta = payload.get("delta", payload.get("value", 0))

            if node == "damage":
                events.append(f"🔥 {it['target']} damage +{delta:.2f}")

            elif node == "stress":
                events.append(f"⚠ {it['target']} stress spike")

        elif t == "cell_state":
            events.append(f"🔶 {it['target']} state change")

        elif t == "add_field":
            events.append(f"🌊 {it['source']} → {it['payload'].get('field')}")

        elif t == "death":
            events.append(f"☠ {it['target']} died")

    return {
        "tick": tick,
        "lines": events
    }
# =========================
# 🔹 world 初始化
# =========================
def init_world(scn):

    world = World(
        width=scn["world"]["width"],
        height=scn["world"]["height"]
    )

    factory = CellFactory()

    # 🔹 cells
    for c in scn["cells"]:

        name = c["type"]   # 👈 对应 template 文件名
        pos = tuple(c["pos"])

        cell = factory.create_cell(name, pos)

        # 👉 scenario override（可选）
        if c.get("infected"):
            cell.state_flags["infected"] = True

        world.add_cell(cell)

    # 🔹 fields
    for f in scn.get("fields", []):
        fname, x, y, val = f

        world.fields.setdefault(fname, {})
        world.fields[fname][(x, y)] = val

    return world
# =========================
# 🔹 主运行
# =========================
def run_simulation(scenario_path, output_path):

    scn = load_scenario(scenario_path)

    world = init_world(scn)

    # 🔹 modules
    event_lib = load_event_lib("scan_master/event_lib")

    scan = ScanMaster(world, event_lib)

    node_defs = {n["node_id"]: n for n in load_nodes()}
    input_builder = InputBuilder(node_defs, REGISTRY)

    substance_master = SubstanceMaster(world, world.field_defs)
    net = InternalNet(behaviors=None)
    intent_builder = IntentBuilder()
    label = LabelCenter()

    recorder = Recorder()

    steps = scn.get("steps", 20)
    
    event_log = []

    # =========================
    # 🔁 LOOP
    # =========================
    for tick in range(steps):

        print(f"\n===== TICK {tick} =====")
        
        state_snapshot = {cid: dict(cell.node_state) for cid, cell in world.cells.items()}
        
        world.step()

        # 1️⃣ scan
        events = scan.scan(tick=tick)

        for e in events:
            print("[SCAN EVENT]", e)
        # 2️⃣ input
        ib_out = input_builder.build(events, cells=world.cells, world=world)

        cell_inputs = ib_out["cell"]

        # 3️⃣ substance
        substance_actions = substance_master.step(ib_out["substance"])

        # 4️⃣ cell
        cell_outputs = net.step_cells(world, cell_inputs, state_snapshot=state_snapshot)

        # 5️⃣ intent
        intents = intent_builder.build(
            cell_outputs=cell_outputs,
            substance_actions=substance_actions,
            tick=tick
        )
        for it in intents:
            print("[INTENT]", it)

        events = extract_events_from_intents(intents, tick)
        event_log.append(events)

        # 6️⃣ apply
        label.collect(intents)

        print("[BEFORE APPLY] world cells:", list(world.cells.keys()))

        label.apply(world, tick)

        print("[AFTER APPLY] world cells:", list(world.cells.keys()))

        # 7️⃣ record ⭐
        frame = build_frame(
            world,
            cell_outputs,
            events,
            intents,
            tick
        )

        recorder.record(frame)

        if not world.cells:
            print("[END] all cells removed")
            break

    # =========================
    # 💾 export
    # =========================
    recorder.export(output_path)

    print(f"\n✅ saved to: {output_path}")


# =========================
# CLI
# =========================
if __name__ == "__main__":

    import sys

    if len(sys.argv) >= 2:
        scenario = sys.argv[1]
    else:
        scenario = "scenarios/cd8_kill_chain.json"

    if len(sys.argv) >= 3:
        output = sys.argv[2]
    else:
        name = os.path.splitext(os.path.basename(scenario))[0]
        output = f"visualization/outputs/{name}.timeline.json"

    run_simulation(scenario, output)
