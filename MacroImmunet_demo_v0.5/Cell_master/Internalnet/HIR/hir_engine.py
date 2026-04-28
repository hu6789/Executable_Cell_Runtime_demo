# Internalnet/HIR/hir_engine.py

import json
import math


# =========================
# utils
# =========================

def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


def eval_formula(expr, context):
    try:
        return eval(expr, {}, context)
    except Exception:
        return 0.0


def check_condition(cond, features):
    node = cond["node"]
    op = cond["op"]
    val = cond["value"]

    x = features.get(node, 0.0)

    if op == ">":
        return x > val
    elif op == "<":
        return x < val
    elif op == ">=":
        return x >= val
    elif op == "<=":
        return x <= val
    elif op == "==":
        return x == val
    return False


# =========================
# 1️⃣ build features
# =========================

def build_features(node_state, cfg):
    features = {}

    for k, v in cfg["features"].items():
        if isinstance(v, str):
            features[k] = node_state.get(v, 0.0)
        else:
            features[k] = 0.0

    return features


# =========================
# 2️⃣ fate evaluation
# =========================

def compute_fate(features, cfg):

    # 👉 priority: condition-based fate（如 perforin）
    for name, rule in cfg["fates"].items():

        if "conditions" in rule:
            results = [
                check_condition(c, features)
                for c in rule["conditions"]
            ]

            logic = rule.get("logic", "all")

            if (logic == "all" and all(results)) or \
               (logic == "any" and any(results)):
                return name, {}

    # 👉 score-based fate
    scores = {}

    for name, rule in cfg["fates"].items():
        weights = rule.get("weights")
        if not weights:
            continue

        val = 0.0
        for k, w in weights.items():
            val += w * features.get(k, 0.0)

        scores[name] = clamp(val)

    # 👉 threshold decision
    for name, rule in cfg["fates"].items():
        th = rule.get("thresholds")
        if not th:
            continue

        ok = True

        if "score" in th:
            ok &= scores.get(name, 0.0) > th["score"]

        for k, v in th.items():
            if k == "score":
                continue
            ok &= features.get(k, 0.0) > v

        if ok:
            return name, scores

    return "normal", scores


# =========================
# 3️⃣ group modifiers
# =========================

def compute_groups(features, cfg):
    groups = {}

    for name, rule in cfg["groups"].items():
        val = eval_formula(rule["formula"], features)
        val = clamp(val)

        val = max(rule.get("min", 0.0), val)

        groups[name] = val

    return groups


# =========================
# 4️⃣ blocks
# =========================

def compute_blocks(features, fate, cfg):
    blocks = {}

    context = dict(features)
    context["fate"] = fate

    for rule in cfg["blocks"]:
        cond = rule["if"]

        try:
            if eval(cond, {}, context):
                for g in rule["disable"]:
                    blocks[g] = True
        except:
            pass

    return blocks


# =========================
# 主入口
# =========================

def run_hir(node_state, hir_cfg):

    features = build_features(node_state, hir_cfg)

    fate, scores = compute_fate(features, hir_cfg)

    group_modifiers = compute_groups(features, hir_cfg)

    blocks = compute_blocks(features, fate, hir_cfg)

    return {
        "fate": fate,
        "scores": scores,
        "group_modifiers": group_modifiers,
        "blocks": blocks,
        "features": features
    }
