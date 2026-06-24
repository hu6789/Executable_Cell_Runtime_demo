# test_passive_execution.py

from pprint import pprint

from cellmaster.internalnet.passive_engine.passive_engine import (
    PassiveEngine
)

from cellmaster.internalnet.passive_engine.passive_runtime_state import (
    build_passive_runtime_state
)


def test_passive_execution():

    print()
    print("============================")
    print("PASSIVE EXECUTION TEST")
    print("============================")
    print()

    # ---------------------------------
    # dummy passive
    # ---------------------------------

    passive_def = {

        "passive_name":
            "ATP_decay",

        "passive_formula": {

            "formula":
                "constant",

            "value":
                -1.0
        },

        "passive_gate": {

            "update_target":
                "ATP"
        },

        "involved_nodes": [
            "ATP"
        ]
    }

    runtime_context = {

        "tick": 1,

        "runtime_state": {

            "ATP": 10.0
        }
    }

    # ---------------------------------
    # execute passive
    # ---------------------------------

    engine = PassiveEngine()

    passive_results = (

        engine.process_all_passives(

            runtime_entity=None,

            runtime_context=
                runtime_context,

            passive_definitions=[
                passive_def
            ]
        )
    )

    print("PASSIVE RESULTS")
    pprint(passive_results)

    print()

    assert len(passive_results) == 1

    result = passive_results[0]

    # ---------------------------------
    # runtime state patch
    # ---------------------------------

    runtime_state_patch = (

        build_passive_runtime_state(

            passive_definition=
                passive_def,

            computed_delta=
                result.get(
                    "computed_value",
                    0.0
                ),

            transformed_delta=
                result.get(
                    "transformed_value",
                    0.0
                ),

            gate_result=
                result.get(
                    "gate_result",
                    {}
                ),

            runtime_context=
                runtime_context
        )
    )

    print("STATE PATCH")
    pprint(runtime_state_patch)

    print()

    assert (
        runtime_state_patch[
            "runtime_type"
        ]
        ==
        "passive_state"
    )

    assert (
        "state_patch"
        in runtime_state_patch
    )

    print("PASS")


if __name__ == "__main__":

    test_passive_execution()
