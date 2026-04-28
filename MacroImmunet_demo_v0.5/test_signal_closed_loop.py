# test_signal_closed_loop.py

from scan_master.scan_master import ScanMaster

from Input_builder.inputbuilder import InputBuilder

from Substance.substance_master import SubstanceMaster
from Intent_builder.intentbuilder import IntentBuilder

from Label_center.labelcenter import LabelCenter

from Cell_master.Internalnet.cellmaster_engine import InternalNet
from Cell_master.Internalnet.node_engine import load_nodes
from scan_master.event_loader import load_event_lib
from World.Registry_library import REGISTRY

# =========================
# mock Cell / World
# =========================
class Cell:
    def __init__(self, cid, cell_type):
        self.cell_id = cid
        self.cell_type = cell_type
        self.position = (0, 0)

        if cell_type == "cd4_t":
            self.node_state = {
                "ATP": 1.0,
                "stress": 0.0,
                "IL2_signal": 0.0
            }

        elif cell_type == "cd8_t":
            self.node_state = {
                "ATP": 1.0,
                "stress": 0.0,
                "IL2_signal": 0.0,
                "TCR_signal": 3.0   # mock antigen
            }

        elif cell_type == "target":
            self.node_state = {
                "membrane": 1.0,
                "stress": 0.0
            }

        self.state_flags = {"infected": cell_type == "target"}

        self.params = {"behavior": {}}

class World:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.fields = {
            "IL2": {(0, 0): 2.0},
            "perforin": {(0, 0): 1.0}
        }

        self.field_defs = {
            "IL2": {
                "type": "signal",
                "interaction": {
                    "kind": "signal",
                    "conversion": {"scale": 1.0}
                }
            },
            "perforin": {
                "interaction": {
                    "kind": "effector",
                    "conversion": {
                        "scale": 1.0
                    },
                    "filter": {
                        "cell_flags": ["infected"]
                    }
                }
            }
        }

        self.cells = {
            1: Cell(1, "cd4_t"),
            2: Cell(2, "cd8_t"),
            3: Cell(3, "target")
        }

    def get_neighbors(self, cell):
        return []


# =========================
# TEST
# =========================
def test_closed_loop():

    print("\n===== SIGNAL CLOSED LOOP TEST =====")

    world = World()

    event_lib = load_event_lib("scan_master/event_lib")

    scan = ScanMaster(world, event_lib=event_lib)
    
    node_defs = {n["node_id"]: n for n in load_nodes()}
    input_builder = InputBuilder(node_defs, REGISTRY)
    substance_master = SubstanceMaster(world, world.field_defs)
    net = InternalNet(behaviors=None)
    intent_builder = IntentBuilder()
    label = LabelCenter()

    for tick in range(3):

        print(f"\n--- TICK {tick} ---")

        # 1️⃣ scan
        events = scan.scan(tick=tick)
        
        # 2️⃣ InputBuilder（统一翻译）
        ib_out = input_builder.build(events, cells=world.cells, world=world)

        cell_inputs = ib_out["cell"]
        substance_inputs = ib_out["substance"]
        print("SUBSTANCE INPUT:", substance_inputs)
        # 3️⃣ SubstanceMaster（直接吃 events）
        substance_actions = substance_master.step(substance_inputs)
        print("SUBSTANCE:", substance_inputs)
        print("ACTIONS:", substance_actions)

        # 4️⃣ CellMaster（InternalNet）
        cell_outputs = {}

        for cid, cell in world.cells.items():

            node_input = cell_inputs.get(cid, {}).get("node_input", {})

            result = net.step(cell, node_input)

            cell_outputs[cid] = result
        print(result.get("behaviors"))
        print("BEHAVIOR RAW:", result.get("behaviors"))
        
        # 5️⃣ IntentBuilder（🔥统一入口）
        intents = intent_builder.build(
            cell_outputs=cell_outputs,
            substance_actions=substance_actions,
            tick=tick
        )
        print("\n[INTENTS]")
        for it in intents:
            print(it)
        # 6️⃣ apply
        label.collect(intents)
        label.apply(world)

        print("FIELD IL2:", world.fields.get("IL2"))
        for cid, cell in world.cells.items():
            print(f"CELL {cid} ({cell.cell_type}):", cell.node_state)


if __name__ == "__main__":
    test_closed_loop()
