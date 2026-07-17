# cellmaster/internalnet/passive_engine/passive_gate.py


# =========================================
# Passive Activation Gate
# =========================================

def evaluate_passive_gate(
    passive_definition,
    runtime_context
):
    """
    evaluate whether passive process
    is active in current tick

    responsibilities:
        - check required nodes existence/value
        - check minimum thresholds
        - support label gating (future-ready)

    DOES NOT:
        - compute physics
        - modify runtime state
    """
    gate = passive_definition.get("passive_gate", {}) or {}
    state = runtime_context.get("runtime_state", {}) or {}
    labels = runtime_context.get("labels", []) or []

    # =====================================
    # no gate → pass
    # =====================================
    if not gate:
        return {
            "passed": True,
            "reason": "no_gate"
        }

    # =====================================
    # required nodes
    # =====================================
    required_nodes = gate.get("required_nodes", [])

    for node in required_nodes:
        if state.get(node, 0.0) <= 0.0:
            return {
                "passed": False,
                "reason": f"missing_or_zero_node:{node}"
            }

    # =====================================
    # minimum value
    # =====================================
    min_v = gate.get("minimum_value", None)

    if min_v is not None and required_nodes:
        node = required_nodes[0]
        if state.get(node, 0.0) < min_v:
            return {
                "passed": False,
                "reason": f"below_minimum:{node}"
            }

    # =====================================
    # labels
    # =====================================
    for r in gate.get("required_labels", []):
        if r not in labels:
            return {
                "passed": False,
                "reason": f"missing_label:{r}"
            }

    for b in gate.get("blocked_labels", []):
        if b in labels:
            return {
                "passed": False,
                "reason": f"blocked_label:{b}"
            }

    return {
        "passed": True,
        "reason": "passed"
    }
