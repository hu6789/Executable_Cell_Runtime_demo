# visualization/recorder.py
import os
print("LOADING RECORDER:", os.path.abspath(__file__))
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

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
   

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

            tick=tick,
            
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

                    values=values,

                    max_value=max(values.values())
                    if values
                    else 0,

                    sources=[]

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
            
            package = behavior_lookup.get(
                cell_id,
                {}
            )
            
            debug_print(
                "RECORDER DEBUG:",
                cell_id,
                "package=",
                package
            )
            
            debug_print(
                "CALL NODE EXTRACT:",
                cell_id,
                package.keys()
            )

            inspector = build_inspector_snapshot(

                object_type="cell",

                object_id=cell_id,

                cell_type=self.get_cell_type(cell),

                nodes=self.collect_nodes_from_runtime(
                    package
                ),

                behaviors=self.collect_behaviors(
                    package
                )

            )

            inspectors[cell_id] = inspector

        return inspectors

    # =====================================================
    # Nodes
    # =====================================================

    def collect_nodes(self, cell):

        output=[]

        runtime = getattr(
            cell,
            "runtime_state",
            None
        )

        print(
            "RUNTIME:",
            cell.id,
            runtime.__dict__
        )

        if runtime is None:
            return output


        if isinstance(runtime, dict):

            iterator = runtime.items()

        elif hasattr(runtime,"__dict__"):

            iterator = runtime.__dict__.items()

        else:

            return output


        for key,value in iterator:

            if isinstance(value,(int,float)):

                output.append(
                    build_node_snapshot(
                        name=key,
                        value=round(value,3)
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

        behavior_trace = package.get(
            "behavior_trace",
            []
        )

        for item in behavior_trace:

            output.append(

                build_behavior_snapshot(

                    name=item.get(
                        "name",
                        item.get(
                            "behavior",
                            "unknown"
                        )
                    ),

                    strength=round(
                        float(
                            item.get(
                                "strength",
                                0
                            )
                        ),
                        6
                    )

                )

            )

        return output

    # =====================================================
    # Events
    # =====================================================

    def collect_events(runtime_result):

        output=[]
        
        if not runtime_result:
            return output


        tick=runtime_result.get("tick",0)


        # -----------------
        # input
        # -----------------

        for event in runtime_result.get("events",[]):

            if event.get("event_type")=="field_exposure_event":

                target=event.get("target_id")

                field=event.get("payload",{}).get(
                    "field_type"
                )

                output.append(
                    build_event_snapshot(
                        tick=tick,
                        category="INPUT",
                        message=
                        f"{target} senses {field}"
                    )
                )


        # -----------------
        # behavior
        # -----------------

        for package in runtime_result.get(
            "cell_packages",
            []
        ):

            cell_id=package.get("cell_id")

            for behavior in package.get(
                "behavior_trace",
                []
            ):

                name=behavior.get(
                    "name",
                    behavior.get("behavior")
                )

                output.append(
                    build_event_snapshot(
                        tick=tick,
                        category="BEHAVIOR",
                        message=
                        f"{cell_id}: {name}"
                    )
                )


        # -----------------
        # substance
        # -----------------

        for request in runtime_result.get(
            "substance_requests",
            []
        ):

            if request.get(
                "operation"
            )=="membrane_damage":

                output.append(
                    build_event_snapshot(
                        tick=tick,
                        category="SUBSTANCE",
                        message=
                        f"{request.get('source_id')} damages {request.get('target_id')} membrane"
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
        
    def normalize_cell_type(self, cell_type):

        name=str(cell_type).lower()
 
        if "cd4" in name:
            return "cd4"

        if "cd8" in name:
            return "cd8"

        if "host" in name:
            return "host"

        if "dead" in name:
            return "dead"

        return name

    def get_cell_type(self, cell):

        #
        # biological identity first
        #

        raw = (

            getattr(cell, "template_id", None)

            or

            getattr(cell, "cell_template", None)

            or

            getattr(cell, "cell_type", None)

            or

            getattr(cell, "type", None)

            or

            ""

        )


        #
        # fallback:
        # inspect id
        #

        if not raw:

            raw = getattr(
                cell,
                "id",
                ""
            )


        return self.normalize_cell_type(raw)

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
        
    def collect_nodes_from_runtime(
        self,
        package
    ):

        output=[]

        if not package:
            return output


        runtime_context = package.get(
            "runtime_context",
            {}
        )

        runtime = runtime_context.get(
            "runtime_state",
            {}
        )


        nodes = runtime.get(
            "nodes",
            {}
        )


        for name,value in nodes.items():
 
            output.append(

                build_node_snapshot(
                    name=name,
                    value=value
                )

            )

        return output
