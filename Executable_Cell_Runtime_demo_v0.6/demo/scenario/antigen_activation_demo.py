# demo/scenario/antigen_activation_demo.py

"""
=========================================================
Antigen Activation Demo
=========================================================

Minimal demo:

pMHC field
    ↓
CD4 activation
    ↓
IL2 production
    ↓
IL2 secretion
"""

from demo.scenario.base_scenario import BaseScenario


class AntigenActivationDemo(BaseScenario):

    def __init__(self):

        super().__init__()

        self.name = "Antigen Activation Demo"

    def build(self, builder):

        #
        # CD4
        #

        builder.add_cell(

            template_id="cd4_t_cell",

            cell_id="cd4_001",

            position=(0, 0),

            runtime_state={

                "ATP":100,

                "ROS":5,

                "TCR":20,

                "IL2":0,

                "IL2R":20,

                "CXCR3":20
            }
        )

        #
        # pMHC field
        #

        builder.add_field(

            field_name="pMHC",

            values={

                (0,0):1.0

            }

        )

        builder.metadata(

            name=self.name,

            description="pMHC activates CD4.",

            version="0.7"
        )

    def runtime_options(self):

        return {

            "ticks":5,

            "enable_console":True
        }
