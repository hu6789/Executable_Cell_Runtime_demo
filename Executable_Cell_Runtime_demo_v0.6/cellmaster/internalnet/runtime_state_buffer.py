# cellmaster/internalnet/runtime_state_buffer.py


# =========================================
# Runtime State Buffer
# =========================================

class RuntimeStateBuffer:

    """
    staged runtime state carrier

    responsibilities:
        - preserve runtime stage snapshots
        - propagate staged runtime states
        - expose current/latest runtime state
        - preserve runtime lineage/debug

    DOES NOT:
        - execute runtime logic
        - evaluate biology
        - mutate world state
    """

    def __init__(self):

        # =================================
        # ordered stage snapshots
        # =================================

        self.stage_states = {}

        # =================================
        # stage execution order
        # =================================

        self.stage_order = []

    # =====================================
    # initialize base runtime state
    # =====================================

    def initialize(
        self,
        base_runtime_state
    ):

        self.write_stage_state(

            stage_name="base_state",

            runtime_state=
                base_runtime_state
        )

    # =====================================
    # write stage state
    # =====================================

    def write_stage_state(
        self,
        stage_name,
        runtime_state
    ):

        self.stage_states[
            stage_name
        ] = runtime_state

        if stage_name not in self.stage_order:

            self.stage_order.append(
                stage_name
            )

    # =====================================
    # read stage state
    # =====================================

    def read_stage_state(
        self,
        stage_name
    ):

        return self.stage_states.get(
            stage_name
        )

    # =====================================
    # latest runtime state
    # =====================================

    def get_latest_state(self):

        if not self.stage_order:

            return {}

        latest_stage = (

            self.stage_order[-1]
        )

        return self.stage_states.get(
            latest_stage,
            {}
        )

    # =====================================
    # previous runtime state
    # =====================================

    def get_previous_state(self):

        if len(self.stage_order) < 2:

            return {}

        previous_stage = (

            self.stage_order[-2]
        )

        return self.stage_states.get(
            previous_stage,
            {}
        )

    # =====================================
    # get stage lineage
    # =====================================

    def get_stage_lineage(self):

        return list(
            self.stage_order
        )

    # =====================================
    # export all runtime stages
    # =====================================

    def export(self):

        exported = {}

        for stage_name in self.stage_order:

            exported[stage_name] = 

                self.stage_states[
                    stage_name
                ]
            

        return exported

    # =====================================
    # debug summary
    # =====================================

    def build_debug_summary(self):

        return {

            "stages":
                self.get_stage_lineage(),

            "latest_state":
                self.get_latest_state()
        }
