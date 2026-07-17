# substance/substance_entity/substance_state.py


class SubstanceState:

    """
    World state layer

    Responsibilities:
        - position
        - amount
        - lifetime
        - active flag

    Does NOT:
        - store interaction rules
        - store runtime cache
        - store decision state
    """

    def __init__(

        self,

        position=(0, 0),

        amount=0.0,

        lifetime=0,

        active=True
    ):

        self.position = position

        self.amount = amount

        self.lifetime = lifetime

        self.active = active

    # =====================================
    # summary
    # =====================================

    def summary(self):

        return {

            "position":
                self.position,

            "amount":
                self.amount,

            "lifetime":
                self.lifetime,

            "active":
                self.active
        }
