{
    "_schema_name": "NodeSchema",

    "_description": "InternalNet Runtime Node Definition Schema",

    "_design_principle": [
        "Node defines physiological state variables",
        "Node does not define graph topology",
        "Node does not define contribution sources",
        "Graph edges define contribution sources",
        "Skeleton defines contribution computation structure"
    ],

    "fields": {

        "name": {
            "type": "string",

            "description":
                "Node definition name",

            "examples": [
                "ATP",
                "RNA",
                "protein",
                "ROS",
                "Ca",
                "cell_membrane",
                "ER_membrane"
            ]
        },

        "node_type": {

            "type": "enum",

            "description":
                "Semantic node category",

            "allowed_values": [

                {
                    "name": "continuous",

                    "description":
                        "Generic continuous variable"
                },

                {
                    "name": "resource",

                    "examples": [
                        "ATP",
                        "RNA",
                        "protein",
                        "amino_acid"
                    ]
                },

                {
                    "name": "signal",

                    "examples": [
                        "Ca",
                        "NFkB",
                        "STAT"
                    ]
                },

                {
                    "name": "damage",

                    "examples": [
                        "ROS",
                        "DNA_damage"
                    ]
                },

                {
                    "name": "structure",

                    "examples": [
                        "cell_membrane",
                        "ER_membrane"
                    ]
                },

                {
                    "name": "state",

                    "examples": [
                        "activation_state",
                        "stress_state"
                    ]
                }
            ]
        },

        "default_value": {

            "type": "float",

            "description":
                "Initial runtime value"
        },

        "runtime_enabled": {

            "type": "bool",

            "description":
                "Whether node participates in runtime"
        },

        "skeleton_formula": {

            "type": "enum",

            "description":
                "Abstract computation structure for node evaluation",

            "allowed_values": [

                {
                    "name": "drive_balance",

                    "formula":
                        "(activation - suppression) × amplification × resource + stabilization - destabilization"
                },

                {
                    "name": "activation_only",

                    "formula":
                        "activation"
                },

                {
                    "name": "suppression_balance",

                    "formula":
                        "activation - suppression"
                },

                {
                    "name": "resource_limited",

                    "formula":
                        "activation × resource - damage"
                },

                {
                    "name": "damage_integrated",

                    "formula":
                        "activation - damage - destabilization"
                },

                {
                    "name": "custom_formula",

                    "description":
                        "Reserved for future programmable formulas"
                }
            ]
        },

        "supported_contribution_categories": {

            "description":
                "Categories consumed by skeleton formulas",

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

        "runtime_gates": {

            "type": "list",

            "description":
                "Node-level activation gates",

            "allowed_gate_types": [

                {
                    "gate_type":
                        "minimum_activation",

                    "required_fields": [
                        "threshold"
                    ]
                },

                {
                    "gate_type":
                        "minimum_resource",

                    "required_fields": [
                        "threshold"
                    ]
                },

                {
                    "gate_type":
                        "maximum_damage",

                    "required_fields": [
                        "threshold"
                    ]
                },

                {
                    "gate_type":
                        "maximum_stress",

                    "required_fields": [
                        "source",
                        "threshold"
                    ]
                },

                {
                    "gate_type":
                        "minimum_node_value",

                    "required_fields": [
                        "threshold"
                    ]
                },

                {
                    "gate_type":
                        "custom_condition",

                    "description":
                        "Reserved for future extension"
                }
            ]
        },

        "runtime_clamp": {

            "description":
                "Runtime physiological limits",

            "fields": {

                "runtime_min": {
                    "type": "float"
                },

                "runtime_max": {
                    "type": "float"
                },

                "soft_clamp": {
                    "type": "bool"
                },

                "soft_limit": {
                    "type": "float"
                },

                "soft_compression": {
                    "type": "float"
                },

                "adaptive_clamp": {

                    "description":
                        "Runtime-dependent dynamic limits",

                    "fields": {

                        "source": {
                            "type": "string"
                        },

                        "scale": {
                            "type": "float"
                        },

                        "min": {
                            "type": "float"
                        },

                        "max": {
                            "type": "float"
                        }
                    }
                }
            }
        },

        "self_decay": {

            "description":
                "Natural node evolution outside graph contributions",

            "allowed_formulas": [

                {
                    "name": "none",

                    "description":
                        "No spontaneous change"
                },

                {
                    "name": "linear",

                    "formula":
                        "value - rate"
                },

                {
                    "name": "proportional",

                    "formula":
                        "value × (1 - rate)"
                },

                {
                    "name": "homeostatic",

                    "formula":
                        "value + (baseline - value) × recovery_rate"
                }
            ],

            "fields": {

                "formula": {
                    "type": "enum"
                },

                "rate": {
                    "type": "float"
                },

                "baseline": {
                    "type": "float"
                },

                "recovery_rate": {
                    "type": "float"
                }
            }
        },

        "metadata": {

            "type": "object",

            "description":
                "Free extension area for future runtime annotations"
        }
    }
}
