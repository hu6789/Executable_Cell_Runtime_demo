# visualization/snapshot_adapter.py


"""
=========================================================
Visualization Snapshot Adapter
=========================================================

Convert observer StateSnapshot into visualization snapshot.

Pipeline

StateSnapshot
        +
Runtime Result
        |
        v
VisualizationSnapshot
        |
        v
Viewer


Responsibilities
----------------
- translate observer snapshot
- build renderer data
- build inspector data
- build event data


DOES NOT
--------
- access SimulationWorld
- modify runtime
- execute simulation
"""


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

from visualization.event_builder import (
    VisualizationEventBuilder
)

# =====================================================
# Inspector Node Display Rules
# =====================================================

NODE_DISPLAY_RULES = {

    "host": [
        "ATP",
        "pathogen_signal",
        "influenza",
        "CXCL10",
        "membrane_integrity"
    ],


    "cd4_t": [
        "ATP",
        "TCR",
        "IL2",
        "IL2R",
        "CXCR3",
        "membrane_integrity"
    ],


    "cd8_t": [
        "ATP",
        "TCR",
        "IL2R",
        "perforin",
        "CXCR3",
        "membrane_integrity"
    ]

}

class VisualizationSnapshotAdapter:


    """
    Observer snapshot -> Visualization snapshot
    """


    # =====================================================
    # Public API
    # =====================================================
    
    def __init__(self):

        self.event_builder = VisualizationEventBuilder()
        
    def adapt(

        self,
        
        state_snapshot,

        runtime_result=None

    ):


        return build_snapshot(
        
            tick=state_snapshot.tick,

            world=self.build_world(

                state_snapshot

            ),

            inspectors=self.build_inspectors(

                state_snapshot,

                runtime_result

            ),

            events=self.event_builder.build(

                tick=state_snapshot.tick,

                state_snapshot=state_snapshot,

                runtime_result=runtime_result

            ),

            metadata=self.build_metadata(

                state_snapshot

            )

        )


    # =====================================================
    # World
    # =====================================================

    def build_world(

        self,

        snapshot

    ):


        if isinstance(snapshot, dict):
 
            tick = snapshot.get(
                "tick",
                0
            )

            cells = snapshot.get(
                "cells",
                {}
            )

            fields = snapshot.get(
                "fields",
                {}
            )

            substances = snapshot.get(
                "substances",
                {}

            )

            metadata = snapshot.get(
                "metadata",
                {}

            )
  
        else:

            tick = snapshot.tick

            cells = snapshot.cells

            fields = snapshot.fields

            substances = snapshot.substances

            metadata = snapshot.metadata
        
        return build_world_snapshot(

            tick=snapshot.tick,

            width=metadata.get(
                "width",
                20
            ),

            height=metadata.get(

                "height",

                20

            ),

            cells=self.build_cells(

                snapshot

            ),

            particles=self.build_particles(

                snapshot

            ),

            fields=self.build_fields(

                snapshot

            )

        )


    # =====================================================
    # Cells
    # =====================================================

    def build_cells(

        self,

        snapshot

    ):

        output = []


        for cell_id, cell in snapshot.cells.items():


            identity = cell.get(

                "identity"

            )


            cell_type = "unknown"


            if identity is not None:


                if hasattr(

                    identity,

                    "cell_type"

                ):

                    cell_type = identity.cell_type


                elif isinstance(

                    identity,

                    dict

                ):

                    cell_type = identity.get(

                        "cell_type",

                        "unknown"

                    )


            output.append(

                build_cell_snapshot(

                    cell_id=cell_id,

                    cell_type=cell_type,

                    position=cell.get(

                        "position",

                        (0,0)

                    ),

                    alive=True

                )

            )


        return output



    # =====================================================
    # Particles
    # =====================================================

    def build_particles(

        self,

        snapshot

    ):


        particles = []


        for pid, substance in snapshot.substances.items():


            particles.append({

                "id":
                    pid,

                "type":
                    substance.get(

                        "substance_type",

                        "unknown"

                    ),

                "position":
                    substance.get(

                        "position",

                        (0,0)

                    ),

                "strength":
                    substance.get(

                        "amount"

                    )

            })


        return particles



    # =====================================================
    # Fields
    # =====================================================

    def build_fields(

        self,

        snapshot

    ):


        output = []


        for field_type, values in snapshot.fields.items():


            output.append(

                build_field_snapshot(

                    field_type=field_type,

                    values=values

                )

            )


        return output



    # =====================================================
    # Inspector
    # =====================================================

    def build_inspectors(

        self,

        snapshot,

        runtime_result=None

    ):


        inspectors = {}


        behavior_lookup = self._collect_behavior_output(

            runtime_result

        )


        for cell_id, cell in snapshot.cells.items():


            runtime_state = cell.get(
                "runtime_state",
                None
            )


            if runtime_state is None:

                runtime_state = cell.get(
                    "runtime_context",
                    {}
                ).get(
                    "runtime_state",
                    {}
                )

            identity = cell.get("identity")

            if isinstance(identity,dict):

                cell_type = identity.get(
                    "cell_type",
                    "unknown"
                )

            else:

                cell_type = getattr(
                    identity,
                    "cell_type",
                    "unknown"
                )

            nodes = self.build_nodes(

                runtime_state,

                cell_type

            )

            behaviors = self.build_behaviors(

                behavior_lookup.get(

                    cell_id,

                    {}

                )

            )

            inspectors[cell_id] = build_inspector_snapshot(

                object_type="cell",

                object_id=cell_id,

                cell_type=cell_type,

                nodes=nodes,

                behaviors=behaviors

            )


        return inspectors



    # =====================================================
    # Nodes
    # =====================================================

    def build_nodes(
        self,
        runtime_state,
        cell_type=None
    ):


        output = []


        allowed = NODE_DISPLAY_RULES.get(
            cell_type,
            []
        )


        for name, value in runtime_state.items():


            if allowed and name not in allowed:
                continue


            if isinstance(
                value,
                (int,float)
            ):


                output.append(

                    build_node_snapshot(

                        name=name,

                        value=value

                    )

                )


        return output
    
    # =====================================================
    # Behaviors
    # =====================================================

    def build_behaviors(self, package):

        output = []


        behavior_output = package.get(
            "behavior_output",
            {}
        )


        trace = behavior_output.get(
            "behavior_trace",
            []
        )


        if not trace:

            snapshot = package.get(
                "runtime_snapshot",
                {}
            )

            trace = snapshot.get(
                "behavior_trace",
                []
            )


        for item in trace:

            output.append(

                build_behavior_snapshot(

                    name=item.get("behavior"),

                    strength=item.get(
                        "strength",
                        0
                    )
                )
            )


        return output
    # =====================================================
    # Runtime result helpers
    # =====================================================

    def _collect_behavior_output(

        self,

        runtime_result

    ):


        result = {}


        if runtime_result is None:

            return result


        for package in runtime_result.get(

            "cell_packages",

            []

        ):


            cell_id = package.get(

                "cell_id"

            )


            if cell_id:

                result[cell_id] = package


        return result

    # =====================================================
    # Metadata
    # =====================================================

    def build_metadata(

        self,

        snapshot

    ):


        return build_metadata_snapshot(

            scenario=snapshot.metadata.get(

                "scenario"

            ),

            title=snapshot.metadata.get(

                "title"

            ),

            description=snapshot.metadata.get(

                "description"

            )

        )
