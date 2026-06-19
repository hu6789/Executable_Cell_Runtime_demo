# cellinstance/profiles/hir_profile.py


# =========================================
# HIR Profile
# =========================================

class HIRProfile:

    """
    homeostatic / integrity regulation profile

    responsibilities:
        - define physiological limits
        - define stress thresholds
        - define fate transition boundaries
        - define behavior suppression policies

    DOES NOT:
        - execute HIR logic
        - mutate runtime state
        - generate intents directly
    """

    def __init__(

        self,

        stress_thresholds=None,

        damage_thresholds=None,

        exhaustion_rules=None,

        suppression_rules=None,

        fate_rules=None
    ):

        # =================================
        # stress thresholds
        # =================================

        self.stress_thresholds = (

            stress_thresholds or {}
        )

        # =================================
        # damage thresholds
        # =================================

        self.damage_thresholds = (

            damage_thresholds or {}
        )

        # =================================
        # exhaustion / dysfunction
        # =================================

        self.exhaustion_rules = (

            exhaustion_rules or {}
        )

        # =================================
        # behavior suppression policies
        # =================================

        self.suppression_rules = (

            suppression_rules or {}
        )

        # =================================
        # fate transition rules
        # =================================

        self.fate_rules = (

            fate_rules or {}
        )

    # =====================================
    # get stress threshold
    # =====================================

    def get_stress_threshold(

        self,
        key,
        default=None
    ):

        return self.stress_thresholds.get(

            key,
            default
        )

    # =====================================
    # get damage threshold
    # =====================================

    def get_damage_threshold(

        self,
        key,
        default=None
    ):

        return self.damage_thresholds.get(

            key,
            default
        )

    # =====================================
    # export summary
    # =====================================

    def summary(self):

        return {

            "stress_thresholds":
                self.stress_thresholds,

            "damage_thresholds":
                self.damage_thresholds,

            "exhaustion_rules":
                self.exhaustion_rules,

            "suppression_rules":
                self.suppression_rules,

            "fate_rules":
                self.fate_rules
        }
