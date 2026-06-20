# labelcenter/labelcenter.py

from labelcenter.intent_bucket import bucket_intents
from labelcenter.write_aggregator import (
    aggregate_fields
)

from labelcenter.field_projection import (
    apply_field_projection
)

from labelcenter.field_dynamics import (
    apply_field_dynamics
)

from labelcenter.lifecycle_manager import (
    apply_lifecycle_updates
)

from labelcenter.cleanup import (
    cleanup_world
)
from labelcenter.cell_state_apply import (
    apply_cell_state_updates
)

from labelcenter.label_flag_apply import (
    apply_label_flag_updates
)

from labelcenter.targeted_directed_apply import (
    apply_targeted_directed_updates
)

from labelcenter.link_apply import (
    apply_link_updates
)

from labelcenter.directed_effect_projection import (
    apply_world_directed_effects
)

from labelcenter.runtime_state_apply import (
    apply_runtime_state_updates
)

class LabelCenter:

    """
    v0.6 World Execution Layer

    LabelCenter is the ONLY world write authority (SSOT).

    Responsibilities:
        - collect intents
        - classify intents
        - orchestrate apply order
        - execute world writes
        - cleanup invalid entities

    LabelCenter DOES NOT:
        - perform biology reasoning
        - compute behavior logic
        - interpret physiology
    """

    def __init__(self):

        # runtime intent queue
        self.intent_queue = []

    # =========================================
    # collect intents
    # =========================================

    def collect(self, intents):

        if not intents:
            return

        self.intent_queue.extend(intents)

    # =========================================
    # main apply pipeline
    # =========================================

    def apply(self, world, tick):

        # -------------------------------------
        # 1. bucket intents
        # -------------------------------------

        buckets, invalid = bucket_intents(
            self.intent_queue
        )

        if invalid:
            print(
                f"[LabelCenter] invalid intents: {len(invalid)}"
            )

        # -------------------------------------
        # 2. apply ordered phases
        # -------------------------------------

        self._apply_cell_state(
            world,
            buckets["cell_state"],
            tick
        )
        
        self._apply_runtime_state(
            world,
            buckets["runtime_state"],
            tick
        )
        

        self._apply_label_flag(
            world,
            buckets["label_flag"],
            tick
        )

        self._apply_field(
            world,
            buckets["field"],
            tick
        )

        self._apply_targeted_directed(
            world,
            buckets["targeted_directed"],
            tick
        )
        
        self._apply_directed_effect_projection(
            world,
            tick
        )

        self._apply_link(
            world,
            buckets["link"],
            tick
        )

        self._apply_entity_lifecycle(
            world,
            buckets["entity_lifecycle"],
            tick
        )

        # -------------------------------------
        # 3. cleanup
        # -------------------------------------

        self._cleanup(world)

        # -------------------------------------
        # 4. clear queue
        # -------------------------------------

        self.intent_queue.clear()

    # =========================================
    # apply phases (skeleton)
    # =========================================

    def _apply_cell_state(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply cell_state: {len(intents)}"
        )

        apply_cell_state_updates(
            world=world,
            intents=intents
        )
        
    def _apply_runtime_state(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply runtime_state: {len(intents)}"
        )

        apply_runtime_state_updates(
            world=world,
            intents=intents
        )
    
    def _apply_label_flag(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply label_flag: {len(intents)}"
        )

        apply_label_flag_updates(
            world=world,
            intents=intents
        )

    def _apply_field(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply field: {len(intents)}"
        )

        # -------------------------------------
        # aggregate field writes
        # -------------------------------------

        aggregated = aggregate_fields(
            intents
        )

        print(
            f"[Field] aggregated writes: "
            f"{len(aggregated)}"
        )

        # -------------------------------------
        # projection
        # -------------------------------------

        apply_field_projection(
            world=world,
            field_writes=aggregated,
            field_defs=world.field_defs
        )
        
        print("\n[DEBUG] AFTER PROJECTION")
        print(world.fields)
 
        # -------------------------------------
        # autonomous field evolution
        # -------------------------------------

        apply_field_dynamics(
            world=world,
            field_defs=world.field_defs
        )
        
        print("\n[DEBUG] AFTER DYNAMICS")
        print(world.fields)

    def _apply_targeted_directed(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply targeted_directed: {len(intents)}"
        )

        apply_targeted_directed_updates(
            world=world,
            intents=intents
        )

    def _apply_directed_effect_projection(
        self,
        world,
        tick
    ):

        print(
            "[LabelCenter] apply directed_effect_projection"
        )

        apply_world_directed_effects(
            world
        )

    def _apply_link(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply link: {len(intents)}"
        )

        apply_link_updates(
            world=world,
            intents=intents
        )

    def _apply_entity_lifecycle(
        self,
        world,
        intents,
        tick
    ):

        print(
            f"[LabelCenter] apply entity_lifecycle: {len(intents)}"
        )
 
        apply_lifecycle_updates(
            world=world,
            lifecycle_intents=intents
        )
    # =========================================
    # cleanup
    # =========================================

    def _cleanup(self, world):

        print("[LabelCenter] cleanup")

        cleanup_world(world)
