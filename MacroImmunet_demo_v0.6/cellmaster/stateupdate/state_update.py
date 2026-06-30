# cellmaster/stateupdate/state_update.py

from cellmaster.stateupdate.context_integrator import (
    integrate_runtime_context
)

from cellmaster.stateupdate.exposure_interpreter import (
    interpret_exposure
)

from cellmaster.stateupdate.public_exposure import (
    build_public_exposure
)

from cellmaster.stateupdate.request_generator import (
    build_exposure_requests
)

from cellmaster.stateupdate.runtime_package import (
    build_runtime_package
)

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
       

# =========================================
# Runtime State Finalization Layer
# =========================================

class StateUpdater:

    """
    runtime state exposure/finalization layer

    responsibilities:
        - receive finalized runtime outputs
        - integrate runtime context
        - interpret outward exposure
        - build PublicExposure
        - generate intent requests
        - return finalized runtime package

    DOES NOT:
        - calculate physiology
        - execute behaviors
        - write world directly
    """

    def __init__(self):

        pass

    # =====================================
    # main update entry
    # =====================================

    def finalize(
        self,
        runtime_outputs,
        world,
        tick=None
    ):

        debug_print(
            f"[StateUpdate] tick={tick}"
        )

        finalized_packages = []

        for runtime_output in runtime_outputs:

            package = self.process_runtime_output(

                runtime_output,
                world,
                tick
            )

            if package is not None:

                finalized_packages.append(
                    package
                )

        debug_print(
            f"[StateUpdate] packages="
            f"{len(finalized_packages)}"
        )

        return finalized_packages

    # =====================================
    # single runtime processing
    # =====================================

    def process_runtime_output(
        self,
        runtime_output,
        world,
        tick
    ):

        cell_id = runtime_output.get(
            "cell_id"
        )

        # ---------------------------------
        # find cell
        # ---------------------------------

        cell = world.cells.get(
            cell_id
        )

        if cell is None:

            return None

        # =================================
        # integrate runtime context
        # =================================

        runtime_context = (
            integrate_runtime_context(
                runtime_output,
                cell,
                tick
            )
        )

        # =================================
        # interpret outward exposure
        # =================================

        interpreted_exposure = (
            interpret_exposure(
                runtime_context
            )
        )

        # =================================
        # build public exposure
        # =================================

        public_exposure = (
            build_public_exposure(
                interpreted_exposure
            )
        )

        # =================================
        # build outward intents
        # =================================

        exposure_requests = (
            build_exposure_requests(

                public_exposure,
                runtime_context,
                cell,
                tick
            )
        )

        # =================================
        # build finalized package
        # =================================

        runtime_package = (
            build_runtime_package(

                runtime_output=
                    runtime_output,

                runtime_context=
                    runtime_context,

                public_exposure=
                    public_exposure,

                exposure_requests=
                    exposure_requests,

                tick=tick
            )
        )

        return runtime_package
