# Scan_Master/event_loader.py

import os
import json

# =========================
# schema validation
# =========================
REQUIRED_KEYS = [
    "event_id",
    "type",
    "topology",
    "mode",
    "field",
    "source",
    "target",
    "value"
]

VALID_TYPES = {"signal", "effector", "binding"}
VALID_TOPOLOGY = {"cell-cell", "cell-substance", "substance-substance"}
VALID_MODE = {"contact", "field", "binding"}


def validate_event_schema(rule):

    # 必要字段
    for k in REQUIRED_KEYS:
        if k not in rule:
            raise ValueError(f"[EVENT SCHEMA ERROR] Missing key: {k}")

    # type
    if rule["type"] not in VALID_TYPES:
        raise ValueError(f"[EVENT SCHEMA ERROR] Invalid type: {rule['type']}")

    # topology
    if rule["topology"] not in VALID_TOPOLOGY:
        raise ValueError(f"[EVENT SCHEMA ERROR] Invalid topology: {rule['topology']}")

    # mode
    if rule["mode"] not in VALID_MODE:
        raise ValueError(f"[EVENT SCHEMA ERROR] Invalid mode: {rule['mode']}")

    # source / target
    if "type" not in rule["source"]:
        raise ValueError("[EVENT SCHEMA ERROR] source missing type")

    if "type" not in rule["target"]:
        raise ValueError("[EVENT SCHEMA ERROR] target missing type")

    return rule


# =========================
# loader
# =========================
def load_event_lib(folder):

    rules = []

    for fname in os.listdir(folder):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(folder, fname)

        with open(path, "r") as f:
            data = json.load(f)

            # 支持单个 or list
            if isinstance(data, list):
                for rule in data:
                    rules.append(validate_event_schema(rule))
            else:
                rules.append(validate_event_schema(data))

    print(f"[EVENT LOADER] Loaded {len(rules)} event rules")

    return rules
