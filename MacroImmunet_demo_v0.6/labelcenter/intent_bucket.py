# labelcenter/intent_bucket.py

from collections import defaultdict


# =========================================
# v0.6 Intent Bucket System
# =========================================

VALID_WRITE_MODES = {

    "cell_state",
    "runtime_state",
    "label_flag",
    "field",
    "targeted_directed",
    "link",
    "entity_lifecycle"

}


# =========================================
# create empty buckets
# =========================================

def create_empty_buckets():

    return {
        "cell_state": [],
        "runtime_state": [],
        "label_flag": [],
        "field": [],
        "targeted_directed": [],
        "link": [],
        "entity_lifecycle": []
    }


# =========================================
# bucket intents by write_mode
# =========================================

def bucket_intents(intents):

    buckets = create_empty_buckets()

    invalid_intents = []

    for intent in intents:

        mode = intent.get("write_mode")

        if mode not in VALID_WRITE_MODES:
            invalid_intents.append(intent)
            continue

        buckets[mode].append(intent)

    return buckets, invalid_intents
