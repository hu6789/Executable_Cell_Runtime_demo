REGISTRY = {

    "IL2": {
        "interaction": {
            "type": "signal",
            "topology": "cell-substance",
            "mode": "field"
        },
        "translation": {
            "node": "IL2_signal"
        }
    },

    "pMHC": {
        "interaction": {
            "type": "binding",   # 🔴 改这里
            "topology": "cell-cell",
            "mode": "contact"
        },
        "translation": {
            "node": "TCR_signal"
        }
    },

    "perforin": {
        "interaction": {
            "type": "effector",
            "topology": "cell-substance",
            "mode": "contact",
            "target_filter": ["infected"]
        },

        "substance": {
            "handler": "perforin_master"
        }
    }
}
