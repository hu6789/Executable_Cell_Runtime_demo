# demo/demo_main.py

"""
=========================================================
MacroImmunet Demo Entry
=========================================================

Example entry point for running a demo scenario.

Responsibilities
----------------
- create MiniDemo
- load scenario
- execute simulation

DOES NOT
--------
- implement simulation logic
- modify runtime
- access LabelCenter directly
"""

from demo.minidemo import (
    MiniDemo
)

from demo.scenario.infection_demo import (
    InfectionDemo
)


def main():

    #
    # Build demo
    #

    demo = MiniDemo()

    scenario = InfectionDemo()

    print()

    print("=" * 60)
    print("MacroImmunet Demo")
    print("=" * 60)

    print()

    print(f"Scenario : {scenario.name}")

    #
    # Build world
    #

    demo.build(

        scenario

    )

    #
    # Runtime options
    #

    options = scenario.runtime_options()

    ticks = options.get(

        "ticks",

        10

    )

    print(

        f"Ticks    : {ticks}"

    )

    print()

    #
    # Run simulation
    #

    demo.run(

        ticks

    )

    print()

    print("=" * 60)
    print("Simulation Finished")
    print("=" * 60)

    print()

    print(

        f"Executed ticks : {demo.tick}"

    )

    print(

        f"Timeline size  : {len(demo.timeline)}"

    )


if __name__ == "__main__":

    main()
