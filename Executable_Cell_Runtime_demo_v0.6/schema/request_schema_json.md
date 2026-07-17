{
    "_schema_name": "RequestSchema",

    "_description":
        "StateUpdate World Semantic Request Schema",

    "_design_principle": [

        "Request represents biological intent",

        "Request is generated before IntentBuilder",

        "Request preserves biological meaning",

        "IntentBuilder translates Request into world intents",

        "Different request types activate different payload fields"
    ],

    "fields": {

        "request_type": {

            "type": "enum",

            "allowed_values": [

                {
                    "name": "field",

                    "generated_by": [

                        "IFN_release",
                        "TNF_release",
                        "IL6_release"
                    ]
                },

                {
                    "name": "cell_state",

                    "generated_by": [

                        "ATP_production",
                        "ROS_cleanup",
                        "membrane_repair"
                    ]
                },

                {
                    "name": "label_flag",

                    "generated_by": [

                        "infection_progression",
                        "activation_state"
                    ]
                },

                {
                    "name": "targeted_directed",

                    "generated_by": [

                        "kill",
                        "attack",
                        "direct_signal"
                    ]
                },

                {
                    "name": "link",

                    "generated_by": [

                        "immune_synapse",
                        "binding"
                    ]
                },

                {
                    "name": "entity_lifecycle",

                    "generated_by": [

                        "divide",
                        "die",
                        "differentiate"
                    ]
                }
            ]
        },

        "request_source": {

            "type": "enum",

            "description":
                "Originating runtime subsystem",

            "allowed_values": [

                "behavior",
                "hir",
                "aip",
                "substance",
                "external"
            ]
        },

        "source_id": {

            "type": "string"
        },

        "position": {

            "type": "vector"
        },

        "strength": {

            "type": "float",

            "default": 1.0
        },

        "payload": {

            "type": "object",

            "description":
                "Request-type-specific payload"
        }
    },

    "payload_fields": {

        "field_type": {

            "used_by": [
                "field"
            ],

            "examples": [

                "IFN",
                "TNF",
                "IL6"
            ]
        },

        "release_amount": {

            "used_by": [
                "field"
            ]
        },

        "target_state": {

            "used_by": [
                "cell_state"
            ],

            "examples": [

                "ATP",
                "ROS",
                "cell_membrane"
            ]
        },

        "operation": {

            "used_by": [

                "cell_state",
                "label_flag",
                "link"
            ],

            "allowed_values": [

                "add",
                "remove",
                "multiply",
                "override",
                "create"
            ]
        },

        "value": {

            "used_by": [
                "cell_state"
            ]
        },

        "label": {

            "used_by": [
                "label_flag"
            ]
        },

        "target_id": {

            "used_by": [

                "targeted_directed",
                "link"
            ]
        },

        "action": {

            "used_by": [

                "targeted_directed",
                "entity_lifecycle"
            ]
        },

        "link_type": {

            "used_by": [
                "link"
            ]
        },

        "target_cell_type": {

            "used_by": [
                "entity_lifecycle"
            ]
        },

        "count": {

            "used_by": [
                "entity_lifecycle"
            ]
        }
    }
}
