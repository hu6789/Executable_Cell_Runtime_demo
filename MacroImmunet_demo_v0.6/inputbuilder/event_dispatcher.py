# inputbuilder/event_dispatcher.py

from collections import defaultdict


# =========================================
# dispatch events by target
# =========================================

def dispatch_events(
    events
):

    """
    regroup standardized events
    by perception target

    output:

        {
            target_id: [
                events...
            ]
        }
    """

    grouped = defaultdict(list)

    for event in events:

        target_id = event.get(
            "target_id"
        )

        # ---------------------------------
        # skip invalid
        # ---------------------------------

        if target_id is None:

            continue

        grouped[target_id].append(
            event
        )

    return dict(grouped)
