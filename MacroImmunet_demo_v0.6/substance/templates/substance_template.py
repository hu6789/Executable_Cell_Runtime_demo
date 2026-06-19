# substance/templates/substance_template.py


class SubstanceTemplate:

    """
    Immutable substance definition.

    Loaded from json.

    Responsibilities:
        - identity definition
        - interaction rules
        - dynamics parameters
        - default values

    Does NOT:
        - store runtime state
        - perform interaction
        - perform world updates
    """

    def __init__(self, data):

        self.raw_data = data

        # =====================================
        # identity
        # =====================================

        identity = data.get(
            "identity",
            {}
        )

        self.template_id = data.get(
            "template_id"
        )

        self.substance_type = identity.get(
            "substance_type"
        )

        self.category = identity.get(
            "category"
        )

        self.species = identity.get(
            "species"
        )

        self.display_name = (

            data.get(
                "display_name"
            )

            or

            self.substance_type
        )

        # =====================================
        # runtime defaults
        # =====================================

        runtime_defaults = data.get(
            "runtime_defaults",
            {}
        )

        self.default_amount = (

            runtime_defaults.get(
                "default_amount",
                0.0
            )
        )

        self.active = (

            runtime_defaults.get(
                "active",
                True
            )
        )

        # =====================================
        # dynamics
        # =====================================

        self.dynamics = data.get(
            "dynamics",
            {}
        )

        # =====================================
        # interaction
        # =====================================

        interaction = data.get(
            "interaction",
            {}
        )

        self.interaction_mode = (

            interaction.get(
                "interaction_mode",
                "passive"
            )
        )

        self.interaction_rules = (

            interaction.get(
                "interaction_rules",
                []
            )
        )

        # =====================================
        # runtime params
        # =====================================

        self.runtime_params = data.get(
            "runtime_params",
            {}
        )

        # =====================================
        # metadata
        # =====================================

        self.metadata = data.get(
            "metadata",
            {}
        )

    # =====================================
    # helpers
    # =====================================

    @property
    def diffusion_radius(self):

        return self.dynamics.get(
            "diffusion_radius",
            0
        )

    @property
    def decay_rate(self):

        return self.dynamics.get(
            "decay_rate",
            0.0
        )

    # =====================================
    # summary
    # =====================================

    def summary(self):

        return {

            "template_id":
                self.template_id,

            "substance_type":
                self.substance_type,

            "category":
                self.category,

            "species":
                self.species,

            "default_amount":
                self.default_amount,

            "interaction_mode":
                self.interaction_mode,

            "interaction_rules":
                len(
                    self.interaction_rules
                ),

            "dynamics":
                self.dynamics
        }

    # =====================================
    # repr
    # =====================================

    def __repr__(self):

        return (

            f"SubstanceTemplate("
            f"type={self.substance_type}, "
            f"rules={len(self.interaction_rules)}"
            f")"
        )
