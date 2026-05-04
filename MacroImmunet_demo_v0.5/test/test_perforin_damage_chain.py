# test_perforin_damage_chain.py
from scan_master.scan_master import ScanMaster
from Input_builder.inputbuilder import InputBuilder
from Substance.substance_master import SubstanceMaster
from Intent_builder.intentbuilder import IntentBuilder
from Cell_master.Internalnet.node_engine import load_nodes
from scan_master.event_loader import load_event_lib
from World.Registry_library import REGISTRY
from Substance.master.perforin_master import PerforinMaster
class Cell:
    def __init__(self, cid):
        self.cell_id = cid
        self.cell_type = "target"
        self.position = (0, 0)

        self.node_state = {
            "membrane": 1.0,
            "Ca_flux": 0.0,
            "stress": 0.0,
            "damage": 0.0,
            "viral_load": 0.0
        }

        self.state_flags = {
            "infected": True,
            "alive": True,
            "dying": False
        }
        self.params = {"behavior": {}}
class World:
    def __init__(self):
        self.width = 10
        self.height = 10

        self.cells = {
            1: Cell(1)
        }

        # 👇 关键：field 里真的有 perforin
        self.fields = {
            "perforin": {(0, 0): 1.0}
        }

        # 👇 必须带 interaction（否则 SubstanceMaster 不工作）
        self.field_defs = {
            "perforin": {
                "interaction": {
                    "kind": "effector",
                    "conversion": {"scale": 1.0},
                    "filter": {
                        "cell_flags": ["infected"]
                    }
                }
            }
        }

    def get_neighbors(self, cell):
        return []
    def remove_cell(self, cid):
        print(f"[WORLD] remove_cell {cid}")
        if cid in self.cells:
            del self.cells[cid]
def test_perforin_chain():

    print("\n===== PERFORIN FULL CHAIN TEST =====")

    world = World()

    event_lib = load_event_lib("scan_master/event_lib")

    scan = ScanMaster(world, event_lib=event_lib)

    node_defs = {n["node_id"]: n for n in load_nodes()}
    input_builder = InputBuilder(node_defs, REGISTRY)

    substance_master = SubstanceMaster(world, world.field_defs)
    net = InternalNet(behaviors=None)
    intent_builder = IntentBuilder()
    label = LabelCenter()

    for tick in range(10):

        print(f"\n--- TICK {tick} ---")

        # 1️⃣ scan
        events = scan.scan(tick=tick)

        # 2️⃣ input
        ib_out = input_builder.build(events, cells=world.cells, world=world)

        cell_inputs = ib_out["cell"]
        substance_inputs = [
            s for s in ib_out["substance"]
            if world.cells.get(s.get("target"))
            and world.cells[s["target"]].state_flags.get("alive", True)
        ]

        # 3️⃣ substance（🔥 perforin 在这里触发）
        substance_actions = substance_master.step(substance_inputs)

        print("[SUBSTANCE ACTIONS]", substance_actions)

        # 4️⃣ cell
        cell_outputs = net.step_cells(world, cell_inputs)

        # 5️⃣ intent
        intents = intent_builder.build(
            cell_outputs=cell_outputs,
            substance_actions=substance_actions,
            tick=tick
        )

        print("[INTENTS]")
        for i in intents:
            print(i)

        # 6️⃣ apply
        label.collect(intents)
        label.apply(world)

        # 7️⃣ state观察
        cell = world.cells.get(1)
 
        if cell is None:
            print("\n[STATE] cell removed")
            break
        ns = cell.node_state

        print("\n[STATE]")
        print("membrane:", ns.get("membrane"))
        print("Ca_flux:", ns.get("Ca_flux"))
        print("stress:", ns.get("stress"))
        print("damage:", ns.get("damage"))
if __name__ == "__main__":

    from Label_center.labelcenter import LabelCenter
    from Cell_master.Internalnet.cellmaster_engine import InternalNet

    # 初始化 world
    world = World()

    # 初始化 label center
    label = LabelCenter()

    # 初始化 cell master
    cell_master = InternalNet(behaviors=None)

    # field_defs（你已有配置）
    field_defs = {
        "perforin": {
            "interaction": {
                "conversion": {
                    "scale": 1.0
                }
            }
        }
    }

    # 👉 调用测试
    test_perforin_chain()
