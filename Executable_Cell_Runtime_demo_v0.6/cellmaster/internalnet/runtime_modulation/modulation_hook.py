# cellmaster/internalnet/runtime_modulation/modulation_hook.py


# =========================================
# Runtime Modulation Hook Base
# =========================================

class RuntimeModulationHook:

    """
    base modulation hook interface

    responsibilities:
        - provide unified hook API
        - define modulation contract
        - expose hook metadata

    hook output may include:
        - node modulation
        - passive modulation
        - runtime gate override
        - behavior bias
        - external stress/resource effects

    DOES NOT:
        - directly write runtime state
        - directly modify world
        - bypass HIR
    """

    def __init__(

        self,

        hook_name,
        hook_type="generic",
        priority=0,
        enabled=True
    ):

        self.hook_name = hook_name

        self.hook_type = hook_type

        self.priority = priority

        self.enabled = enabled

    # =====================================
    # hook applicability
    # =====================================

    def supports(
        self,
        runtime_entity
    ):

        """
        whether this hook
        supports current entity

        override in subclass
        """

        return True

    # =====================================
    # runtime apply
    # =====================================

    def apply(
        self,
        modulation_context
    ):

        """
        execute modulation

        MUST return:
            - dict
            - list[dict]
            - None

        override in subclass
        """

        raise NotImplementedError

    # =====================================
    # hook metadata
    # =====================================

    def export_metadata(self):

        return {

            "hook_name":
                self.hook_name,

            "hook_type":
                self.hook_type,

            "priority":
                self.priority,

            "enabled":
                self.enabled
        }
