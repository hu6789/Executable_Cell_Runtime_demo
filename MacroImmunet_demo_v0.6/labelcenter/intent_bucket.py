# labelcenter/intent_bucket.py

"""
LabelCenter Intent Bucket

Responsibilities
----------------
- classify intents by write_mode
- create stable buckets for LabelCenter apply pipeline
- separate invalid intents

DOES NOT
--------
- aggregate intents
- execute world updates
- validate payload semantics
"""

from typing import Dict, List, Tuple


# ==========================================================
# Supported write modes
# ==========================================================

VALID_WRITE_MODES = {

    "runtime_state",

    "field",

    "entity",

    "substance",

    "event",

    "targeted_directed",

    "link",

    "label"

}


# ==========================================================
# Bucket Factory
# ==========================================================

def create_empty_buckets() -> Dict[str, List[dict]]:

    return {

        mode: []

        for mode in VALID_WRITE_MODES

    }


# ==========================================================
# Bucket Intents
# ==========================================================

def bucket_intents(
    intents: List[dict]
) -> Tuple[
    Dict[str, List[dict]],
    List[dict]
]:

    buckets = create_empty_buckets()

    invalid = []

    for intent in intents:

        mode = intent.get(
            "write_mode"
        )

        if mode not in VALID_WRITE_MODES:

            invalid.append(intent)

            continue

        buckets[mode].append(intent)

    return buckets, invalid
