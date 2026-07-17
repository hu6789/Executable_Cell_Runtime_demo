# aip/viral_behavior_engine/viral_to_skeleton_adapter.py

"""
Viral → Skeleton Adapter

purpose:
    translate viral semantics
    into behavior_skeleton-compatible inputs

IMPORTANT:
    - does NOT execute behavior
    - does NOT perform gating
    - does NOT mutate runtime state

this is PURE representation mapping layer
"""

# =========================================
# Viral → Skeleton Input Builder
# =========================================

def build_viral_skeleton_inputs(
    behavior_name,
    behavior_def,
    viral_context,
    competition_context,
    viral_cycle_state=None   # 加这一行
):

    # =========================
    # SAFE FLAT LOOKUP
    # =========================

    competition_weight = 1.0

    comp = competition_context.get("competition", {})

    if isinstance(comp, dict):
        # flat style
        if behavior_name in comp:
            competition_weight = comp[behavior_name].get(
                "competition_weight",
                1.0
            )
        else:
            # fallback scan
            for _, v in comp.items():
                if isinstance(v, dict) and behavior_name in v:
                    competition_weight = v[behavior_name].get(
                        "competition_weight",
                        1.0
                    )
                    break

    # =========================
    # viral bias
    # =========================

    viral_bias = behavior_def.get("viral_resource_bias", {})

    ribosome_boost = viral_bias.get("ribosome_priority", 1.0)

    amplification = ribosome_boost * competition_weight

    activation = competition_weight

    suppression = 0.0

    resource = viral_context.get(
        "resource_projection", {}
    )

    resource_value = sum(resource.values()) / max(len(resource), 1)

    stabilization = viral_context.get("stabilization_proxy", 0.7)

    destabilization = viral_bias.get("destabilization_bias", 0.0)

    damage = viral_context.get("damage_proxy", 0.0)

    return {
        "activation": activation,
        "suppression": suppression,
        "amplification": amplification,
        "resource": resource_value,
        "damage": damage,
        "stabilization": stabilization,
        "destabilization": destabilization
    }
