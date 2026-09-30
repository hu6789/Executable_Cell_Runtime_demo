import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class ScenarioCell:
    name: str
    type: str
    position: float


@dataclass(frozen=True)
class Scenario:
    name: str
    type: str
    cells: List[ScenarioCell]


def load_scenario(path):
    path = Path(path)

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    cells = [
        ScenarioCell(
            name=cell["name"],
            type=cell["type"],
            position=cell["position"],
        )
        for cell in data["cells"]
    ]

    return Scenario(
        name=data["name"],
        type=data["type"],
        cells=cells,
    )
    
def resolve_current_graphs(
    scenario_cell,
    type_definition_repository,
):
    definition = type_definition_repository.find_by_type(
        scenario_cell.type
    )

    return tuple(definition.current_graphs)
