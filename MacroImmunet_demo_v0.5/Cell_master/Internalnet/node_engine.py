# Cell_master/Internalnet/node_engine.py

import os
import json


# =========================
# load node definitions
# =========================
def load_nodes():
    import os, json

    base_dir = os.path.dirname(__file__)
    node_dir = os.path.join(base_dir, "node")

    nodes = []

    for f in os.listdir(node_dir):
        if not f.endswith(".json"):
            continue

        path = os.path.join(node_dir, f)

        with open(path) as file:
            data = json.load(file)

            # ✅ 如果没有 node_id，就自动补
            if "node_id" not in data:
                data["node_id"] = f.replace(".json", "")

            nodes.append(data)

    return nodes

# =========================
# build graph inputs map
# =========================
def build_inputs_map(graph):

    inputs_map = {}

    for edge in graph.get("edges", []):

        if edge.get("type") != "node-node":
            continue

        tgt = edge["target"]

        inputs_map.setdefault(tgt, []).append(edge)

    return inputs_map


# =========================
# gate evaluation
# =========================
def check_gate(value, gate):

    # 新结构
    if "conditions" in gate:
        results = []

        for cond in gate["conditions"]:
            op = cond.get("op")
            threshold = cond.get("value")

            if op == ">":
                results.append(value > threshold)
            elif op == "<":
                results.append(value < threshold)
            elif op == ">=":
                results.append(value >= threshold)
            elif op == "<=":
                results.append(value <= threshold)
            elif op == "==":
                results.append(value == threshold)
            else:
                results.append(True)

        logic = gate.get("logic", "all")

        if logic == "all":
            return all(results)
        elif logic == "any":
            return any(results)

        return True

    # 老结构 fallback
    op = gate.get("op")
    threshold = gate.get("value")

    if op == ">":
        return value > threshold
    elif op == "<":
        return value < threshold
    elif op == ">=":
        return value >= threshold
    elif op == "<=":
        return value <= threshold
    elif op == "==":
        return value == threshold

    return True

# =========================
# resolve update order（先简单版）
# =========================
def resolve_update_order(graph):
    nodes = graph.get("nodes", [])

    if isinstance(nodes, list):
        return nodes
    elif isinstance(nodes, dict):
        return list(nodes.keys())

    return []

# =========================
# core node update
# =========================
def run_node_graph(node_state, graph, node_defs, node_input):
    """
    核心节点更新函数
    - node_state: 上一轮节点状态 dict，可为 None
    - graph: 节点图结构，包含 edges
    - node_defs: 所有节点定义 dict
    - node_input: 外部输入 dict
    """
    # =========================
    # 0️⃣ 初始化 current
    # =========================
    # 先给所有节点赋初值 0.0
    current = {node: 0.0 for node in node_defs.keys()}
    
    # 继承上一轮状态
    if node_state:
        current.update(node_state)
    
    # =========================
    # 1️⃣ 注入 external input
    # =========================
    for k, v in node_input.items():
        node_def = node_defs.get(k, {})
        mode = node_def.get("update_rule", {}).get("type")
        if mode == "direct_input":
            current[k] = v  # 覆盖
        else:
            current[k] += v  # 累加，保证节点已初始化

    # =========================
    # 2️⃣ 构建 graph 结构
    # =========================
    inputs_map = build_inputs_map(graph)
    update_order = resolve_update_order(graph)

    # =========================
    # 3️⃣ 节点更新（graph propagation）
    # =========================
    for node in update_order:
        node_def = node_defs.get(node)
        if not node_def:
            continue

        update_rule = node_def.get("update_rule", {})
        mode = update_rule.get("type", "weighted_sum")

        # external_only / direct_input 已经在外部处理
        if mode in ["external_only", "direct_input"]:
            continue

        # graph propagation
        inputs = inputs_map.get(node, [])
        val = 0.0

        for edge in inputs:
            src = edge["source"]
            weight = edge.get("weight", 1.0)
            src_val = current.get(src, 0.0)

            gate = edge.get("gate")
            if gate and not check_gate(src_val, gate):
                continue

            val += src_val * weight

        # clamp
        clamp = node_def.get("clamp", {})
        if clamp.get("enabled"):
            min_v = clamp.get("min", 0.0)
            max_v = clamp.get("max", 1.0)
            val = max(min_v, min(max_v, val))

        if inputs:
            current[node] += val

    # =========================
    # 4️⃣ decay（统一在最后）
    # =========================
    for node, node_def in node_defs.items():

        update_rule = node_def.get("update_rule", {}).get("type")

        decay_def = node_def.get("decay", {})
        if not decay_def.get("enabled"):
            continue

        tau = decay_def.get("tau", 1.0)
        val = current.get(node, 0.0)
        val *= (1.0 - 1.0 / tau)
        current[node] = val

    return current, update_order
# =========================
# emitter（node → external）
# =========================
def collect_emitters(node_state, node_defs):

    emitted = {}

    for node_id, node_def in node_defs.items():

        io = node_def.get("io", {})
        output = io.get("output", {})

        if not output.get("emit_external"):
            continue

        key = node_def.get("external_key")
        if not key:
            continue

        value = node_state.get(node_id, 0.0)

        if value > 0:
            emitted[key] = emitted.get(key, 0.0) + value

    return emitted
