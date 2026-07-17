# test_behavior_internal_outputs.py

from pprint import pprint

from cellmaster.stateupdate.context_integrator import (
    integrate_runtime_context
)


# =========================================
# Dummy Cell
# =========================================

class DummyCell:

    def __init__(self):

        self.label_flags = {}
        
# =========================================
# Test IL2 Production
# =========================================

def test_il2_production():

    print()
    print("=" * 60)
    print("TEST: IL2 production internal output")
    print("=" * 60)


    runtime_output = {


        "cell_id":
            "cd4_001",


        "modulated_runtime_state": {

            "ATP":100.0,

            "IL2":0.0,

            "TCR":20.0,

            "amino_acid":100.0

        },


        "hir_output": {

            "state_labels":[]

        },


        "behavior_output": {


            "merged_physiological_cost": {

                "ATP": -5.0

            },


            "merged_internal_outputs": {

                "IL2":10.0

            },


            "behavior_packages":[],

            "external_requests":[]

        }

    }


    context = integrate_runtime_context(

        runtime_output,

        DummyCell(),

        tick=0

    )


    pprint(context)


    projected = context[

        "projected_runtime_state"

    ]


    assert projected["ATP"] == 95.0

    assert projected["IL2"] == 10.0
    
    assert context["runtime_labels"]["activated"] is False

    print()

    print("IL2 production PASS")
    
# =========================================
# Main
# =========================================

if __name__ == "__main__":

    test_il2_production()

    print()

    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
