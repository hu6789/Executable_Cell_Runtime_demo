# aip/viral_behavior_engine/viral_to_modulation_adapter.py

# =========================================
# Viral → Modulation Contribution Adapter
# =========================================

"""
Purpose:

    Convert viral behavior execution results
    into modulation contributions ONLY.

Position in pipeline:

    viral_behavior_engine
            ↓
    modulation_contribution (THIS MODULE)
            ↓
    modulation_aggregate.py
            ↓
    build_modulation_runtime_state()

Key rule:

    This module MUST NOT construct
    modulation_runtime_state directly.

It only emits "modulation intent signals".
"""

# =========================================
# Main Entry
# =========================================

def build_viral_modulation_contribution(
    viral_output,
    viral_context=None
):
    """
    Convert viral behavior output into
    modulation contribution format.
    """

    if not viral_output:
        return {
            "modulations": {},
            "payloads": []
        }

    behavior_trace = viral_output.get("behavior_trace", {})
    cycle_state = viral_output.get("modulation_runtime_state", {}).get(
        "viral_cycle_state", None
    )

    # =====================================
    # modulation container (core output)
    # =====================================

    modulations = {}
    payloads = []

    # =====================================
    # 1. behavior → modulation mapping
    # =====================================

    for behavior_name, trace in behavior_trace.items():

        drive = trace.get("drive", 0.0)
        damage = trace.get("damage", 0.0)

        modulations[f"behavior:{behavior_name}"] = {

            "multiply": drive,

            "add": 0.0,

            "override": None,

            "sources": [
                "viral_behavior_engine"
            ],

            # abstract signal only
            "signals": {
                "damage_pressure": damage
            }
        }

    # =====================================
    # 2. global viral pressure
    # =====================================

    total_activity = viral_output.get(
        "viral_trace", {}
    ).get("total_activity", 0.0)

    total_damage = viral_output.get(
        "viral_trace", {}
    ).get("total_damage", 0.0)

    modulations["global:viral_pressure"] = {

        "multiply": min(total_activity, 1.0),

        "add": 0.0,

        "override": None,

        "sources": ["viral_behavior_engine"],

        "signals": {
            "total_damage": total_damage,
            "cycle_state": cycle_state
        }
    }

    # =====================================
    # 3. resource pressure (abstract only)
    # =====================================

    resource_snapshot = viral_output.get(
        "modulation_runtime_state", {}
    ).get("resource_modulations", {})

    if resource_snapshot:

        modulations["global:resource_pressure"] = {

            "multiply": 0.5,

            "add": 0.0,

            "override": None,

            "sources": ["viral_behavior_engine"],

            "signals": resource_snapshot
        }

    # =====================================
    # 4. optional viral payloads (external effects)
    # =====================================

    behavior_contributions = viral_output.get(
        "behavior_trace", {}
    )

    for name, trace in behavior_contributions.items():

        # only pass "external intent-like effects"
        if trace.get("resource_cost"):

            payloads.append({
                "type": "viral_behavior_payload",
                "behavior": name,
                "resource_cost": trace["resource_cost"]
            })

    # =====================================
    # final output (CONTRIBUTION ONLY)
    # =====================================

    return {

        "modulations": modulations,
        "payloads": payloads,

        "meta": {
            "source": "viral_behavior_engine",
            "cycle_state": cycle_state
        }
    }
