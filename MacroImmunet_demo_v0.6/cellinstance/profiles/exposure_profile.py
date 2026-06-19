# cellinstance/profiles/exposure_profile.py


# =========================================
# Exposure Profile
# =========================================

class ExposureProfile:

    """
    outward exposure policy profile

    responsibilities:
        - define observable states
        - define exposure thresholds
        - define exposure mappings
        - support public visibility queries

    DOES NOT:
        - calculate runtime state
        - generate intents directly
        - write world state
    """

    def __init__(

        self,

        surface_rules=None,

        secretion_rules=None,

        danger_rules=None,

        visibility_rules=None
    ):

        # =================================
        # membrane / surface exposure
        # =================================

        self.surface_rules = (

            surface_rules or {}
        )

        # =================================
        # secreted signal exposure
        # =================================

        self.secretion_rules = (

            secretion_rules or {}
        )

        # =================================
        # danger exposure rules
        # =================================

        self.danger_rules = (

            danger_rules or {}
        )

        # =================================
        # visibility constraints
        # =================================

        self.visibility_rules = (

            visibility_rules or {}
        )

    # =====================================
    # get surface rules
    # =====================================

    def get_surface_rules(self):

        return self.surface_rules

    # =====================================
    # get secretion rules
    # =====================================

    def get_secretion_rules(self):

        return self.secretion_rules

    # =====================================
    # get danger rules
    # =====================================

    def get_danger_rules(self):

        return self.danger_rules

    # =====================================
    # export summary
    # =====================================

    def summary(self):

        return {

            "surface_rules":
                self.surface_rules,

            "secretion_rules":
                self.secretion_rules,

            "danger_rules":
                self.danger_rules,

            "visibility_rules":
                self.visibility_rules
        }
