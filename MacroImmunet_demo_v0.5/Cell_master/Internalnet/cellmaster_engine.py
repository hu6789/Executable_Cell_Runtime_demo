# cellmaster/Internalnet/internalnet_engine.py

import os
import glob
import json
from Cell_master.Internalnet.node_engine import run_node_graph, load_nodes, collect_emitters
from Cell_master.Internalnet.passive_engine import run_passive_engine, load_passives
from Cell_master.Internalnet.behavior_engine import evaluate_behaviors
from Cell_master.Internalnet.HIR.hir_core import compute_HIR
from Cell_master.Internalnet.graph_loader import GraphLoader
from Cell_master.state_updata.state_updata import apply_dynamics
from Cell_master.state_updata.state_updata import collect_deltas
from Cell_master.state_updata.state_updata import compute_state_update
class InternalNet:

    def __init__(self, behaviors):

        if behaviors is None:
            behavior_dir = os.path.join(
                os.path.dirname(__file__), "behavior"
            )
            self.behaviors = []
            for path in glob.glob(os.path.join(behavior_dir, "*.json")):
                with open(path) as f:
                    self.behaviors.append(json.load(f))
            print(f"[DEBUG] Loaded {len(self.behaviors)} behaviors from {behavior_dir}")
        else:
            self.behaviors = behaviors

        # =========================
        # Node defs（registry）
        # =========================
        self.node_defs = {
            n["node_id"]: n
            for n in load_nodes()
        }

        # =========================
        # Passive defs
        # =========================
        self.passive_defs = load_passives()
        print("[DEBUG] passive_defs loaded:", type(self.passive_defs), len(self.passive_defs))

        self.graph_loader = GraphLoader()
        self.graph_map = {
            "host_cell": ["base", "host"],
            "target": ["base", "host"],   
            "cd4_t": ["base", "CD4"],
            "cd8_t": ["base", "CD8"]
        }
        self.behavior_graph = self.graph_loader.load_behavior_graph(["base"])

    # =========================
    # 🔹 单步执行（唯一入口）
    # =========================
    def step(self, cell, node_input):

        before_state = dict(cell.node_state)
        
        # =========================
        # 0️⃣ init
        # =========================
        node_state = dict(cell.node_state)
        node_deltas = {}

        # =========================
        # 1️⃣ Load graph（只影响 node）
        # =========================
        graph_names = self.graph_map.get(cell.cell_type, ["base"]) 

        node_graph = self.graph_loader.load_node_graph(graph_names)
        print("[DEBUG] node_graph loaded from:", graph_names)
        print("[DEBUG] node_graph content keys:", node_graph.keys())
        behavior_graph = self.graph_loader.load_behavior_graph(graph_names)

        # =========================
        # 2️⃣ Node Engine
        # =========================
        old_state = dict(node_state)
        node_state, update_order = run_node_graph(
            node_state,
            node_graph,
            self.node_defs,
            node_input
        )
        node_deltas["node"] = {
            k: node_state[k] - old_state.get(k, 0.0)
            for k in node_state
            if abs(node_state[k] - old_state.get(k, 0.0)) > 1e-6
        }

        # =========================
        # 3️⃣ Passive Engine（🔥关键）
        # =========================
        print("[DEBUG] node_state before passive:", node_state)
        passive_delta, passive_logs = run_passive_engine(node_state, self.passive_defs)
        node_deltas["passive"] = passive_delta.copy()
        for k, v in passive_delta.items():
            node_state[k] = node_state.get(k, 0.0) + v

        node_state_pre_behavior = dict(node_state)   
        for p in self.passive_defs:
            print("[CHECK PASSIVE]", p["passive_id"], "trigger:", p.get("trigger"))
        print("node_state:", node_state)
        # =========================
        # 4️⃣ HIR（只看 node_state）
        # =========================
        hir_output = compute_HIR(node_state, cell)

        # =========================
        # 5️⃣ Behavior Engine
        # =========================
        behavior_outputs = evaluate_behaviors(
            node_state,
            hir_output,
            self.behaviors,
            graph=behavior_graph,
            cell=cell
        ) 

        # =========================
        # 6️⃣ State Update
        # =========================
        state_delta, new_state = compute_state_update(
            node_state,
            behavior_outputs,
            self.node_defs
        )

        cell.node_state = new_state
        print("[NODE DELTAS]", node_deltas)
        print("[STATE AFTER UPDATE]", new_state)
        # =========================
        # 8️⃣ Debug（结构化）
        # =========================
        self._debug_step(
            cell,
            before_state,
            node_state_pre_behavior, 
            node_input,
            hir_output,
            behavior_outputs,
            passive_logs
        )

        return {
            "behaviors": behavior_outputs,
            "hir": hir_output,
            "state_delta": state_delta,
            "fate": hir_output.get("fate", "normal"),
        }

    # =========================
    # 🔹 Debug（结构化输出）
    # =========================
    def _debug_step(
        self,
        cell,
        before_state,
        node_state_pre,
        node_input,
        hir_output,
        behaviors,
        passive_logs
    ):

        print("\n==============================")
        print(f" InternalNet Step | {cell.cell_type}")
        print("==============================")

        # -------------------------
        # INPUT
        # -------------------------
        print("\n[INPUT]")
        print("node_input:", node_input)

        # -------------------------
        # PASSIVE EFFECTS
        # -------------------------
        print("\n[PASSIVE]")

        if not passive_logs:
            print("  (none)")
        else:
            for d in passive_logs:
                print(
                    f"  {d['passive']} | "
                    f"{d['node']} Δ {round(d['delta'],3)}"
                )

        # -------------------------
        # STATE BEFORE BEHAVIOR（HIR看到的）
        # -------------------------
        print("\n[STATE BEFORE BEHAVIOR]")
        for k in sorted(node_state_pre.keys()):
            before = before_state.get(k, 0.0)
            after = node_state_pre.get(k, 0.0)

            if abs(after - before) > 1e-4:
                print(f"  {k}: {round(before,3)} → {round(after,3)}")

        # -------------------------
        # HIR
        # -------------------------
        print("\n[HIR]")
        print("  fate:", hir_output.get("fate"))

        features = hir_output.get("features", {})
        for k, v in features.items():
            print(f"  {k}: {round(v,3)}")

        # -------------------------
        # BEHAVIORS
        # -------------------------
        print("\n[BEHAVIORS]")
        for b in behaviors:
            print(
                f"  {b['behavior_id']} | "
                f"act={round(b['activation'],3)} "
                f"drive={round(b['drive'],3)}"
            )

        print("==============================\n")
