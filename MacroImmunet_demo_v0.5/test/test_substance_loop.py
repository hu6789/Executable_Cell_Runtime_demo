from scan_master.scan_master import ScanMaster
from Input_builder.substance_input_builder import SubstanceInputBuilder
from Substance.master.perforin_master import PerforinMaster
from Intent_builder.action_adapter import to_intents
from Intent_builder.intentbuilder import IntentBuilder
class Cell:
    def __init__(self, cid):
        self.cell_id = cid
        self.position = (0, 0)
        self.state_flags = {"infected": True}
        self.node_state = {}


class World:
    def __init__(self):
        self.fields = {
            "perforin": {(0, 0): 1.0},
            "IL2": {(0, 0): 2.0}
        }

        self.field_defs = {
            "perforin": {
                "type": "effector",
                "interaction": {
                    "kind": "damage",
                    "conversion": {"damage_scale": 0.5},
                    "filter": {"cell_flags": ["infected"]}
                }
            },
            "IL2": {
                "type": "signal",
                "interaction": {
                    "kind": "signal",
                    "conversion": {"scale": 1.0}
                }
            }
        }

        self.cells = {
            1: Cell(1)
        }

    def get_neighbors(self, cell):
        return []
def test_substance_loop():
    print("\n===== SUBSTANCE TEST =====")

    world = World()

    scan = ScanMaster(world, event_lib=[])

    input_builder = SubstanceInputBuilder()
    
    masters = [PerforinMaster()]
    intent_builder = IntentBuilder()

    # 1️⃣ scan（统一入口）
    events = scan.scan(tick=0)
    print("EVENTS:", events)
    print("FIELDS:", world.fields)
    # 2️⃣ input → interactions
    interactions = input_builder.build(events, world)
    world.interactions = interactions

    print("INTERACTIONS:", interactions)
    print("CELL:", world.cells)
    print("FIELD_DEFS:", world.field_defs)

    # 3️⃣ master → actions
    actions = []
    for m in masters:
        actions += m.step(interactions)

    print("ACTIONS:", actions)

    # 4️⃣ actions → intents
    intents = to_intents(actions, intent_builder, tick=0)

    print("INTENTS:", intents)

if __name__ == "__main__":
    test_substance_loop()
