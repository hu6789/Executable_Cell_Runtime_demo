# cellinstance/runtime/runtime_identity.py


# =========================================
# Runtime Identity
# =========================================

class RuntimeIdentity:

    """
    biological semantic identity container

    responsibilities:
        - store biological identity
        - expose lineage/subtype semantics
        - support identity matching
        - support phenotype queries

    DOES NOT:
        - store runtime state
        - execute runtime logic
        - write world state
    """

    def __init__(

        self,

        cell_type,

        lineage=None,

        subtype=None,

        phenotype_tags=None,

        metadata=None
    ):

        # =================================
        # primary type
        # =================================

        self.cell_type = cell_type

        # =================================
        # lineage semantics
        # =================================

        self.lineage = lineage

        # =================================
        # subtype semantics
        # =================================

        self.subtype = subtype

        # =================================
        # phenotype descriptors
        # =================================

        self.phenotype_tags = set(

            phenotype_tags or []
        )

        # =================================
        # additional metadata
        # =================================

        self.metadata = (

            metadata or {}
        )

    # =====================================
    # tag check
    # =====================================

    def has_tag(
        self,
        tag
    ):

        return tag in self.phenotype_tags

    # =====================================
    # add tag
    # =====================================

    def add_tag(
        self,
        tag
    ):

        self.phenotype_tags.add(
            tag
        )

    # =====================================
    # remove tag
    # =====================================

    def remove_tag(
        self,
        tag
    ):

        self.phenotype_tags.discard(
            tag
        )

    # =====================================
    # export summary
    # =====================================

    def summary(self):

        return {

            "cell_type":
                self.cell_type,

            "lineage":
                self.lineage,

            "subtype":
                self.subtype,

            "phenotype_tags":
                list(
                    self.phenotype_tags
                ),

            "metadata":
                self.metadata
        }
