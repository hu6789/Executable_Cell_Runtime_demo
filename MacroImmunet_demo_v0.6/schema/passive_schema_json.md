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

            "type": "string",

            "description": [

                "Unique passive definition name.",

                "Examples:",

                "ATP_decay",

                "ROS_overload",

                "Ca_flux",

                "viral_uncoating"
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

                "Used for organization and editor display only.",

                "Does not affect runtime execution."
            ]
        },

        "runtime_enabled": {

            "type": "bool",

            "default": true,

            "description": [

                "Whether this passive participates in runtime execution."
            ]
        },

        "involved_nodes": {

            "type": "list[string]",

            "description": [

                "Nodes read by this passive.",

                "Acts as runtime dependency declaration.",

                "These nodes are available to formula evaluation."
            ]
        },

        "update_target": {

            "type": "string",

            "description": [

                "Target node updated by passive result.",

                "Passive output is applied to this node.",

                "Must reference a valid runtime node."
            ]
        },

        "update_mode": {

            "type": "enum",

            "allowed_values": [

                "add",

                "subtract",

                "replace"
            ],

            "default": "add",

            "description": [

                "How passive result is applied to update_target."
            ]
        },

        "formula": {

            "type": "object",

            "description": [

                "Passive computation definition."
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
                },

                "source": {

                    "type": "string",

                    "description": [

                        "Primary source node."
                    ]
                },

                "stress": {

                    "type": "string",

                    "description": [

                        "Stress source node."
                    ]
                },

                "repair": {

                    "type": "string",

                    "description": [

                        "Repair source node."
                    ]
                },

                "instability_source": {

                    "type": "string",

                    "description": [

                        "Secondary instability node."
                    ]
                },

                "activity": {

                    "type": "string",

                    "description": [

                        "Activity node used by resource consumption."
                    ]
                },

                "load": {

                    "type": "string",

                    "description": [

                        "Load node used by resource consumption."
                    ]
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
                }
            }
        },

        "passive_gate": {

            "type": "object",

            "description": [

                "Execution gate evaluated before formula runtime."
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

                "Post-processing after formula evaluation."
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

            "type": "object",

            "description": [

                "Documentation fields.",

                "Ignored by runtime."
            ]
        }
    }
}
