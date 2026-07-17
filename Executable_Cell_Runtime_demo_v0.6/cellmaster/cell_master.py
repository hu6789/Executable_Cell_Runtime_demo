# cellmaster/cell_master.py

from cellmaster.scheduler.scheduler import (
    RuntimeScheduler
)

from cellmaster.internalnet.internalnet import (
    InternalNet
)

from cellmaster.internalnet.runtime_context import (
    build_runtime_context
)

from cellmaster.stateupdate.state_update import (
    StateUpdater
)


class CellMaster:

    """
    Runtime orchestration layer

    responsibilities:

        Scheduler
            ↓

        RuntimeContext

            ↓

        InternalNet

            ↓

        StateUpdate

    DOES NOT:

        - write world
        - generate intents directly
        - apply lifecycle
    """

    def __init__(self):

        self.scheduler = RuntimeScheduler()

        self.internalnet = InternalNet()

        self.state_updater = StateUpdater()

    def run(

        self,

        node_inputs,

        world,

        tick=None
    ):

        # =============================
        # scheduler
        # =============================

        scheduled_contexts = (
            self.scheduler.schedule(

                node_inputs,

                world,

                tick=tick
            )
        )

        print(
            f"[CellMaster] scheduled="
            f"{len(scheduled_contexts)}"
        )

        runtime_outputs = []

        # =============================
        # internal runtime
        # =============================

        for runtime_request in scheduled_contexts:

            cell_id = runtime_request.get(
                "cell_id"
            )

            runtime_entity = (
                world.cells.get(
                    cell_id
                )
            )

            if runtime_entity is None:

                continue

            graph_context = (
                runtime_entity.runtime_graph
            )

            signal_inputs = (
                runtime_request.get(
                    "signals",
                    []
                )
            )

            runtime_context = (
                build_runtime_context(

                    runtime_entity=
                        runtime_entity,

                    node_inputs=
                        signal_inputs,

                    runtime_request=
                        runtime_request,

                    runtime_graph=
                        graph_context,

                    tick=
                        tick
                )
            )


            output = self.internalnet.run(

                runtime_entity=
                    runtime_entity,

                graph_context=
                    graph_context,

                node_inputs=
                    signal_inputs,

                runtime_context=
                    runtime_context,

                tick=
                    tick
            )

            runtime_outputs.append(
                output
            )

        print(
            f"[CellMaster] outputs="
            f"{len(runtime_outputs)}"
        )

        # =============================
        # state update
        # =============================

        runtime_packages = (
            self.state_updater.finalize(

                runtime_outputs,

                world,

                tick=tick
            )
        )

        print(
            f"[CellMaster] packages="
            f"{len(runtime_packages)}"
        )

        return runtime_packages
