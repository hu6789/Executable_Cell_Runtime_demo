# Cell_master/Internalnet/passive_engine.py

import os
import json

def _get_val(x):
    if isinstance(x, dict):
        return x.get("value")
    return x
# =========================
# load passive definitions
# =========================
def load_passives():
    base_dir = os.path.dirname(__file__)
    passive_dir = os.path.join(base_dir, "passive")

    passives = []

    for file in sorted(os.listdir(passive_dir)): 
        if not file.endswith(".json"):
            continue

        path = os.path.join(passive_dir, file)

        with open(path) as f:
            data = json.load(f)

            print("[DEBUG] loading passive:", file, "→", type(data))

            passives.append(data)

    # ✅ 兼容 priority 写法（int / dict）
    def get_priority(p):
        pr = p.get("priority", 0)
        if isinstance(pr, dict):
            return pr.get("value", 0)
        return pr

    passives.sort(key=get_priority, reverse=True)

    # 🔥 防御性检查（关键）
    if passives is None:
        print("[ERROR] passives is None!")
        return []

    return passives
def _get_priority(p):

    pr = p.get("priority", 0)

    if isinstance(pr, dict):
        pr = pr.get("value", 0)

    if not isinstance(pr, (int, float)):
        return 0

    return pr   # ✅


# =========================
# gate evaluation
# =========================
def check_gate(node_state, gate):

    conditions = gate.get("conditions", [])
    logic = gate.get("logic", "all")

    results = []

    for cond in conditions:

        node = cond["node"]
        op = cond["op"]
        val = cond["value"]

        node_val = node_state.get(node, 0.0)

        if op == ">":
            results.append(node_val > val)
        elif op == "<":
            results.append(node_val < val)
        elif op == ">=":
            results.append(node_val >= val)
        elif op == "<=":
            results.append(node_val <= val)
        elif op == "==":
            results.append(node_val == val)
        else:
            results.append(True)

    if logic == "all":
        return all(results)
    elif logic == "any":
        return any(results)

    return True


# =========================
# compute expression
# =========================
def compute_value(node_state, compute_def):

    expr = compute_def.get("expression", "")
    params = compute_def.get("params", {})

    # 🔥 构造局部变量
    local_vars = dict(node_state)
    local_vars.update(params)

    try:
        safe_env = {
            "__builtins__": {},
            "min": min,
            "max": max,
            "abs": abs
        }

        value = eval(expr, safe_env, local_vars)
    except Exception:
        value = 0.0

    return value


# =========================
# apply updates
# =========================
def apply_update(node_state, update_def, computed_value):

    targets = update_def.get("targets", [])

    for tgt in targets:

        node = tgt["node"]
        mode = tgt.get("mode", "add")

        # value来源
        if tgt.get("value_from") == "compute":
            val = computed_value
        else:
            val = tgt.get("value", 0.0)

        # scale
        scale = tgt.get("scale", 1.0)
        val *= scale

        if mode == "add":
            node_state[node] = node_state.get(node, 0.0) + val
        elif mode == "set":
            node_state[node] = val

    return node_state


# =========================
# run passive engine
# =========================
def run_passive_engine(node_state, passive_defs):

    delta = {}
    passive_logs = []

    for passive in passive_defs:

        gate = passive.get("gate")
        if gate and not check_gate(node_state, gate):
            continue

        compute_def = passive.get("compute", {})
        value = compute_value(node_state, compute_def)

        update_def = passive.get("update", {})

        targets = update_def.get("targets", [])

        for tgt in targets:

            node = tgt["node"]
            mode = tgt.get("mode", "add")

            # value来源
            if tgt.get("value_from") == "compute":
                val = value
            else:
                val = tgt.get("value", 0.0)

            # scale
            scale = tgt.get("scale", 1.0)
            val *= scale

            # ❗关键：只记录 delta，不改 state
            if mode == "add":
                d = val
            elif mode == "set":
                # set 很 tricky，这里转成 delta（近似）
                prev = node_state.get(node, 0.0)
                d = val - prev
            else:
                d = 0.0

            delta[node] = delta.get(node, 0.0) + d

            passive_logs.append({
                "passive": passive.get("passive_id", "unknown"),
                "node": node,
                "delta": d
            })

    return delta, passive_logs
