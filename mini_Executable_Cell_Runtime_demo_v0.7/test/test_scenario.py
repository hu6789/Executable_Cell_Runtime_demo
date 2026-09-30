import json
from pathlib import Path
from demo.scenario_loader import (
    Scenario,
    ScenarioCell,
    load_scenario,
    resolve_current_graphs,
)
from internalnet.hir.type.repository import (
    TypeDefinitionRepository,
)
TYPE_DEFINITION_PATH = (
    Path(__file__).resolve().parents[1]
    / "internalnet"
    / "hir"
    / "library"
    / "type_definitions.json"
)

SCENARIO_DIR = (
    Path(__file__).resolve().parents[1]
    / "demo"
    / "scenario"
)


def load_scenario_json(name):
    path = SCENARIO_DIR / name
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_abc_same_environment():
    scenario = load_scenario_json("abc_same_environment.json")

    assert scenario["name"] == "abc_same_environment"
    assert scenario["type"] == "static"

    cells = scenario["cells"]

    assert [cell["name"] for cell in cells] == [
        "A",
        "B",
        "C",
    ]

    assert [cell["type"] for cell in cells] == [
        "neural_progenitor",
        "floor_plate_progenitor",
        "motor_neuron_progenitor",
    ]

    assert [cell["position"] for cell in cells] == [
        0.0,
        1.0,
        2.0,
    ]


def test_shh_patterning():
    scenario = load_scenario_json("shh_patterning.json")

    assert scenario["name"] == "shh_patterning"
    assert scenario["type"] == "patterning"

    cells = scenario["cells"]

    assert len(cells) == 12

    assert [cell["name"] for cell in cells] == [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
    ]

    assert cells[5]["type"] == "floor_plate_progenitor"

    for cell in cells[:5] + cells[6:]:
        assert cell["type"] == "neural_progenitor"

    assert all(
        "graph_ids" not in cell
        for cell in cells
    )
    
def test_load_abc_scenario():
    scenario = load_scenario(
        SCENARIO_DIR / "abc_same_environment.json"
    )

    assert isinstance(scenario, Scenario)
    assert len(scenario.cells) == 3

    assert scenario.cells[0] == ScenarioCell(
        name="A",
        type="neural_progenitor",
        position=0.0,
    )

    assert scenario.cells[1] == ScenarioCell(
        name="B",
        type="floor_plate_progenitor",
        position=1.0,
    )

    assert scenario.cells[2] == ScenarioCell(
        name="C",
        type="motor_neuron_progenitor",
        position=2.0,
    )


def test_load_shh_patterning_scenario():
    scenario = load_scenario(
        SCENARIO_DIR / "shh_patterning.json"
    )

    assert isinstance(scenario, Scenario)
    assert scenario.name == "shh_patterning"
    assert scenario.type == "patterning"

    assert len(scenario.cells) == 12

    assert scenario.cells[5] == ScenarioCell(
        name="B",
        type="floor_plate_progenitor",
        position=5.0,
    )

    assert all(
        cell.type == "neural_progenitor"
        for cell in scenario.cells[:5]
    )

    assert all(
        cell.type == "neural_progenitor"
        for cell in scenario.cells[6:]
    )
    
    
    
def test_resolve_current_graphs_for_neural_progenitor():
    scenario = load_scenario(
        SCENARIO_DIR / "shh_patterning.json"
    )

    repository = TypeDefinitionRepository(
        TYPE_DEFINITION_PATH
    )

    cell = scenario.cells[0]

    assert cell.type == "neural_progenitor"

    assert resolve_current_graphs(
        cell,
        repository,
    ) == (
        "common_shh_signaling",
        "neural_progenitor_core",
    )


def test_resolve_current_graphs_for_floor_plate():
    scenario = load_scenario(
        SCENARIO_DIR / "shh_patterning.json"
    )

    repository = TypeDefinitionRepository(
        TYPE_DEFINITION_PATH
    )

    cell = scenario.cells[5]

    assert cell.name == "B"
    assert cell.type == "floor_plate_progenitor"

    assert resolve_current_graphs(
        cell,
        repository,
    ) == (
        "common_shh_signaling",
        "floor_plate_progenitor",
    )
    
    

