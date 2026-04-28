class World:

    def __init__(self, width=20, height=20):

        self.width = width
        self.height = height

        # 🧬 cells
        self.cells = {}   # {cell_id: cell_instance}

        # 🌊 fields（IL2 / perforin 等）
        self.fields = {}  # {field_name: {(x,y): value}}

        # ⚙️ field 参数
        self.field_defs = {
            "IL2": {
                "sigma": 1.5,
                "diffusion": 0.2,
                "decay_tau": 10
            },
            "perforin": {
                "sigma": 1.0,
                "diffusion": 0.1,
                "decay_tau": 5
            }
        }

    def add_cell(self, cell):
        self.cells[cell.cell_id] = cell

    def remove_cell(self, cell_id):
        if cell_id in self.cells:
            del self.cells[cell_id]
