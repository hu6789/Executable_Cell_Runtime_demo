# demo/scenario/cd4_il2_demo.py

"""
=========================================================
Infection Demo Scenario
=========================================================

Minimal infection scenario for MacroImmunet Demo.
"""

from demo.scenario.base_scenario import (
    BaseScenario
)


class InfectionDemo(BaseScenario):

    """
    Minimal influenza infection demo.
    """

    def __init__(self):

        super().__init__()

        self.name = "Minimal Infection Demo"

    # =====================================================
    # Build Scenario
    # =====================================================

    def build(
        self,
        builder
    ):

        #
        # Host Cell
        #
        # Most runtime nodes are initialized by
        # host_cell.json (init_node_state).
        #
        # Here we only override the values required
        # for this specific scenario.
        #

        builder.add_cell(

            template_id="cd4_t_cell",

            cell_id="cd4_001",

            position=(0, 0),

            runtime_state={

                "ATP":100,

                "ROS":5,

                "TCR":0,

                "IL2R":20
            }
        )

        #
        # Initial IFN field
        #

        builder.add_field(

            field_name="pMHC",

            values={

                (0, 0): 100.0

            }

        )

        #
        # Metadata
        #

        builder.metadata(

            name=self.name,

           description="CD4 IL2 stimulation demo.",

            version="0.7"

        )

    # =====================================================
    # Optional
    # =====================================================

    def metadata(self):

        return {

            "name": self.name,

            "description":
                "Single infected host cell.",

            "version":
                "0.7"

        }

    def runtime_options(self):

        return {

            "ticks": 5,

            "enable_console": True

        }
