# aip/viral_behavior_engine/behavior_output.py

# =========================================
# Viral Behavior Output Builder (MODULATION-ALIGNED)
# =========================================

def build_viral_behavior_output(
    viral_context,
    behavior_results,
    cycle_state,
    resource_usage,
    competition_result=None
):

    behavior_modulations = {}
    global_modulations = {}

    total_activity = 0.0
    total_damage = 0.0

    # =====================================
    # behavior-level modulation mapping
    # =====================================

    for behavior_name, result in behavior_results.items():

        raw_drive = result.get("raw_drive", 0.0)
        scaled_drive = result.get("scaled_drive", raw_drive)

        behavior_modulations[behavior_name] = {

            # 🔥 关键：drive → modulation strength
            "multiply": scaled_drive,

            # optional semantic enrichment
            "add": 0.0,
            "override": None,
            "blocked": False,

            "sources": [
                "viral_behavior",
                behavior_name
            ]
        }

        total_activity += scaled_drive
        total_damage += result.get("damage", 0.0)

    # =====================================
    # resource modulation（真正关键修复）
    # =====================================

    resource_modulations = {}

    for k, v in resource_usage.items():
        resource_modulations[k] = {
            "multiply": 1.0 - min(v, 1.0),
            "sources": ["viral_resource_proxy"]
        }

    # =====================================
    # global modulation (viral pressure field)
    # =====================================

    global_modulations = {
        "viral_activity_pressure": {
            "add": total_activity,
            "sources": ["viral_activity"]
        },
        "viral_damage_pressure": {
            "add": total_damage,
            "sources": ["viral_damage"]
        }
    }

    # =====================================
    # CORE OUTPUT
    # =====================================

    modulation_runtime_state = {

        "viral_cycle_state": cycle_state,

        "behavior_modulations": behavior_modulations,

        "resource_modulations": resource_modulations,

        "global_modulations": global_modulations,

        "node_modulations": {},
        "passive_modulations": {},
        "hir_modulations": {},

        "payloads": []
    }

    return {
        "modulation_runtime_state": modulation_runtime_state,

        "viral_trace": {
            "total_activity": total_activity,
            "total_damage": total_damage
        }
    }
