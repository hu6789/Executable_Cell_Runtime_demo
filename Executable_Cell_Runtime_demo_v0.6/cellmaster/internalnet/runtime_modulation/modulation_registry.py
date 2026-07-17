# cellmaster/internalnet/runtime_modulation/modulation_registry.py

from cellmaster.internalnet.runtime_modulation.modulation_hook import (
    RuntimeModulationHook
)


# =========================================
# Runtime Modulation Registry
# =========================================

class RuntimeModulationRegistry:

    """
    modulation hook registry

    responsibilities:
        - register runtime hooks
        - organize hook execution order
        - provide hook lookup
        - filter unsupported hooks

    DOES NOT:
        - execute modulation logic
        - mutate runtime state
    """

    def __init__(self):

        self.hooks = []

    # =====================================
    # register hook
    # =====================================

    def register_hook(
        self,
        hook
    ):

        if not isinstance(
            hook,
            RuntimeModulationHook
        ):

            raise TypeError(

                "hook must inherit "
                "RuntimeModulationHook"
            )

        self.hooks.append(
            hook
        )

        self.sort_hooks()

    # =====================================
    # sort hooks by priority
    # =====================================

    def sort_hooks(self):

        self.hooks.sort(

            key=lambda h:
                h.priority,

            reverse=True
        )

    # =====================================
    # runtime-compatible hooks
    # =====================================

    def get_runtime_hooks(
        self,
        runtime_entity
    ):

        compatible = []

        for hook in self.hooks:

            if not hook.enabled:

                continue

            if not hook.supports(
                runtime_entity
            ):

                continue

            compatible.append(
                hook
            )

        return compatible

    # =====================================
    # export registry snapshot
    # =====================================

    def export_registry_snapshot(
        self
    ):

        snapshot = []

        for hook in self.hooks:

            snapshot.append(

                hook.export_metadata()
            )

        return snapshot
