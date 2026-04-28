class Cell:

    def __init__(self, cid, cell_type, position):

        # =========================
        # Identity
        # =========================
        self.cell_id = cid
        self.cell_type = cell_type
        self.position = position

        # =========================
        # Core State（唯一真状态）
        # =========================
        self.node_state = {}

        # =========================
        # HIR state（运行时标签）
        # =========================
        self.hir_state = {
            "fate": "normal",
            "labels": []
        }

        # =========================
        # Parameters（全部调参入口）
        # =========================
        self.params = {
            "feature": {},   # → HIR
            "node": {},      # → NodeEngine
            "behavior": {}   # → BehaviorEngine
        }

        # =========================
        # Flags（生命周期）
        # =========================
        self.flags = {
            "alive": True
        }

        # =========================
        # Meta（调试/分析）
        # =========================
        self.meta = {}
