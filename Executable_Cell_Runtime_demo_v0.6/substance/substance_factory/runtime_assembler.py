# substance/substance_factory/runtime_assembler.py

from substance.substance_entity.substance_identity import (
    SubstanceIdentity
)

from substance.substance_entity.substance_state import (
    SubstanceState
)

from substance.substance_entity.substance_entity import (
    SubstanceEntity
)


# =========================================
# build identity
# =========================================

def build_identity(
    template,
    substance_id,
    source_id=None
):

    return SubstanceIdentity(

        substance_id=
            substance_id,

        substance_type=
            template.substance_type,

        source_id=source_id
    )


# =========================================
# build state
# =========================================

def build_state(

    template,

    position,

    amount=None
):

    if amount is None:

        amount = template.default_amount

    return SubstanceState(

        position=
            position,

        amount=
            amount
    )


# =========================================
# assemble runtime entity
# =========================================

def assemble_runtime_entity(

    template,

    substance_id,

    position,

    amount=None,
    
    source_id=None
):

    identity = build_identity(

        template=
            template,

        substance_id=
            substance_id,

        source_id=
            source_id
    )

    state = build_state(

        template=
            template,

        position=
            position,

        amount=
            amount
    )

    entity = SubstanceEntity(

        identity=
            identity,

        state=
            state
    )

    entity.template = template

    return entity
