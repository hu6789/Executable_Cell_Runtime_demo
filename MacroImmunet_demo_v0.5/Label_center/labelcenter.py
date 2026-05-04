# Label_center/labelcenter.py

from collections import defaultdict
from Cell_master.state_updata.state_updata import apply_dynamics
from Cell_master.Internalnet.node_engine import load_nodes
import math

class LabelCenter:

    def __init__(self, field_defs=None):

        self.intents = []
        self.field_defs = field_defs or {}
        self.node_defs = {n["node_id"]: n for n in load_nodes()}

    # =========================
    # 收集 intents
    # =========================
    def collect(self, intents):
        if intents:
            self.intents.extend(intents)
    # =========================
    # 主执行
    # =========================
    def apply(self, world, tick):
        self.field_defs = world.field_defs

        # 1️⃣ 分桶
        buckets = self._bucket_intents(self.intents)

        # ✅ ① effect 先打（外部伤害或直接 delta）
        effect_acc = self._collect_effect_deltas(buckets)
        self._apply_state_updates(world, effect_acc)

        # ✅ ② 再处理 cell_state（行为/修复）
        cell_acc = self._collect_cellstate_deltas(buckets)
        self._apply_state_updates(world, cell_acc)

        # 3️⃣ field（⭐ kernel 投影）
        sources = self._build_sources(world, buckets["field"])
        self._project_sources(world, sources)

        # 4️⃣ fate（死亡等）
        self._apply_fate(world, buckets["fate"])

        # 5️⃣ dynamics
        self._apply_diffusion(world)
        self._apply_decay(world)

        # 6️⃣ cleanup
        self._cleanup(world)

        # clear
        self.intents.clear()

    # =========================
    # 分桶
    # =========================
    def _bucket_intents(self, intents):

        buckets = {
            "effect": [],
            "field": [],
            "fate": [],
            "cell_state": []
        }

        for it in intents:
            t = it.get("type")

            if t == "add_field":
                buckets["field"].append(it)

            elif t == "death":          # ⭐ 核心修复
                buckets["fate"].append(it)

            elif t in buckets:
                buckets[t].append(it)

        return buckets

    # =========================
    # effect → delta（直接透传 payload）
    # =========================
    def _collect_effect_deltas(self, buckets):

        acc = defaultdict(lambda: defaultdict(float))

        for it in buckets["effect"]:
            payload = it.get("payload", {})
            cid = it.get("target")
            # 直接用 payload 提供的 node 和 delta/value
            node = payload.get("node")
            delta = payload.get("delta", payload.get("value", 0.0))

            if cid and node:
                acc[cid][node] += delta

        return acc

    # =========================
    # cell_state → delta
    # =========================
    def _collect_cellstate_deltas(self, buckets):

        acc = defaultdict(lambda: defaultdict(float))

        for it in buckets["cell_state"]:
            cid = it.get("target")
            payload = it.get("payload", {})
            node = payload.get("node")
            delta = payload.get("delta", 0.0)

            if node:
                acc[cid][node] += delta

        return acc

    # =========================
    # 应用 state delta
    # =========================
    def _apply_state_updates(self, world, acc):

        for cid, node_deltas in acc.items():

            cell = world.cells.get(cid)

            if not cell or not cell.state_flags.get("alive", True):
                continue

            prev_state = dict(cell.node_state)

            new_state = apply_dynamics(
                prev_state,
                node_deltas,
                self.node_defs
            )

            cell.node_state = new_state

    # =========================
    # field source 构建
    # =========================
    def _build_sources(self, world, intents):

        sources = []

        for it in intents:
            if it.get("type") != "add_field":
                continue
            payload = it.get("payload", {})
            field = payload.get("field")
            value = payload.get("value", 0.0)

            if not field:
                continue

            cell = world.cells.get(it.get("source"))
            if not cell:
                continue

            source = {
                "field": field,
                "amount": value,
                "pos": tuple(cell.position),
                "source": it.get("source") 
            }

            sources.append(source)

        return sources

    # =========================
    # field 投影 kernel
    # =========================
    def _project_sources(self, world, sources):

        acc = defaultdict(lambda: defaultdict(float))

        for src in sources:

            field = src["field"]
            amount = src["amount"]
            cx, cy = src["pos"]

            cfg = self.field_defs.get(field, {})
            sigma = cfg.get("sigma", 1.0)
            radius = int(3 * sigma) + 1

            weights = []

            # 收集
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):

                    x = cx + dx
                    y = cy + dy

                    if not (0 <= x < world.width and 0 <= y < world.height):
                        continue

                    dist = math.sqrt(dx * dx + dy * dy)
                    w = self._gaussian_kernel(dist, sigma)

                    weights.append(((x, y), w))

            # 归一化
            total_w = sum(w for _, w in weights)
            if total_w <= 0:
                continue

            # 写入
            for (x, y), w in weights:
                acc[field][(x, y)] += amount * (w / total_w)

        # aggregation
        for fname, grid in acc.items():

            world.fields.setdefault(fname, {})

            cfg = self.field_defs.get(fname, {})
            max_val = cfg.get("max", 1.0)

            for pos, val in grid.items():

                old = world.fields[fname].get(pos, 0.0)
                new = min(max_val, old + val)

                world.fields[fname][pos] = new

    # =========================
    # Gaussian kernel
    # =========================
    def _gaussian_kernel(self, dist, sigma):

        if sigma <= 0:
            return 0.0

        return math.exp(-(dist ** 2) / (2 * sigma ** 2))

    # =========================
    # fate（死亡）
    # =========================
    def _apply_fate(self, world, intents):

        for it in intents:
            if it.get("type") != "death":
                continue

            cid = it.get("target")
            cell = world.cells.get(cid)

            if not cell:
                continue

            # 1️⃣ 标记死亡（不要立刻删）
            cell.state_flags["alive"] = False

    # =========================
    # diffusion
    # =========================
    def _apply_diffusion(self, world):

        for fname, grid in world.fields.items():

            cfg = self.field_defs.get(fname, {})
            rate = cfg.get("diffusion", 0.0)

            if rate <= 0:
                continue

            new_grid = defaultdict(float)

            for (x, y), val in grid.items():

                share = val * rate
                remain = val - share

                new_grid[(x, y)] += remain

                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < world.width and 0 <= ny < world.height:
                        new_grid[(nx, ny)] += share / 4

            world.fields[fname] = dict(new_grid)

    # =========================
    # decay
    # =========================
    def _apply_decay(self, world):

        for fname, grid in world.fields.items():

            cfg = self.field_defs.get(fname, {})
            tau = cfg.get("decay_tau", 10.0)

            if tau <= 0:
                continue

            new_grid = {}

            for pos, val in grid.items():

                new_val = val * (tau - 1) / tau

                if new_val > 1e-4:
                    new_grid[pos] = new_val

            world.fields[fname] = new_grid

    # =========================
    # cleanup
    # =========================
    def _cleanup(self, world):

        dead = [
            cid for cid, c in world.cells.items()
            if not c.state_flags.get("alive", True)
        ]

        for cid in dead:
            world.remove_cell(cid)
