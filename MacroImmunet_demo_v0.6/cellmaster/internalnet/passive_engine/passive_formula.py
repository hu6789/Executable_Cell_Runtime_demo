# cellmaster/internalnet/passive_engine/passive_formula.py

import math


# =========================================
# Passive Formula Runtime
# =========================================

def compute_passive_formula(
    passive_definition,
    runtime_context
):
    """
    compute fixed physiological dynamics

    responsibilities:
        - resolve symbolic node references
        - compute deterministic biological effects
        - apply formula type dispatch

    DOES NOT:
        - modify runtime state
        - apply transform
    """

    formula = passive_definition.get("formula", {}) or {}
    f_type = formula.get("type")

    nodes = passive_definition.get("involved_nodes", []) or []
    state = runtime_context.get("runtime_state", {}) or {}

    node_values = {n: state.get(n, 0.0) for n in nodes}

    # =====================================
    # linear_decay
    # =====================================
    if f_type == "linear_decay":
        src = formula.get("source")
        rate = formula.get("decay_rate", 0.01)
        return -node_values.get(src, 0.0) * rate

    # =====================================
    # leakage
    # =====================================
    if f_type == "proportional_leakage":
        src = formula.get("source", "source")
        inst = formula.get("instability_source", "instability")
        rate = formula.get("leakage_rate", 0.01)

        return -node_values.get(src, 0.0) * node_values.get(inst, 1.0) * rate

    # =====================================
    # exponential
    # =====================================
    if f_type == "exponential_accumulation":
        src = formula.get("source", "source")
        g = formula.get("growth_rate", 0.05)

        return math.exp(node_values.get(src, 0.0) * g) - 1.0

    # =====================================
    # resource
    # =====================================
    if f_type == "resource_consumption":
        act = node_values.get("activity", 0.0)
        load = node_values.get("load", 1.0)
        rate = formula.get("consumption_rate", 0.1)

        return -act * load * rate

    # =====================================
    # membrane
    # =====================================
    if f_type == "membrane_instability":

        stress_node = formula.get(
            "stress",
            "stress"
        )

        repair_node = formula.get(
            "repair",
            "repair"
        )

        stress = node_values.get(
            stress_node,
            0.0
        )

        repair = node_values.get(
            repair_node,
            0.0
        )

        k = formula.get(
            "instability_factor",
            0.05
        )

        return (
            stress - repair
        ) * k
        
    # =====================================
    # Ca
    # =====================================
    if f_type == "calcium_influx":

        membrane = node_values.get(
            formula.get(
                "source",
                "cell_membrane"
            ),
            0.0
        )

        rate = formula.get(
            "flux_rate",
            0.05
        )

        max_integrity = formula.get(
            "max_integrity",
            100.0
        )

        damage = max(
 
            0.0,

            max_integrity
            - membrane
        )

        return damage * rate
    return 0.0
