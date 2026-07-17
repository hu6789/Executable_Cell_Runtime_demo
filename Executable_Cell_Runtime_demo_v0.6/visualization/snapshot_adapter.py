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


class VisualizationSnapshotAdapter:


    """
    Observer snapshot -> Visualization snapshot
    """


    # =====================================================
    # Public API
    # =====================================================

    def adapt(

        self,

        state_snapshot,

        runtime_result=None

    ):


        return build_snapshot(

            world=self.build_world(

                state_snapshot

            ),

            inspectors=self.build_inspectors(

                state_snapshot,

                runtime_result

            ),

            events=self.build_events(

                runtime_result

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


        return build_world_snapshot(

            tick=snapshot.tick,

            width=snapshot.metadata.get(

                "width",

                20

            ),

            height=snapshot.metadata.get(

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


            nodes = self.build_nodes(

                cell.get(

                    "runtime_state",

                    {}

                )

            )


            behaviors = self.build_behaviors(

                behavior_lookup.get(

                    cell_id,

                    {}

                )

            )


            identity = cell.get(

                "identity"

            )


            cell_type = "unknown"


            if identity is not None:

                cell_type = getattr(

                    identity,

                    "cell_type",

                    "unknown"

                )


            inspectors[cell_id] = build_inspector_snapshot(

                cell_id=cell_id,

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

        runtime_state

    ):


        output = []


        for name, value in runtime_state.items():


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

    def build_behaviors(

        self,

        package

    ):


        output = []


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

                    strength=strength

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
    # Events
    # =====================================================

    def build_events(

        self,

        runtime_result

    ):


        output = []


        if runtime_result is None:

            return output


        for event in runtime_result.get(

            "events",

            []

        ):


            output.append(

                build_event_snapshot(

                    tick=event.get(

                        "tick",

                        0

                    ),

                    message=str(event),

                    level="info"

                )

            )


        return output



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
