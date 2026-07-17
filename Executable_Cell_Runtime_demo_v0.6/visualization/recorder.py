# visualization/recorder.py

from visualization.snapshot import (
    build_snapshot,
    build_world_snapshot,
    build_cell_snapshot,
    build_field_snapshot,
    build_inspector_snapshot,
    build_node_snapshot,
    build_behavior_snapshot,
    build_event_snapshot,
    build_metadata_snapshot
)


# =========================================================
# Visualization Recorder
# =========================================================

class VisualizationRecorder:

    def __init__(self):

        self.snapshots = []

    # =====================================================
    # Record Tick
    # =====================================================

    def record_tick(

        self,

        tick,

        world,

        runtime_result=None

    ):

        snapshot = build_snapshot(

            world=self.collect_world(

                tick,
                world

            ),

            inspectors=self.collect_inspectors(

                world,
                runtime_result

            ),

            events=self.collect_events(

                runtime_result

            ),

            metadata=self.collect_metadata(

                runtime_result

            )

        )

        self.snapshots.append(

            snapshot

        )

        return snapshot

    # =====================================================
    # World
    # =====================================================

    def collect_world(

        self,

        tick,

        world

    ):

        return build_world_snapshot(

            tick=tick,

            width=getattr(

                world,
                "width",
                20

            ),

            height=getattr(

                world,
                "height",
                20

            ),

            cells=self.collect_cells(

                world

            ),

            particles=[],

            fields=self.collect_fields(

                world

            )

        )

    # =====================================================
    # Cells
    # =====================================================

    def collect_cells(

        self,

        world

    ):

        output = []

        cells = getattr(

            world,

            "cells",

            {}

        )

        if isinstance(

            cells,

            dict

        ):

            iterable = cells.values()

        else:

            iterable = cells

        for cell in iterable:

            output.append(

                build_cell_snapshot(

                    cell_id=self.get_cell_id(cell),

                    cell_type=self.get_cell_type(cell),

                    position=self.get_position(cell),

                    alive=self.get_alive(cell)

                )

            )

        return output

    # =====================================================
    # Fields
    # =====================================================

    def collect_fields(

        self,

        world

    ):

        output = []

        fields = getattr(

            world,

            "fields",

            {}

        )

        if not isinstance(

            fields,

            dict

        ):

            return output

        for field_type, values in fields.items():

            output.append(

                build_field_snapshot(

                    field_type=field_type,

                    values=values

                )

            )

        return output

    # =====================================================
    # Inspectors
    # =====================================================

    def collect_inspectors(

        self,

        world,

        runtime_result

    ):

        inspectors = {}

        cells = getattr(

            world,

            "cells",

            {}

        )

        if isinstance(

            cells,

            dict

        ):

            iterable = cells.values()

        else:

            iterable = cells

        #
        # behavior lookup
        #

        behavior_lookup = {}

        if runtime_result:

            for package in runtime_result.get(

                "cell_packages",

                []

            ):

                behavior_lookup[

                    package.get(

                        "cell_id"

                    )

                ] = package

        for cell in iterable:

            cell_id = self.get_cell_id(

                cell

            )

            inspector = build_inspector_snapshot(

                cell_id=cell_id,

                cell_type=self.get_cell_type(

                    cell

                ),

                nodes=self.collect_nodes(

                    cell

                ),

                behaviors=self.collect_behaviors(

                    behavior_lookup.get(

                        cell_id,

                        {}

                    )

                )

            )

            inspectors[cell_id] = inspector

        return inspectors

    # =====================================================
    # Nodes
    # =====================================================

    def collect_nodes(

        self,

        cell

    ):

        output = []

        runtime = getattr(

            cell,

            "runtime_state",

            None

        )

        if runtime is None:

            return output

        if hasattr(

            runtime,

            "__dict__"

        ):

            for key, value in runtime.__dict__.items():

                if isinstance(

                    value,

                    (int, float)

                ):

                    output.append(

                        build_node_snapshot(

                            name=key,

                            value=round(

                                value,

                                3

                            )

                        )

                    )

        return output

    # =====================================================
    # Behaviors
    # =====================================================

    def collect_behaviors(

        self,

        package

    ):

        output = []

        if not package:

            return output

        behavior_output = package.get(

            "behavior_output",

            {}

        )

        regulated = behavior_output.get(

            "regulated_behaviors",

            {}

        )

        for name, strength in regulated.items():

            output.append(

                build_behavior_snapshot(

                    name=name,

                    strength=round(

                        float(strength),

                        6

                    )

                )

            )

        return output

    # =====================================================
    # Events
    # =====================================================

    def collect_events(

        self,

        runtime_result

    ):

        output = []

        if not runtime_result:

            return output

        for event in runtime_result.get(

            "events",

            []

        ):

            event_type = event.get(

                "event_type",

                "event"

            )

            target = event.get(

                "target_id",

                ""

            )

            message = (

                f"{event_type}: {target}"

            )

            output.append(

                build_event_snapshot(

                    tick=event.get(

                        "tick",

                        0

                    ),

                    message=message,

                    level="info"

                )

            )

        return output

    # =====================================================
    # Metadata
    # =====================================================

    def collect_metadata(

        self,

        runtime_result

    ):

        if runtime_result is None:

            return build_metadata_snapshot()

        return build_metadata_snapshot(

            scenario=runtime_result.get(

                "scenario"

            ),

            title=runtime_result.get(

                "title"

            )

        )

    # =====================================================
    # Helpers
    # =====================================================

    def get_cell_id(

        self,

        cell

    ):

        return getattr(

            cell,

            "id",

            "unknown"

        )

    def get_position(

        self,

        cell

    ):

        return getattr(

            cell,

            "position",

            (0, 0)

        )

    def get_alive(

        self,

        cell

    ):

        return getattr(

            cell,

            "alive",

            True

        )

    def get_cell_type(

        self,

        cell

    ):

        return (

            getattr(

                cell,

                "cell_type",

                None

            )

            or

            getattr(

                cell,

                "type",

                None

            )

            or

            cell.__class__.__name__

        )

    # =====================================================
    # Timeline
    # =====================================================

    def get_snapshot(

        self,

        tick

    ):

        return self.snapshots[tick]

    def latest_snapshot(

        self

    ):

        if not self.snapshots:

            return None

        return self.snapshots[-1]

    def clear(

        self

    ):

        self.snapshots.clear()

    def snapshot_count(

        self

    ):

        return len(

            self.snapshots

        )
