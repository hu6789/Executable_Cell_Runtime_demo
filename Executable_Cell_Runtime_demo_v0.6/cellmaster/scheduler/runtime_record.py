# cellmaster/scheduler/runtime_record.py


# =========================================
# scheduler runtime records
# =========================================

class RuntimeRecordManager:

    """
    scheduler runtime memory

    stores:
        - last runtime tick
        - activation history
        - persistence state
        - cooldown state
        - runtime statistics
    """

    def __init__(self):

        self.records = {}

    # =====================================
    # get record
    # =====================================

    def get_record(
        self,
        cell_id
    ):

        if cell_id not in self.records:

            self.records[cell_id] = (
                build_empty_record()
            )

        return self.records[cell_id]

    # =====================================
    # update after runtime
    # =====================================

    def update_runtime_record(
        self,
        cell_id,
        runtime_context,
        tick
    ):

        record = self.get_record(
            cell_id
        )

        # ---------------------------------
        # last runtime
        # ---------------------------------

        record["last_runtime_tick"] = (
            tick
        )

        # ---------------------------------
        # activation count
        # ---------------------------------

        record["runtime_count"] += 1

        # ---------------------------------
        # persistence
        # ---------------------------------

        if runtime_context.get(
            "persistent_runtime",
            False
        ):

            record[
                "persistent_ticks"
            ] += 1

        else:

            record[
                "persistent_ticks"
            ] = 0

        # ---------------------------------
        # cooldown tracking
        # ---------------------------------

        record[
            "last_priority"
        ] = runtime_context.get(
            "runtime_priority",
            0.0
        )

        # ---------------------------------
        # activation source
        # ---------------------------------

        trigger_source = runtime_context.get(
            "trigger_source",
            "unknown"
        )

        record[
            "last_trigger_source"
        ] = trigger_source

        # ---------------------------------
        # runtime history
        # ---------------------------------

        history = record[
            "runtime_history"
        ]

        history.append({

            "tick": tick,

            "priority":
                runtime_context.get(
                    "runtime_priority",
                    0.0
                ),

            "source":
                trigger_source
        })

        # limit history
        max_history = 32

        if len(history) > max_history:

            history.pop(0)

    # =====================================
    # mark skipped runtime
    # =====================================

    def mark_skipped(
        self,
        cell_id,
        reason
    ):

        record = self.get_record(
            cell_id
        )

        record[
            "last_skip_reason"
        ] = reason

    # =====================================
    # cleanup dead cells
    # =====================================

    def remove_record(
        self,
        cell_id
    ):

        if cell_id in self.records:

            del self.records[cell_id]


# =========================================
# empty record template
# =========================================

def build_empty_record():

    return {

        "last_runtime_tick": None,

        "runtime_count": 0,

        "persistent_ticks": 0,

        "last_priority": 0.0,

        "last_trigger_source": None,

        "last_skip_reason": None,

        "runtime_history": [],

        "last_runtime_state": {}
    }
