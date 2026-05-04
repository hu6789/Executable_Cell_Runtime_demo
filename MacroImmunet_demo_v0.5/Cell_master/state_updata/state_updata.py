# Internalnet/state_update.py
# Internalnet/state_update.py

def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


# =========================
# 1️⃣ 收集 delta（恢复完整实现）
# =========================
def collect_deltas(behavior_outputs, node_defs):

    delta = {}

    for b in behavior_outputs:

        outputs = b.get("outputs", [])

        for out in outputs:

            if out.get("type") != "internal_state":
                continue

            node = out.get("node")
            if not node:
                continue

            node_def = node_defs.get(node, {})
            writable = node_def.get("writable_by", [])

            if "behavior" not in writable:
                continue

            val = out.get("value", 0.0)
            intensity = b.get("activation", 1.0)

            delta[node] = delta.get(node, 0.0) + val * intensity

    return delta


# =========================
# 2️⃣ dynamics 更新（唯一版本）
# =========================
def apply_dynamics(node_state, delta, node_defs):

    new_state = {}

    for node_id, node_def in node_defs.items():

        prev = node_state.get(node_id, 0.0)
        d = delta.get(node_id, 0.0)

        dyn = node_def.get("state_dynamics", {})
        mode = dyn.get("type", "instant")

        if mode == "instant":
            val = prev + d

        elif mode == "accumulative":
            decay = dyn.get("decay", 0.99)
            val = prev * decay + d

        elif mode == "leaky":
            decay = dyn.get("decay", 1.0)
            baseline = dyn.get("baseline", 0.0)
            val = prev * decay + (1 - decay) * baseline + d

        elif mode == "switch":
            threshold = dyn.get("threshold", 0.5)
            val = 1.0 if (prev + d) > threshold else 0.0

        else:
            val = prev + d

        val = clamp(val)
        new_state[node_id] = val

    return new_state


# =========================
# 3️⃣ 唯一对外入口
# =========================
def compute_state_update(node_state, behavior_outputs, node_defs):

    delta = collect_deltas(behavior_outputs, node_defs)
    new_state = apply_dynamics(node_state, delta, node_defs)

    return delta, new_state
