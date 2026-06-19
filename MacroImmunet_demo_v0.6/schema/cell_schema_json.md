{
  "_schema_name": "CellTemplateSchema",

  "_description": [

    "Static Cell Definition.",

    "CellTemplate defines biological identity.",

    "CellTemplate defines graph references.",

    "CellTemplate defines initialization defaults.",

    "CellTemplate does NOT execute runtime logic.",

    "CellTemplate does NOT store runtime state.",

    "CellTemplate does NOT define node semantics.",

    "CellTemplate does NOT define behavior semantics.",

    "Node semantics come from NodeSchema.",

    "Behavior semantics come from BehaviorSchema.",

    "Graph topology comes from GraphSchema."
  ],

  "fields": {

    "template_id": {

      "type": "string",

      "description": [

        "Unique template identifier.",

        "Examples:",

        "cd8_effector",

        "cd4_helper",

        "macrophage_m1",

        "epithelial_cell"
      ]
    },

    "identity": {

      "type": "object",

      "description": [

        "Biological identity definition."
      ],

      "fields": {

        "cell_type": {

          "type": "string",

          "description": [

            "Primary cell type.",

            "Examples:",

            "cd8_t",

            "cd4_t",

            "b_cell",

            "macrophage",

            "epithelial"
          ]
        },

        "subtype": {

          "type": "string",

          "description": [

            "Subtype or specialization.",

            "Examples:",

            "naive",

            "activated",

            "effector",

            "memory",

            "m1",

            "m2"
          ]
        },

        "lineage": {

          "type": "string",

          "description": [

            "Cell lineage.",

            "Examples:",

            "t_cell",

            "b_cell",

            "myeloid",

            "epithelial"
          ]
        },

        "species": {

          "type": "string",

          "description": [

            "Biological species.",

            "Examples:",

            "human",

            "mouse"
          ]
        }
      }
    },

    "graph_refs": {

      "type": "object",

      "description": [

        "Runtime graph assembly references.",

        "Referenced graphs are merged during RuntimeAssembler."
      ],

      "fields": {

        "base": {

          "type": "list[string]",

          "description": [

            "Core physiology graphs.",

            "Examples:",

            "cell_core",

            "immune_core"
          ]
        },

        "specific": {

          "type": "list[string]",

          "description": [

            "Cell-specific graphs.",

            "Examples:",

            "cd8_effector",

            "plasma_bcell",

            "macrophage_m1"
          ]
        },

        "lineage_shared": {

          "type": "list[string]",

          "description": [

            "Shared lineage graphs.",

            "Future extension.",

            "Examples:",

            "tcell_common",

            "myeloid_common"
          ]
        }
      }
    },

    "init_node_state": {

      "type": "object",

      "description": [

        "Initial runtime node values.",

        "Used when RuntimeState is created.",

        "Keys should reference NodeSchema names."
      ],

      "example": {

        "ATP": 100.0,

        "RNA": 50.0,

        "Protein": 80.0,

        "ROS": 0.1
      }
    },

    "hir_capabilities": {

      "type": "object",

      "description": [

        "HIR configuration references.",

        "Defines which HIR profile governs this cell."
      ],

      "fields": {

        "hir_profile": {

          "type": "string",

          "description": [

            "HIR profile name.",

            "Examples:",

            "default_cd8",

            "default_macrophage",

            "default_epithelial"
          ]
        }
      }
    },

    "exposure_rules": {

      "type": "object",

      "description": [

        "Exposure profile references.",

        "Controls public observability."
      ],

      "fields": {

        "exposure_profile": {

          "type": "string",

          "description": [

            "Exposure profile name.",

            "Examples:",

            "immune_default",

            "infected_cell",

            "silent_cell"
          ]
        }
      }
    },

    "runtime_params": {

      "type": "object",

      "description": [

        "Cell-specific runtime modifiers.",

        "Used for parameter tuning.",

        "Does not define biology."
      ],

      "fields": {

        "metabolic_scale": {

          "type": "float",

          "default": 1.0,

          "description": [

            "Global metabolic multiplier."
          ]
        },

        "signal_sensitivity": {

          "type": "float",

          "default": 1.0,

          "description": [

            "Signal responsiveness multiplier."
          ]
        },

        "volume": {

          "type": "float",

          "default": 1.0,

          "description": [

            "Relative cell volume."
          ]
        }
      }
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
  }
}
