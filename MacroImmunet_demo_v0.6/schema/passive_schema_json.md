{
    "_schema_name": "PassiveSchema",

    "_description": [

        "Static Passive Process Definition.",

        "Passive defines fixed physiological dynamics.",

        "Passive computes deterministic biological effects.",

        "Passive does NOT perform decision making.",

        "Passive does NOT compete with behaviors.",

        "Passive does NOT execute world actions.",

        "Passive does NOT generate intents.",

        "Passive represents chemistry, physics, and homeostasis.",

        "Examples include ATP decay, ROS clearance, membrane leakage, and cytokine diffusion."
    ],

    "fields": {

        "name": {

            "type": "string",

            "description": [

                "Unique passive definition name.",

                "Examples:",

                "ATP_decay",

                "ROS_clearance",

                "Ca_leakage",

                "Protein_degradation",

                "Membrane_instability"
            ]
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
            ],

            "description": [

                "Passive semantic category.",

                "Used for organization and editor display.",

                "Does not affect runtime execution."
            ]
        },

        "runtime_enabled": {

            "type": "bool",

            "default": true,

            "description": [

                "Whether this passive process participates in runtime."
            ]
        },

        "involved_nodes": {

            "type": "list[string]",

            "description": [

                "Nodes read by this passive process.",

                "References NodeSchema definitions.",

                "Examples:",

                "ATP",

                "ROS",

                "cell_membrane",

                "Ca"
            ]
        },
        "update_target": {

            "type": "string",

            "description": [

                "Node updated by passive result.",

                "Passive delta will be applied to this node.",

                "Must reference a valid NodeSchema node."
            ]
        },
        "formula": {

            "type": "object",

            "description": [

                "Passive computation definition.",

                "Determines how passive delta is calculated."
            ],

            "fields": {

                "type": {

                    "type": "enum",

                    "allowed_values": [

                        "linear_decay",

                        "proportional_leakage",

                        "exponential_accumulation",

                        "resource_consumption",

                        "membrane_instability",

                        "custom_formula"
                    ]
                }
            }
        },

        "passive_gate": {

            "type": "object",

            "description": [

                "Activation requirements for passive execution.",

                "Evaluated before formula execution."
            ],

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

            "description": [

                "Post-processing applied after formula evaluation."
            ],

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
                }
            }
        },
        
        "update_mode": {

            "type": "enum",

            "allowed_values": [

                "add",

                "subtract",

                "replace"
            ],

            "default": "add"
        }

        "metadata": {

            "type": "object",

            "description": [

                "Documentation fields.",

                "Ignored by runtime."
            ]
        }
    }
}
