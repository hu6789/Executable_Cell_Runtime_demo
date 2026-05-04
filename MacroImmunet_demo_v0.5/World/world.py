# ⚠️ TEMP HACK:
# movement handled in World for v0.5 visualization
# future: migrate to Intent-based movement system
import random
class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.cells = {}
        self.fields = {}
        self.field_defs = {}

    def add_cell(self, cell):
        self.cells[cell.cell_id] = cell

    def remove_cell(self, cid):
        if cid in self.cells:
            del self.cells[cid]

    def get_neighbors(self, cell):

        neighbors = []

        for other in self.cells.values():
            if other.cell_id == cell.cell_id:
                continue
 
            # 简单距离判定（曼哈顿）
            dx = abs(other.position[0] - cell.position[0])
            dy = abs(other.position[1] - cell.position[1])

            if dx <= 1 and dy <= 1:
                neighbors.append(other)

        return neighbors

    # =========================
    # ⚠️ TEMP HACK: movement
    # =========================
    def step(self):

        for cell in self.cells.values():

            if not cell.state_flags.get("alive", True):
                continue

            # 🔴 host 不动
            if cell.cell_type == "host_cell":
                continue

            # 🔵 CD8：追 pMHC
            if cell.cell_type == "cd8_t":
                self.biased_move_towards_field(cell, "pMHC")
                continue

            # 🟢 CD4：随机游走（轻微）
            if cell.cell_type == "cd4_t":
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])

                x, y = cell.position
                nx = max(0, min(self.width - 1, x + dx))
                ny = max(0, min(self.height - 1, y + dy))

                cell.position = (nx, ny)
                continue

    def biased_move_towards_field(self, cell, field_name):

        field = self.fields.get(field_name, {})
        if not field:
            return

        x, y = cell.position

        # 👇 看周围8格
        candidates = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = max(0, min(self.width - 1, x + dx))
                ny = max(0, min(self.height - 1, y + dy))

                val = field.get((nx, ny), 0)
                candidates.append((val, nx, ny))

        # 👉 选最大梯度方向
        _, tx, ty = max(candidates, key=lambda x: x[0])

        cell.position = (tx, ty)
# ⚠️ TEMP HACK:
# movement handled in World for v0.5 visualization
# future: migrate to Intent-based movement system




class Cell:
    def __init__(self, cid, cell_type, position):
        self.cell_id = cid
        self.cell_type = cell_type
        self.position = position

        self.node_state = {}
        self.state_flags = {
            "alive": True
        }

        self.params = {"behavior": {}}


