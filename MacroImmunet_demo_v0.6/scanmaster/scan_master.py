# scanmaster/scan_master.py

from scanmaster.topology_scan import (
    scan_topology
)

from scanmaster.interaction_classifier import (
    classify_interactions
)

from scanmaster.event_gating import (
    gate_events
)

from scanmaster.event_standardizer import (
    standardize_events
)


# =========================================
# ScanMaster
# =========================================

class ScanMaster:

    """
    World Topology Scan Layer

    responsibilities:
        - scan topology
        - classify interactions
        - gate biological events
        - standardize events

    does NOT:
        - modify world
        - generate intents
        - perform cell decisions
    """

    def __init__(self):

        self.event_buffer = []

    # =====================================
    # main scan pipeline
    # =====================================

    def scan(
        self,
        world,
        tick
    ):

        print(
            f"\n[ScanMaster] tick={tick}"
        )

        # ---------------------------------
        # topology scan
        # ---------------------------------

        topology_events = scan_topology(
            world,
            tick
        )

        print(

            f"[ScanMaster] topology="
            f"{len(topology_events)}"
        )

        # ---------------------------------
        # interaction classification
        # ---------------------------------

        classified = classify_interactions(
            topology_events
        )

        print(

            f"[ScanMaster] classified="
            f"{len(classified)}"
        )

        # ---------------------------------
        # biological gating
        # ---------------------------------

        gated = gate_events(
            classified
        )

        print(

            f"[ScanMaster] gated="
            f"{len(gated)}"
        )

        # ---------------------------------
        # event standardization
        # ---------------------------------

        standardized = standardize_events(
            gated
        )

        print(

            f"[ScanMaster] standardized="
            f"{len(standardized)}"
        )

        # ---------------------------------
        # buffer
        # ---------------------------------

        self.event_buffer.extend(
            standardized
        )

        return standardized
