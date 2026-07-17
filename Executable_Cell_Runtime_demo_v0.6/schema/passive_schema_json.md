{
    "_schema_name": "PassiveSchema",

    "_description": [

        "Static Passive Process Definition.",

        "Passive defines deterministic physiological dynamics.",

        "Passive represents chemistry, physics, degradation, leakage, diffusion and homeostasis.",

        "Passive does NOT perform decision making.",

        "Passive does NOT compete with behaviors.",

        "Passive does NOT generate intents.",

        "Passive does NOT modify world state directly.",

        "Passive produces runtime state patches.",

        "Passive executes after Node Runtime and before Modulation Runtime."
    ],

    "fields": {

        "name": {
            "type": "string"
        },

        "passive_type": {
            "type": "enum",

            "allowed_values": [

                "decay",
                "consumption",
                "accumulation",
                "leakage",
                "diffusion",
                "instability",
                "maintenance",
                "custom"
            ]
        },

        "runtime_enabled": {

            "type": "bool",

            "default": true
        },

        "involved_nodes": {

            "type": "list[string]"
        },

        "formula": {

            "type": "object",

            "fields": {

                "type": {

                    "type": "enum",

                    "allowed_values": [

                        "linear_decay",

                        "proportional_leakage",

                        "exponential_accumulation",

                        "resource_consumption",

                        "membrane_instability",

                        "calcium_influx",

                        "custom_formula"
                    ]
                },

                "source": {
                    "type": "string"
                },

                "stress": {
                    "type": "string"
                },

                "repair": {
                    "type": "string"
                },

                "instability_source": {
                    "type": "string"
                },

                "activity": {
                    "type": "string"
                },

                "load": {
                    "type": "string"
                },

                "decay_rate": {
                    "type": "float"
                },

                "leakage_rate": {
                    "type": "float"
                },

                "growth_rate": {
                    "type": "float"
                },

                "consumption_rate": {
                    "type": "float"
                },

                "instability_factor": {
                    "type": "float"
                },

                "flux_rate": {
                    "type": "float"
                },

                "max_integrity": {
                    "type": "float"
                }
            }
        },

        "outputs": {

            "type": "list[object]",

            "description": [

                "Runtime state patches produced by this passive.",

                "One passive may update multiple runtime nodes.",

                "Each output is applied independently."
            ],

            "fields": {

                "target": {

                    "type": "string",

                    "description": [

                        "Runtime node to modify."
                    ]
                },

                "mode": {

                    "type": "enum",

                    "allowed_values": [

                        "add",

                        "subtract",

                        "replace"
                    ],

                    "default": "add"
                },

                "scale": {

                    "type": "float",

                    "default": 1.0,

                    "description": [

                        "Optional multiplier applied after transform."
                    ]
                }
            }
        },

        "passive_gate": {

            "type": "object",

            "fields": {

                "required_nodes": {

                    "type": "list[string]"
                },

                "required_labels": {

                    "type": "list[string]"
                },

                "blocked_labels": {

                    "type": "list[string]"
                },

                "minimum_value": {

                    "type": "float"
                }
            }
        },

        "passive_transform": {

            "type": "object",

            "fields": {

                "transform": {

                    "type": "enum",

                    "allowed_values": [

                        "none",

                        "linear",

                        "normalized",

                        "sigmoid",

                        "limiting",

                        "clamp"
                    ]
                },

                "minimum": {
                    "type": "float"
                },

                "maximum": {
                    "type": "float"
                },

                "limit": {
                    "type": "float"
                }
            }
        },

        "metadata": {

            "type": "object"
        }
    }
}
