# test_stateupdate_external_requests.py

from pprint import pprint

from cellmaster.stateupdate.context_integrator import (
    integrate_runtime_context
)


# ==========================================================
# Dummy Cell
# ==========================================================

class DummyCell:

    def __init__(self):

        self.label_flags = {}


# ==========================================================
# IL2 Release
# ==========================================================

def test_il2_release():

    print()
    print("=" * 60)
    print("TEST: IL2 release external request")
    print("=" * 60)

    runtime_output = {

        "cell_id": "cd4_001",

        "modulated_runtime_state": {

            "ATP": 100.0,
            "IL2": 10.0

        },

        "hir_output": {

            "state_labels": []

        },

        "behavior_output": {

            "merged_physiological_cost": {

                "ATP": -1.0

            },

            "merged_internal_outputs": {},

            "behavior_packages": [],

            "external_requests": [

                {

                    "request_type": "secrete",

                    "payload": {

                        "substance": "IL2"

                    }

                }

            ]

        }

    }

    context = integrate_runtime_context(

        runtime_output,

        DummyCell(),

        tick=0

    )

    pprint(context)

    requests = context["external_requests"]

    assert len(requests) == 1

    assert requests[0]["request_type"] == "secrete"

    assert requests[0]["payload"]["substance"] == "IL2"

    print()

    print("IL2 release PASS")


# ==========================================================
# Chemotaxis
# ==========================================================

def test_chemotaxis():

    print()
    print("=" * 60)
    print("TEST: Chemotaxis external request")
    print("=" * 60)

    runtime_output = {

        "cell_id": "cd4_001",

        "modulated_runtime_state": {

            "ATP": 100.0,
            "CXCR3": 20.0

        },

        "hir_output": {

            "state_labels": []

        },

        "behavior_output": {

            "merged_physiological_cost": {

                "ATP": -0.5

            },

            "merged_internal_outputs": {},

            "behavior_packages": [],

            "external_requests": [

                {

                    "request_type": "move",

                    "payload": {

                        "mode": "chemotaxis"

                    }

                }

            ]

        }

    }

    context = integrate_runtime_context(

        runtime_output,

        DummyCell(),

        tick=0

    )

    pprint(context)

    requests = context["external_requests"]

    assert len(requests) == 1

    assert requests[0]["request_type"] == "move"

    assert requests[0]["payload"]["mode"] == "chemotaxis"

    print()

    print("Chemotaxis PASS")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    test_il2_release()

    test_chemotaxis()

    print()
    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
