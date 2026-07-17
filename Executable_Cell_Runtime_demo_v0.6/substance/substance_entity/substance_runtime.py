# substance/substance_entity/substance_runtime.py


class SubstanceRuntime:

    """
    Runtime cache layer

    Responsibilities:
        - candidate targets
        - interaction events
        - generated requests

    Runtime data is rebuilt every tick.

    Does NOT:
        - store persistent world state
        - store template data
        - store interaction rules
    """

    def __init__(self):

        self.candidate_targets = []

        self.interaction_events = []

        self.generated_requests = []

    # =====================================
    # reset
    # =====================================

    def reset(self):

        self.candidate_targets.clear()

        self.interaction_events.clear()

        self.generated_requests.clear()

    # =====================================
    # summary
    # =====================================

    def summary(self):

        return {

            "candidate_targets":
                len(self.candidate_targets),

            "interaction_events":
                len(self.interaction_events),

            "generated_requests":
                len(self.generated_requests)
        }
