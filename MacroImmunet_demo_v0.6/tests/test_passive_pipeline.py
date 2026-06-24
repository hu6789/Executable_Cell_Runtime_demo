# test_passive_pipeline.py

from pprint import pprint

from cellmaster.internalnet.passive_engine.passive_engine import (
    PassiveEngine
)

from cellmaster.internalnet.passive_engine.passive_runtime_state import (
    build_passive_runtime_state
)


def test_passive_pipeline():

    print()
    print("============================")
    print("PASSIVE PIPELINE TEST")
    print("============================")

    # ----------------------------------
    # fake node runtime state
    # ----------------------------------

    node_runtime_state = {

        "ATP": 100.0,
        "ROS": 10.0
    }

    print()
    print("NODE STATE")

    pprint(node_runtime_state)

    # ----------------------------------
    # fake passive result
    # ----------------------------------

    passive_definition = {

        "name": "ATP_decay",

        "passive_gate": {

            "update_target": "ATP"
        }
    }

    passive_result = {

        "target_node": "ATP",

        "computed_value": -10.0,

        "transformed_value": -10.0,

        "gate_passed": True
    }

    passive_results = [

        passive_result
    ]

    # ----------------------------------
    # apply passive
    # ----------------------------------

    engine = PassiveEngine()

    passive_runtime_state = (

        engine.apply_passive_state(

            node_runtime_state.copy(),

            passive_results
        )
    )

    print()
    print("PASSIVE STATE")

    pprint(passive_runtime_state)

    print()
    print("ASSERTIONS")

    assert passive_runtime_state["ATP"] == 90.0

    assert node_runtime_state["ATP"] == 100.0

    print("PASS")


if __name__ == "__main__":

    test_passive_pipeline()
