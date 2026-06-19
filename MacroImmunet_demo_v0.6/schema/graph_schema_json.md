{
    "_schema_name": "GraphSchema",

    "_description": [

        "Runtime Graph Definition",

        "Graph defines contribution topology.",

        "Graph connects runtime entities.",

        "Graph does NOT define node meaning.",

        "Graph does NOT define behavior meaning.",

        "NodeSchema defines node semantics.",

        "BehaviorSchema defines behavior semantics.",

        "Graph only defines information flow."
    ],

    "fields": {

        "name": {

            "type": "string",

            "description": [

                "Graph definition name.",

                "Examples:",

                "macrophage_graph",
                "tcell_graph",
                "virus_infected_cell_graph"
            ]
        },

        "graph_type": {

            "type": "enum",

            "description": [

                "Runtime graph category."
            ],

            "allowed_values": [

                "node_graph",
                "behavior_graph",
                "passive_graph",
                "viral_graph"
            ]
        },

        "nodes": {

            "type": "list[string]",

            "description": [

                "Definition names participating in graph.",

                "Graph does not own definitions.",

                "Definitions come from NodeSchema, BehaviorSchema, PassiveSchema, ViralSchema."
            ]
        },

        "edges": {

            "type": "list[edge]",

            "description": [

                "Contribution topology."
            ]
        },

        "runtime_enabled": {

            "type": "bool",

            "default": true
        },

        "metadata": {

            "type": "object",

            "description": [

                "Free-form documentation.",

                "Ignored by runtime."
            ]
        }
    },

    "edge_definition": {

        "description": [

            "Defines contribution flow between runtime entities."
        ],

        "fields": {

            "source": {

                "type": "string",

                "description": [

                    "Source definition name."
                ]
            },

            "target": {

                "type": "string",

                "description": [

                    "Target definition name."
                ]
            },

            "weight": {

                "type": "float",

                "default": 1.0
            },

            "transform": {

                "type": "enum",

                "allowed_values": [

                    "linear",
                    "sigmoid",
                    "relu",
                    "square",
                    "inverse",
                    "normalized",
                    "limiting"
                ]
            },

            "contribution_category": {

                "type": "enum",

                "description": [

                    "Contribution semantic category.",

                    "Consumed by NodeSkeleton and BehaviorSkeleton."
                ],

                "allowed_values": [

                    "activation",
                    "suppression",
                    "amplification",
                    "resource",
                    "damage",
                    "stabilization",
                    "destabilization"
                ]
            },

            "participation_requirement": {

                "type": "enum",

                "description": [

                    "Future contribution participation policy."
                ],

                "allowed_values": [

                    "optional",
                    "all_required",
                    "any_required"
                ]
            },

            "contribution_gate": {

                "type": "object",

                "description": [

                    "Runtime eligibility gate."
                ],

                "fields": {

                    "source": {

                        "type": "string"
                    },

                    "operator": {

                        "type": "enum",

                        "allowed_values": [

                            ">",
                            "<",
                            ">=",
                            "<=",
                            "==",
                            "range"
                        ]
                    },

                    "threshold": {

                        "type": "float"
                    },

                    "minimum": {

                        "type": "float"
                    },

                    "maximum": {

                        "type": "float"
                    }
                }
            },

            "runtime_enabled": {

                "type": "bool",

                "default": true
            },

            "metadata": {

                "type": "object"
            }
        }
    }
}
