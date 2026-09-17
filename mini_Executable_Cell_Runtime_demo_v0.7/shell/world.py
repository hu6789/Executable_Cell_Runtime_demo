from shell.schema import CellState, WorldState
from shell.shh_field import SHHField


class World:
    """
    Minimal World container for the v0.7 demo.

    World owns persistent cell states and the extracellular SHH field.
    """

    def __init__(
        self,
        state=None,
        shh_field=None,
    ):
        if state is None:
            state = WorldState()

        if shh_field is None:
            shh_field = SHHField()

        self.state = state
        self.state.shh_field = shh_field

    def add_cell(self, cell):
        if cell.id in self.state.cells:
            raise ValueError(
                "Cell already exists: {}".format(cell.id)
            )

        self.state.cells[cell.id] = cell

    def get_cell(self, cell_id):
        if cell_id not in self.state.cells:
            raise KeyError(
                "Cell not found: {}".format(cell_id)
            )

        return self.state.cells[cell_id]

    def shh_concentration(self, position):
        return self.state.shh_field.concentration_at(position)
