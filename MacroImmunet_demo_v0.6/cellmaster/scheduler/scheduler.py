# cellmaster/scheduler/scheduler.py

from cellmaster.scheduler.runtime_trigger import (
    collect_runtime_triggers
)

from cellmaster.scheduler.eligibility import (
    check_runtime_eligibility
)

from cellmaster.scheduler.persistence import (
    evaluate_persistence
)

from cellmaster.scheduler.cooldown import (
    evaluate_cooldown
)

from cellmaster.scheduler.priority import (
    compute_runtime_priority
)

from cellmaster.scheduler.scheduling_policy import (
    apply_scheduling_policy
)

from cellmaster.scheduler.budget_allocator import (
    allocate_runtime_budget
)

from cellmaster.scheduler.runtime_record import (
    RuntimeRecordManager
)

from cellmaster.scheduler.internal_trigger_builder import (
    build_internal_triggers
)

class RuntimeScheduler:

    """
    Runtime orchestration authority.

    responsibilities:
        - runtime trigger integration
        - runtime eligibility
        - persistence handling
        - cooldown handling
        - priority evaluation
        - scheduling policy
        - budget allocation
        - runtime record update

    RuntimeScheduler DOES NOT execute
    InternalNet directly.

    execution is handled later by
    runtime dispatcher / backend layer.
    """

    def __init__(self):

        self.runtime_records = (
            RuntimeRecordManager()
        )

    # =====================================
    # main scheduling entry
    # =====================================

    def schedule(
        self,
        node_inputs,
        world,
        tick=None
    ):

        print(
            f"[Scheduler] tick={tick}"
        )
        # ---------------------------------
        # internal runtime triggers
        # ---------------------------------

        internal_inputs = (

            build_internal_triggers(

                world,

                self.runtime_records.records
            )
        )
        
        # ---------------------------------
        # merge inputs
        # ---------------------------------

        merged_inputs = []

        merged_inputs.extend(
            node_inputs
        )

        merged_inputs.extend(
            internal_inputs
        )
      
        # ---------------------------------
        # runtime trigger collection
        # ---------------------------------

        trigger_contexts = (

            collect_runtime_triggers(

                merged_inputs,

                self.runtime_records.records
            )
        )

        print(
            f"[Scheduler] triggers="
            f"{len(trigger_contexts)}"
        )

        scheduled = []

        # =================================
        # evaluate runtime contexts
        # =================================

        for context in trigger_contexts:

            # -----------------------------
            # eligibility
            # -----------------------------

            eligible = (

                check_runtime_eligibility(
                    context,
                    world,
                    self.runtime_records.records
                )
            )

            if not eligible:

                continue

            # -----------------------------
            # persistence
            # -----------------------------

            context = evaluate_persistence(

                context,
                self.runtime_records.records
            )

            # -----------------------------
            # cooldown
            # -----------------------------

            context = evaluate_cooldown(

                context,
               self.runtime_records.records
            )

            # -----------------------------
            # priority
            # -----------------------------

            context = compute_runtime_priority(
                context
            )

            # -----------------------------
            # scheduling policy
            # -----------------------------

            context["tick"] = tick

            context = apply_scheduling_policy(
                context
            )

            if not context.get(
                "execute_runtime",
                False
            ):

                continue

            scheduled.append(
                context
            )

        print(
            f"[Scheduler] eligible="
            f"{len(scheduled)}"
        )

        # =================================
        # runtime budget allocation
        # =================================

        scheduled = allocate_runtime_budget(

            scheduled
        )

        print(
            f"[Scheduler] allocated="
            f"{len(scheduled)}"
        )

        # =================================
        # update runtime records
        # =================================

        for context in scheduled:

            cell_id = context.get(
                "cell_id"
            )

            self.runtime_records.update_runtime_record(

                cell_id,
                context,
                tick
            )

        return scheduled
