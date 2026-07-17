# cellmaster/stateupdate/runtime_package.py


# =========================================
# build finalized runtime package
# =========================================

def build_runtime_package(

    runtime_output,
    runtime_context,
    public_exposure,
    exposure_requests,
    tick=None
):

    """
    finalized outward runtime package

    returned by StateUpdate layer
    """

    return {

        # ---------------------------------
        # runtime identity
        # ---------------------------------

        "cell_id":
            runtime_output.get(
                "cell_id"
            ),

        "cell_type":
            runtime_output.get(
                "cell_type"
            ),

        "tick": tick,

        # ---------------------------------
        # finalized runtime state
        # ---------------------------------

        "runtime_context":
            runtime_context,

        # ---------------------------------
        # outward readable exposure
        # ---------------------------------

        "public_exposure":
            public_exposure,
        
        "projected_runtime_state":
            runtime_context.get(
                "projected_runtime_state",
                {}
            ),

        # ---------------------------------
        # outward requests
        # ---------------------------------

        "intent_requests":
            exposure_requests,

        # ---------------------------------
        # raw runtime output
        # ---------------------------------

        "runtime_output":
            runtime_output
    }
