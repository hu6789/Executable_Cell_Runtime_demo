# labelcenter/labelcenter.py

from labelcenter.intent_bucket import bucket_intents

from labelcenter.write_aggregator import (
    aggregate_intents
)

from labelcenter.runtime_state_apply import (
    apply_runtime_state_updates
)

from labelcenter.field_projection import (
    apply_field_projection
)

from labelcenter.field_dynamics import (
    apply_field_dynamics
)

from labelcenter.entity_apply import (
    apply_entity_updates
)

from labelcenter.targeted_directed_apply import (
    apply_targeted_directed_updates
)

from labelcenter.directed_effect_projection import (
    apply_world_directed_effects
)

from labelcenter.link_apply import (
    apply_link_updates
)

from labelcenter.cleanup import (
    cleanup_world
)


DEBUG = False


def debug_print(*args, **kwargs):

    if DEBUG:
        print(*args, **kwargs)


# ==========================================================
# LabelCenter
# ==========================================================

class LabelCenter:

    """
    LabelCenter v1.0

    World State Single Source of Truth (SSOT)

    Responsibilities
    ----------------
    - collect write requests
    - bucket requests
    - aggregate writes
    - execute world updates
    - cleanup world

    DOES NOT
    --------
    - perform biological reasoning
    - execute InternalNet
    - schedule cells
    - interpret physiology
    """

    def __init__(self):

        self.intent_queue = []

    # ======================================================
    # Collect
    # ======================================================

    def collect(
        self,
        intents
    ):

        if intents:

            self.intent_queue.extend(intents)

    # ======================================================
    # Main Apply
    # ======================================================

    def apply(
        self,
        world,
        tick
    ):

        buckets, invalid = bucket_intents(
            self.intent_queue
        )

        if invalid:

            print(
                f"[LabelCenter] ignored {len(invalid)} invalid intents."
            )


        #
        # Entity
        #

        self._run_entity(
            world,
            buckets["entity"]
        )

        #
        # Runtime
        #

        self._run_runtime_state(
            world,
            buckets["runtime_state"]
        )

        #
        # Field
        #

        self._run_field(
            world,
            buckets["field"]
        )

        #
        # Directed Effects
        #

        self._run_targeted_directed(
            world,
            buckets["targeted_directed"]
        )

        self.last_effect_events = self._run_directed_projection(
            world
        )

        #
        # Link
        #

        self._run_link(
            world,
            buckets["link"]
        )

        #
        # Cleanup
        #

        self._cleanup(
            world
        )

        #
        # Clear queue
        #

        self.intent_queue.clear()
        
    # ======================================================
    # Entity
    # ======================================================

    def _run_entity(
        self,
        world,
        intents
    ):

        intents = aggregate_intents(
            "entity",
            intents
        )

        apply_entity_updates(

            world=world,

            entity_requests=intents

        )
        
    # ======================================================
    # Runtime State
    # ======================================================

    def _run_runtime_state(
        self,
        world,
        intents
    ):

        intents = aggregate_intents(
            "runtime_state",
            intents
        )

        apply_runtime_state_updates(
            world=world,
            intents=intents
        )

    # ======================================================
    # Field
    # ======================================================

    def _run_field(
        self,
        world,
        intents
    ):
    
        intents = aggregate_intents(
            "field",
            intents
        )
        
        apply_field_projection(

            world=world,

            field_writes=intents,

            field_defs=world.field_defs

        )

        apply_field_dynamics(

            world=world,

            field_defs=world.field_defs

        )
    # ======================================================
    # Directed
    # ======================================================

    def _run_targeted_directed(
        self,
        world,
        intents
    ):

        apply_targeted_directed_updates(

            world=world,

            intents=intents

        )

    def _run_directed_projection(
        self,
        world
    ):

        return apply_world_directed_effects(
            world
        )

    # ======================================================
    # Link
    # ======================================================

    def _run_link(
        self,
        world,
        intents
    ):

        apply_link_updates(

            world=world,

            intents=intents

        )

    # ======================================================
    # Cleanup
    # ======================================================

    def _cleanup(
        self,
        world
    ):

        cleanup_world(world)
