# test_runtime_pipeline.py

from pprint import pprint

from scanmaster.scan_master import ScanMaster
from inputbuilder.input_builder import InputBuilder
from cellmaster.cell_master import CellMaster
from intentbuilder.intent_builder import IntentBuilder
from labelcenter.labelcenter import LabelCenter

from cellinstance.templates.template_loader import TemplateLoader
from cellmaster.internalnet.runtime_graph.graph_loader import RuntimeGraphLoader
from cellinstance.factory.cell_factory import CellFactory


# =========================================================
# Build World
# =========================================================

template_loader = TemplateLoader()
template_loader.load_template_directory("cellinstance/cells")

graph_loader = RuntimeGraphLoader()

factory = CellFactory(
    template_loader,
    graph_loader
)

cell = factory.create_runtime_entity(
    template_id="host_cell",
    cell_id="host_001"
)

cell.position = (0, 0)
cell.runtime_state["ATP"] = 80
cell.runtime_state["ROS"] = 1


class DummyWorld:
    def __init__(self):
        self.cells = {}
        self.fields = {}
        self.field_defs = {}

    def add_cell(self, cell):
        self.cells[cell.id] = cell


world = DummyWorld()
world.add_cell(cell)

world.fields["IFN"] = {(0, 0): 1.0}
world.field_defs["IFN"] = {}


# =========================================================
# Runtime Components
# =========================================================

scanmaster = ScanMaster()
inputbuilder = InputBuilder()
cellmaster = CellMaster()
intentbuilder = IntentBuilder()
labelcenter = LabelCenter()

tick = 1


# =========================================================
# 1. Scan
# =========================================================

print("\n===== SCAN =====")
events = scanmaster.scan(world, tick)


# =========================================================
# 2. InputBuilder
# =========================================================

print("\n===== INPUT BUILDER =====")
inputbuilder.collect(events)
input_result = inputbuilder.build()

node_inputs = input_result["node_inputs"]


# =========================================================
# 3. CellMaster
# =========================================================

print("\n===== CELL MASTER =====")
packages = cellmaster.run(
    node_inputs=node_inputs,
    world=world,
    tick=tick
)


# =========================================================
# 4. IntentBuilder
# =========================================================

print("\n===== INTENT BUILDER =====")

for p in packages:
    intentbuilder.collect(p.get("intent_requests", []))

intents = intentbuilder.build()

pprint(intents)


# =========================================================
# 5. LabelCenter
# =========================================================

print("\n===== LABELCENTER =====")

labelcenter.collect(intents)
labelcenter.apply(world, tick)


# =========================================================
# FINAL WORLD
# =========================================================

print("\n===== FINAL WORLD =====")

print("\nCells:")
pprint(world.cells)

print("\nFields:")
pprint(world.fields)

print("\nRuntime State:")
pprint(world.cells["host_001"].runtime_state.snapshot())

print("\n===== DONE =====")
