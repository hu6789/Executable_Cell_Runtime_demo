from demo.scenario.base_scenario import BaseScenario


class InfectionDemo(BaseScenario):

    def __init__(self):

        super().__init__()

        self.name = "Host Infection Demo"

    def build(self, builder):

        builder.add_cell(

            template_id="host_cell",

            cell_id="host_001",

            position=(0, 0),

            runtime_state={

                "ATP":100,

                "ROS":5,

                "influenza":1,

                "viral_RNA":5,

                "capsid_protein":0,

                "NS1":0,

                "PA_X":0,

                "M2":0,

                "pathogen_signal":10
            }
        )
        
        builder.add_field(

            field_name="influenza",

            values={

                (0, 0): 100.0

            }

        )
        
        builder.metadata(

            name=self.name,

            description="Host cell infected by influenza.",

            version="0.7"
        )

    def runtime_options(self):

        return {

            "ticks":5,

            "enable_console":True
        }
