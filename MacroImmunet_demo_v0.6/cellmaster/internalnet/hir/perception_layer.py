# cellmaster/internalnet/hir/perception_layer.py

from copy import deepcopy


def build_perceived_context(global_context, deception_delta):
    perceived = global_context.copy()

    if not deception_delta:
        return perceived

    # mask signals
    for s in deception_delta.get("masked_signals", []):
        if s in perceived:
            perceived[s] = perceived[s] * 0.5

    # fake resources
    fake = deception_delta.get("fake_resource_map", {})
    if "resource_pool" in perceived:
        perceived["resource_pool"].update(fake)

    # hide infection
    if "infection_hidden" in deception_delta.get("override_flags", []):
        perceived["infection_visible"] = False

    return perceived
