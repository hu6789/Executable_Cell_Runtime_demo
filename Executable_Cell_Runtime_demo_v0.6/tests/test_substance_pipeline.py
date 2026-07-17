# test_substance_pipeline.py

from pprint import pprint

from substance.substance_master.substance_master import SubstanceMaster

from scanmaster.scan_master import ScanMaster
from inputbuilder.input_builder import InputBuilder
from cellmaster.cell_master import CellMaster
from intentbuilder.intent_builder import IntentBuilder
from labelcenter.labelcenter import LabelCenter
from cellinstance.factory.cell_factory import CellFactory
from cellinstance.templates.template_loader import TemplateLoader
from cellmaster.internalnet.runtime_graph.graph_loader import RuntimeGraphLoader

# =========================================================
# Dummy Substance
# =========================================================

class DummySubstance:

    def __init__(self):

        self.id = "perforin_001"
        self.substance_type = "perforin"
        self.position = (0, 0)
        self.amount = 10.0


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


def build_world():

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

    # runtime init（你之前测试用的）
    cell.position = (0, 0)
    cell.runtime_state["IFNGR_activation"] = 10.0
    cell.runtime_state["viral_signal"] = 5.0

    world = DummyWorld()
    world.add_cell(cell)

    world.fields["IFN"] = {(0, 0): 1.0}
    world.field_defs["IFN"] = {}

    return world
class DummyWorld:

    def __init__(self):
        self.cells = {}
        self.fields = {}
        self.field_defs = {}

    def add_cell(self, cell):
        self.cells[cell.id] = cell


# =========================================================
# Build World
# =========================================================

world = DummyWorld()

world.add_cell(cell)

substance = DummySubstance()
world.add_substance(substance)

world.fields["IFN"] = {
    (0, 0): 1.0
}

world.field_defs["IFN"] = {}


# =========================================================
# Runtime Components
# =========================================================

scanmaster = ScanMaster()
inputbuilder = InputBuilder()
cellmaster = CellMaster()
intentbuilder = IntentBuilder()
labelcenter = LabelCenter()

substance_master = SubstanceMaster()

tick = 1


# =========================================================
# PIPELINE START
# =========================================================

print("\n================ BUILD WORLD ================")

print("\nCells:")
pprint(world.cells)

print("\nSubstances:")
pprint(world.substances)

print("\nFields:")
pprint(world.fields)


# =========================================================
# CELL PIPELINE (optional but useful for context)
# =========================================================

print("\n================ CELL PIPELINE ================")

events = scanmaster.scan(world, tick)
inputbuilder.collect(events)

node_inputs = inputbuilder.build()["node_inputs"]

packages = cellmaster.run(
    node_inputs=node_inputs,
    world=world,
    tick=tick
)

print("\nCELL PACKAGES:", len(packages))


# =========================================================
# SUBSTANCE PIPELINE (核心)
# =========================================================

print("\n================ SUBSTANCE PIPELINE ================")

requests = substance_master.process(

    substance=substance,
    template={
        "interaction_mode": "active",
        "interaction_rules": [
            {
                "target_type": "cell",
                "effect_type": "membrane_damage",
                "base_strength": 5.0
            }
        ]
    },

    candidate_cells=list(world.cells.values()),
    candidate_substances=list(world.substances.values()),
    world=world

)

print("\nSUBSTANCE REQUESTS:")
pprint(requests)


# =========================================================
# INTENT BUILD + LABELCENTER
# =========================================================

print("\n================ INTENT + LABELCENTER ================")

intentbuilder.collect(requests)
intents = intentbuilder.build()

print("\nINTENTS:")
pprint(intents)

labelcenter.collect(intents)
labelcenter.apply(world, tick)


# =========================================================
# FINAL WORLD
# =========================================================

print("\n================ FINAL WORLD ================")

print("\nCells runtime state:")
pprint(world.cells["host_001"].runtime_state)

print("\nSubstances:")
pprint(world.substances)

print("\nFields:")
pprint(world.fields)

print("\n================ DONE ================")
