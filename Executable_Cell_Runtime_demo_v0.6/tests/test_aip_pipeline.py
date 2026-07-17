# test_aip_pipeline.py

from pprint import pprint

from scanmaster.scan_master import ScanMaster
from inputbuilder.input_builder import InputBuilder
from cellmaster.cell_master import CellMaster
from intentbuilder.intent_builder import IntentBuilder
from labelcenter.labelcenter import LabelCenter

from cellinstance.templates.template_loader import (
    TemplateLoader
)

from cellmaster.internalnet.runtime_graph.graph_loader import (
    RuntimeGraphLoader
)

from cellinstance.factory.cell_factory import (
    CellFactory
)


# ==========================================================
# Build Runtime World
# ==========================================================

template_loader = TemplateLoader()
template_loader.load_template_directory(
    "cellinstance/cells"
)

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

# ----------------------------------------------------------
# Host state
# ----------------------------------------------------------

cell.runtime_state["ATP"] = 80
cell.runtime_state["ROS"] = 1

# ----------------------------------------------------------
# Viral state (AIP test)
# ----------------------------------------------------------

cell.runtime_state["viral_RNA"] = 300
cell.runtime_state["viral_protein"] = 120
cell.runtime_state["capsid"] = 50

cell.runtime_state["viral_signal"] = 5
cell.runtime_state["IFNGR_activation"] = 10


# ==========================================================
# Dummy World
# ==========================================================

class DummyWorld:

    def __init__(self):

        self.cells = {}
        self.fields = {}
        self.field_defs = {}

    def add_cell(self, cell):

        self.cells[cell.id] = cell


world = DummyWorld()

world.add_cell(cell)

world.fields["IFN"] = {

    (0, 0): 1.0

}

world.field_defs["IFN"] = {}


# ==========================================================
# Runtime Components
# ==========================================================

scanmaster = ScanMaster()

inputbuilder = InputBuilder()

cellmaster = CellMaster()

intentbuilder = IntentBuilder()

labelcenter = LabelCenter()

tick = 1


# ==========================================================
# Scan
# ==========================================================

print("\n================ SCAN ================")

events = scanmaster.scan(
    world,
    tick
)


# ==========================================================
# InputBuilder
# ==========================================================

print("\n================ INPUT BUILDER ================")

inputbuilder.collect(events)

input_result = inputbuilder.build()

node_inputs = input_result["node_inputs"]


# ==========================================================
# CellMaster
# ==========================================================

print("\n================ CELL MASTER ================")

packages = cellmaster.run(

    node_inputs=node_inputs,

    world=world,

    tick=tick

)

print()

print("Packages:", len(packages))


# ==========================================================
# Runtime Debug
# ==========================================================

if packages:

    package = packages[0]

    runtime_output = package.get(
        "runtime_output",
        {}
    )

    print("\n================ OUTPUT KEYS ================")

    pprint(list(runtime_output.keys()))

    print("\n================ PROJECTED RUNTIME ================")

    pprint(
        package.get(
            "projected_runtime_state",
            {}
        )
    )

    print("\n================ PUBLIC EXPOSURE ================")

    pprint(
        package.get(
            "public_exposure",
            {}
        )
    )

    # ------------------------------------------------------
    # Optional AIP outputs
    # ------------------------------------------------------

    if "vml_output" in runtime_output:

        print("\n================ VML OUTPUT ================")

        pprint(
            runtime_output["vml_output"]
        )

    if "viral_behavior" in runtime_output:

        print("\n================ VIRAL BEHAVIOR ================")

        pprint(
            runtime_output["viral_behavior"]
        )

    if "modulation_runtime_state" in runtime_output:

        print("\n================ MODULATION STATE ================")

        pprint(
            runtime_output[
                "modulation_runtime_state"
            ]
        )


# ==========================================================
# IntentBuilder
# ==========================================================

print("\n================ INTENT BUILDER ================")

for package in packages:

    intentbuilder.collect(

        package.get(
            "intent_requests",
            []
        )
    )

intents = intentbuilder.build()

pprint(intents)


# ==========================================================
# LabelCenter
# ==========================================================

print("\n================ LABELCENTER ================")

labelcenter.collect(intents)

labelcenter.apply(
    world,
    tick
)


# ==========================================================
# Final World
# ==========================================================

print("\n================ FINAL WORLD ================")

print("\nRuntime State")

pprint(

    world.cells[
        "host_001"
    ].runtime_state.snapshot()

)

print("\nFields")

pprint(world.fields)

print()

print("================ AIP TEST DONE ================")
