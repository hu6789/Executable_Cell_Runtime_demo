# test_minisio_pipeline.py

from pprint import pprint

# =========================
# Core pipeline
# =========================

from minisio.core.minisio import MiniSIO

from scanmaster.scan_master import ScanMaster
from inputbuilder.input_builder import InputBuilder
from cellmaster.cell_master import CellMaster
from intentbuilder.intent_builder import IntentBuilder
from labelcenter.labelcenter import LabelCenter
from substance.substance_master.substance_master import SubstanceMaster

from cellinstance.templates.template_loader import TemplateLoader
from cellmaster.internalnet.runtime_graph.graph_loader import RuntimeGraphLoader
from cellinstance.factory.cell_factory import CellFactory
from cellinstance.templates.template_loader import TemplateLoader
from cellmaster.internalnet.runtime_graph.graph_loader import RuntimeGraphLoader

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


# =========================
# Dummy substance
# =========================

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

# =========================
# Build world
# =========================

world = DummyWorld()

world.add_cell(cell)

substance = DummySubstance()
world.add_substance(substance)

world.fields["IFN"] = {(0, 0): 1.0}
world.field_defs["IFN"] = {}


# =========================
# Core systems
# =========================

scanmaster = ScanMaster()
inputbuilder = InputBuilder()
cellmaster = CellMaster()
intentbuilder = IntentBuilder()
labelcenter = LabelCenter()

substance_master = SubstanceMaster()
minisio = MiniSIO()


# =========================
# 1. Scan
# =========================

print("\n================ SCAN ================")

events = scanmaster.scan(world, tick=1)
pprint(events)


# =========================
# 2. Input build
# =========================

print("\n================ INPUT ================")

inputbuilder.collect(events)

input_result = inputbuilder.build()

node_inputs = input_result["node_inputs"]

pprint(node_inputs)


# =========================
# 3. Cell runtime
# =========================

print("\n================ CELL ================")

packages = cellmaster.run(
    node_inputs=node_inputs,
    world=world,
    tick=1
)

print(f"packages: {len(packages)}")


# =========================
# 4. Substance pipeline
# =========================

print("\n================ SUBSTANCE ================")

substance_requests = substance_master.process(
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
    candidate_substances=[],
    world=world
)

pprint(substance_requests)


# =========================
# 5. IntentBuilder (merge cell + substance)
# =========================

print("\n================ INTENT BUILDER ================")

# cell intents
for p in packages:
    intentbuilder.collect(p.get("intent_requests", []))

# substance requests → fake intent wrapper
intentbuilder.collect([
    {
        "write_mode": "substance",
        "operation": r["operation"],
        "target_id": r["target_id"].id if hasattr(r["target_id"], "id") else r["target_id"],
        "payload": {"strength": r.get("strength", 0)}
    }
    for r in substance_requests
])

intents = intentbuilder.build()
pprint(intents)


# =========================
# 6. LabelCenter apply
# =========================

print("\n================ LABELCENTER ================")

labelcenter.collect(intents)
labelcenter.apply(world, tick=1)


# =========================
# 7. MiniSIO test (raw injection)
# =========================

print("\n================ MINISIO ================")

raw_requests = [
    {
        "operation": "create_substance",
        "write_mode": "substance",
        "target_id": "IFN",
        "payload": {
            "template_id": "IFN",
            "amount": 10
        },
        "tick": 1
    },
    {
        "operation": "set_runtime",
        "write_mode": "runtime_state",
        "target_id": "host_001",
        "payload": {
            "ATP": 80,
            "ROS": 2
        },
        "tick": 1
    }
]

mini_package = minisio.receive(raw_requests, metadata={"source": "test"})

pprint(mini_package.metadata)
pprint(mini_package.requests)


# =========================
# FINAL WORLD
# =========================

print("\n================ FINAL WORLD ================")

pprint(world.cells)
pprint(world.substances)
pprint(world.fields)
