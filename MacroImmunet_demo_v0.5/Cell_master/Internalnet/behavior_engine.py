import math

def build_drive_from_graph(node_state, behavior_id, graph):
    inputs = []

    for edge in graph["edges"]:
        if edge["target"] != behavior_id:
            continue

        source = edge["source"]
        weight = edge.get("weight", 1.0)

        val = node_state.get(source, 0.0)

        # gate 判断
        gate = edge.get("gate")
        if gate:
            ok = True
            for cond in gate.get("conditions", []):
                op = cond["op"]
                th = cond["value"]

                if op == ">" and not (val > th):
                    ok = False
                elif op == "<" and not (val < th):
                    ok = False

            if not ok:
                continue

        inputs.append(val * weight)

    if not inputs:
        return None

    drive = sum(inputs)

    if graph.get("default_drive_normalize"):
        drive = min(1.0, drive)
    print(f"[GRAPH] building drive for {behavior_id}")
    print("edges:", graph.keys())
    print("inputs:", inputs)
    return drive
def eval_gate(node_state, gate_cfg):
    if not gate_cfg:
        return True

    results = []

    for cond in gate_cfg.get("conditions", []):
        val = node_state.get(cond["node"], 0.0)
        op = cond["op"]
        th = cond["value"]

        if op == ">":
            results.append(val > th)
        elif op == "<":
            results.append(val < th)
        elif op == ">=":
            results.append(val >= th)
        elif op == "<=":
            results.append(val <= th)
        elif op == "==":
            results.append(val == th)

    logic = gate_cfg.get("logic", "all")

    return all(results) if logic == "all" else any(results)


def compute_drive(node_state, drive_cfg):
    inputs = drive_cfg.get("inputs", [])
    dtype = drive_cfg.get("type", "weighted_sum")

    values = [
        node_state.get(i["node"], 0.0) * i.get("weight", 1.0)
        for i in inputs
    ]

    if not values:
        return 0.0

    if dtype == "weighted_sum":
        val = sum(values)
    elif dtype == "product":
        val = math.prod(values)
    elif dtype == "max":
        val = max(values)
    else:
        val = 0.0

    if drive_cfg.get("normalize"):
        val = min(1.0, val)

    return val


def apply_hir(drive, behavior, hir_output):
    hir_cfg = behavior.get("hir", {})
    group = hir_cfg.get("group")

    # block
    if "block" in hir_cfg.get("mode", []):
        if hir_output["blocks"].get(group, False):
            drive *= 0.05

    # scale
    if "scale" in hir_cfg.get("mode", []):
        drive *= hir_output["group_modifiers"].get(group, 1.0)

    return drive
def activate(drive, act_cfg, cell=None):

    th = act_cfg.get("threshold_base", 0.0)
    slope = act_cfg.get("slope", 4.0)

    if cell is not None:
        behavior_mod = cell.params.get("behavior", {})
        b_id = act_cfg.get("behavior_id")

        if b_id and b_id in behavior_mod:
            mod = behavior_mod[b_id]

            th += mod.get("threshold_shift", 0.0)
            slope *= mod.get("slope_scale", 1.0)

    if act_cfg.get("mode") == "deterministic":
        return 1.0 if drive >= th else 0.0
    else:
        slope = act_cfg.get("slope", 4.0)
        x = drive - th
        return 1 / (1 + math.exp(-slope * x))

def build_outputs(b, activation, drive, cell=None):

    outputs = []

    targets = b.get("output", {}).get("targets", [])
    out_def = b.get("output", {})
    out_type = out_def.get("type")

    for tgt in targets:

        val = tgt.get("value", 0.0)

        # scaling
        if tgt.get("scale_by") == "activation":
            val *= activation
        elif tgt.get("scale_by") == "drive":
            val *= drive

        # -------------------------
        # internal_state
        # -------------------------
        if tgt.get("type") == "internal_state":

            outputs.append({
                "type": "internal_state",
                "node": tgt["node"],
                "value": val
            })

        # -------------------------
        # intent
        # -------------------------
        elif tgt.get("type") == "intent":

            outputs.append({
                "type": "intent",
                "intent_type": tgt.get("intent_type"),
                "field": tgt.get("field"),
                "value": val,  # 注意是 val（已经 scale 过）
                "source": cell.cell_id
            })

    return outputs

def evaluate_behaviors(node_state, hir_output, behaviors, graph=None, cell=None):

    # ✅ 先定义
    if isinstance(behaviors, dict):
        behavior_iter = behaviors.values()
    else:
        behavior_iter = behaviors

    # ✅ 再 debug
    print("\n[DEBUG] === ENTER behavior_engine ===")
    print("[DEBUG] node_state:", node_state)
    print("[DEBUG] HIR fate:", hir_output.get("fate"))
    print("[BEHAVIOR IDS]", [b.get("behavior_id") for b in behavior_iter])

    outputs = []
    fate = hir_output.get("fate", "normal")

    for b in behavior_iter:
        exec_group = b.get("execution_group", "normal")

        # 1️⃣ fate gating
        if fate == "dying" and exec_group != "fate_execution":
            continue

        # 2️⃣ gate
        if not eval_gate(node_state, b.get("gate")):
            continue

        # 3️⃣ drive
        if graph is not None:
            drive = build_drive_from_graph(node_state, b["behavior_id"], graph)
            if drive is None:
                continue
        else:
            drive = compute_drive(node_state, b.get("drive", {}))

        # 4️⃣ HIR
        drive = apply_hir(drive, b, hir_output)
        if cell is not None:
            b_id = b["behavior_id"]
            sens = cell.params.get("behavior", {}).get(b_id, {}).get("sensitivity", 1.0)
            drive *= sens
        if b["behavior_id"] == "baseline_consumption":
            stress = node_state.get("stress", 0.0)
            print(f"[DEBUG] {b['behavior_id']} stress={stress:.3f} drive={drive:.3f}")

        # 5️⃣ activation
        act_cfg = dict(b.get("activation", {}))
        act_cfg["behavior_id"] = b["behavior_id"]

        act = activate(drive, act_cfg, cell=cell)

        if act <= 0:
            continue

        # 6️⃣ output（支持多输出）
        results = build_outputs(b, act, drive, cell=cell)
        outputs.append({
            "behavior_id": b["behavior_id"],
            "activation": act,
            "drive": drive,
            "outputs": results
        })
        print("[DEBUG] checking behavior:", b.get("behavior_id"))
        print(f"[CELL TYPE] {cell.cell_type} → {b['behavior_id']}")
    return outputs
