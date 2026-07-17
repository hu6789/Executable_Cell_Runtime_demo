# test_adaptive_immunity_demo.py

from pprint import pprint

from demo.minidemo import (
    MiniDemo
)

from demo.scenario.adaptive_immunity_demo import (
    AdaptiveImmunityDemo
)


# ==========================================================
# Build Demo
# ==========================================================

print("\n================ BUILD DEMO ================\n")

demo = MiniDemo()

scenario = AdaptiveImmunityDemo()

demo.build(
    scenario
)


# ==========================================================
# Run
# ==========================================================

print("\n================ RUN ================\n")

ticks = scenario.runtime_options().get(
    "ticks",
    5
)

demo.run(
    ticks
)


# ==========================================================
# Verify Runtime
# ==========================================================

print("\n================ RUNTIME ================\n")

print(
    f"Current Tick : {demo.tick}"
)

print(
    f"Timeline Size: {len(demo.timeline)}"
)


# ==========================================================
# Latest Snapshot
# ==========================================================

print("\n================ SNAPSHOT ================\n")

record = demo.latest

if record is not None:

    pprint(record.snapshot)

    print()

    pprint(record.statistics)


# ==========================================================
# Timeline
# ==========================================================

print("\n================ TIMELINE ================\n")

for record in demo.timeline:

    print(

        f"Tick {record.tick}"

    )


# ==========================================================
# Assertions
# ==========================================================

assert demo.tick == ticks

assert len(demo.timeline) == ticks

assert demo.latest is not None

print("\nAll assertions passed.")


# ==========================================================
# DONE
# ==========================================================

print("\n================ DONE ================\n")


from visualization.viewer_builder import launch_viewer

launch_viewer(

    demo.observer.visualization.snapshots,

    "Adaptive Immunity"

)

