# substance/substance_entity/substance_identity.py


class SubstanceIdentity:

    """
    Immutable identity layer

    Responsibilities:
        - substance id
        - substance type

    Does NOT:
        - store runtime state
        - store position
        - store amount
    """

    def __init__(

        self,

        substance_id,

        substance_type
    ):

        self.id = substance_id

        self.substance_type = (
            substance_type
        )

    # =====================================
    # summary
    # =====================================

    def summary(self):

        return {

            "id":
                self.id,

            "substance_type":
                self.substance_type
        }
