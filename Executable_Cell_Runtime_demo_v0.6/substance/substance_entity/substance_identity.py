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
        substance_type,
        source_id=None
    ):

        self.id = substance_id
        self.substance_type = substance_type
        self.source_id = source_id

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
