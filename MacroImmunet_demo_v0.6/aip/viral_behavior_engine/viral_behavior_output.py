# aip/viral_behavior_engine/behavior_output.py

# =========================================
# Viral Behavior Output Builder (REVISED)
# =========================================

def build_viral_behavior_output(
    viral_context,
    behavior_results,
    cycle_state,
    resource_usage,
    competition_result=None
):
    """
    responsibilities:

        - aggregate viral behavior execution trace
        - generate modulation_runtime_state (PRIMARY OUTPUT)
        - provide lightweight summary for debugging

    DOES NOT:

        - perform gating decisions
        - execute behaviors
        - modify runtime state directly
    """

    # =====================================
    # 1. behavior trace (debug layer)
    # =====================================

    behavior_trace = {}

    total_activity = 0.0
    total_damage = 0.0

    for behavior_name, result in behavior_results.items():

        behavior_trace[behavior_name] = {
            "drive": result.get("scaled_drive", 0.0),
            "damage": result.get("damage", 0.0),
            "resource_cost": result.get("resource_cost", {})
        }

        total_activity += result.get("scaled_drive", 0.0)
        total_damage += result.get("damage", 0.0)

    # =====================================
    # 2. modulation_runtime_state (CORE OUTPUT)
    # =====================================

    modulation_runtime_state = {

        # cycle pressure
        "viral_cycle_state": cycle_state,

        # behavior influence layer
        "behavior_modulations": {
            name: {
                "multiply": res.get("scaled_drive", 0.0),
                "sources": ["viral_behavior"]
            }
            for name, res in behavior_results.items()
        },

        # resource pressure projection (viral proxy, NOT host ATP truth)
        "resource_modulations": {
            "ATP": resource_usage.get("ATP", 0.0),
            "ribosome": resource_usage.get("ribosome", 0.0),
            "ER": resource_usage.get("ER", 0.0),
            "membrane": resource_usage.get("membrane", 0.0)
        },

        # structural stress projection
        "hir_modulations": {
            "infection_pressure": total_damage,
            "viral_load_proxy": total_activity
        }
    }

    # =====================================
    # 3. lightweight summary
    # =====================================

    output = {
        "modulation_runtime_state": modulation_runtime_state,

        "viral_trace": {
            "total_activity": total_activity,
            "total_damage": total_damage
        },

        "behavior_trace": behavior_trace
    }

    # =====================================
    # optional competition snapshot
    # =====================================

    if competition_result:
        output["competition_snapshot"] = competition_result

    return output
