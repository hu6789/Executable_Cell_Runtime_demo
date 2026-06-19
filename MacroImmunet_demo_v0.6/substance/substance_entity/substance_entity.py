# substance/substance_entity/substance_entity.py

from substance.substance_entity.substance_identity import (
    SubstanceIdentity
)

from substance.substance_entity.substance_state import (
    SubstanceState
)

from substance.substance_entity.substance_runtime import (
    SubstanceRuntime
)


class SubstanceEntity:

    """
    Runtime Substance Instance

    Composition:

        Identity
        State
        Runtime

    Does NOT:

        - execute interactions
        - generate intents
        - perform diffusion
        - perform decay
    """

    def __init__(

        self,

        identity: SubstanceIdentity,

        state: SubstanceState
    ):

        self.identity = identity

        self.state = state

        self.runtime = SubstanceRuntime()

    # =====================================
    # convenience properties
    # =====================================

    @property
    def id(self):
        return self.identity.id

    @property
    def substance_type(self):

        return self.identity.substance_type

    @property
    def position(self):
        return self.state.position

    @property
    def amount(self):
        return self.state.amount
    
    @property
    def active(self):
        return self.state.active

    @active.setter
    def active(self, value):
        self.state.active = value
    
    # =====================================
    # runtime reset
    # =====================================

    def reset_runtime(self):

        self.runtime.reset()

    # =====================================
    # summary
    # =====================================

    def summary(self):

        return {

            "identity":
                self.identity.summary(),

            "state":
                self.state.summary(),

            "runtime":
                self.runtime.summary()
        }

    # =====================================
    # repr
    # =====================================

    def __repr__(self):

        return (

            f"SubstanceEntity("
            f"id={self.id}, "
            f"type={self.substance_type}, "
            f"amount={self.amount}"
            f")"
        )
