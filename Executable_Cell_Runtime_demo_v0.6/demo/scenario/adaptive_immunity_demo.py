# demo/scenario/adaptive_immunity_demo.py

from demo.scenario.base_scenario import BaseScenario


class AdaptiveImmunityDemo(BaseScenario):

    def __init__(self):

        super().__init__()

        self.name = "Adaptive Immunity Demo"

    def build(self, builder):

        # =====================================
        # Host Cell
        # pre-loaded antigen presentation
        # =====================================

        builder.add_cell(

            template_id="host_cell",

            cell_id="host_001",

            position=(7, 6),

            runtime_state={

                "ATP": 100,
                "ROS": 0,

                # directly present antigen


            }

        )
        
        builder.add_field(

            field_name="influenza",

            values={

                (7,6):100.0

            }

        )
        

        # =====================================
        # CD4 T Cell
        # =====================================

        builder.add_cell(

            template_id="cd4_t_cell",

            cell_id="cd4_001",

            position=(7, 7),

            runtime_state={

                "ATP": 100

            }

        )


        # =====================================
        # CD8 T Cell
        # =====================================

        builder.add_cell(

            template_id="cd8_t_cell",

            cell_id="cd8_001",

            position=(6, 6),

            runtime_state={

                "ATP": 100

            }

        )

        # =====================================
        # metadata
        # =====================================

        builder.metadata(

            name=self.name,

            description=(
                "Adaptive immune response demo: "
                "Host antigen presentation activates CD4, "
                "CD4 secretes IL2, "
                "IL2 activates CD8, "
                "CD8 releases perforin to damage the host."
            ),

            version="0.6"

        )

    def runtime_options(self):

        return {

            "ticks": 25,

            "enable_console": True

        }
