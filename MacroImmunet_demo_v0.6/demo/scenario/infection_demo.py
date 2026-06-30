# demo/scenario/infection_demo.py

"""
=========================================================
Infection Demo Scenario
=========================================================

Minimal infection scenario for MacroImmunet Demo.

Responsibilities
----------------
- create initial cells
- create initial virus
- create initial field
- provide MiniSIO requests

DOES NOT
--------
- execute simulation
- build SimulationWorld
- perform biological reasoning
"""

from demo.scenario.base_scenario import (
    BaseScenario
)

from minisio.minisio_schema import (
    MiniSIOOperation,
    MiniSIOWriteMode
)


class InfectionDemo(BaseScenario):

    """
    Minimal influenza infection demo.

    Initial world

        Host Cell
            +

        Influenza Virus
            +

        IFN Field
    """

    def __init__(self):

        super().__init__()

        self.name = "Minimal Infection Demo"

    # =====================================================
    # Build Scenario
    # =====================================================

    def build(self):

        requests = [

            #
            # Host Cell
            #

            {

                "operation":
                    MiniSIOOperation.CREATE_CELL,

                "write_mode":
                    MiniSIOWriteMode.ENTITY,

                "target_id":
                    "host_001",

                "payload": {

                    "template_id":
                        "host_cell",

                    "position":
                        (0, 0)

                }

            },

            #
            # Influenza Virus
            #

            {

                "operation":
                    MiniSIOOperation.CREATE_VIRUS,

                "write_mode":
                    MiniSIOWriteMode.ENTITY,

                "target_id":
                    "virus_001",

                "payload": {

                    "template_id":
                        "influenza_A",

                    "position":
                        (0, 0)

                }

            },

            #
            # Initial IFN field
            #

            {

                "operation":
                    MiniSIOOperation.EMIT_FIELD,

                "write_mode":
                    MiniSIOWriteMode.FIELD,

                "payload": {

                    "field_name":
                        "IFN",

                    "position":
                        (0, 0),

                    "value":
                        1.0

                }

            }

        ]

        return requests

    # =====================================================
    # Optional
    # =====================================================

    def metadata(self):

        return {

            "name":
                self.name,

            "description":
                "Single host cell with one influenza virus.",

            "version":
                "0.6"

        }

    def runtime_options(self):

        return {

            "ticks": 20,

            "enable_console": True

        }
