{
  "_schema_name": "SubstanceTemplateSchema",

  "_description": [

    "Static Substance Definition.",

    "SubstanceTemplate defines biochemical identity.",

    "SubstanceTemplate defines runtime defaults.",

    "SubstanceTemplate defines dynamics configuration.",

    "SubstanceTemplate defines interaction capabilities.",

    "SubstanceTemplate does NOT execute runtime logic.",

    "SubstanceTemplate does NOT store runtime state.",

    "SubstanceTemplate does NOT perform diffusion.",

    "SubstanceTemplate does NOT perform decay.",

    "SubstanceDynamicsEngine executes world-side dynamics.",

    "SubstanceMaster executes active interactions."
  ],

  "fields": {

    "template_id": {

      "type": "string",

      "description": [

        "Unique template identifier.",

        "Examples:",

        "ifn_alpha",

        "tnf_alpha",

        "il6",

        "perforin",

        "granzyme_b",

        "fasl"
      ]
    },

    "identity": {

      "type": "object",

      "description": [

        "Biochemical identity definition."
      ],

      "fields": {

        "substance_type": {

          "type": "string",

          "description": [

            "Primary substance type.",

            "Examples:",

            "IFN_alpha",

            "TNF_alpha",

            "IL6",

            "Perforin",

            "GranzymeB",

            "FasL"
          ]
        },

        "category": {

          "type": "string",

          "description": [

            "Functional category.",

            "Examples:",

            "cytokine",

            "chemokine",

            "effector",

            "toxin",

            "viral_particle"
          ]
        },

        "species": {

          "type": "string",

          "description": [

            "Biological origin.",

            "Examples:",

            "human",

            "mouse",

            "generic"
          ]
        }
      }
    },

    "runtime_defaults": {

      "type": "object",

      "description": [

        "Initial runtime state.",

        "Used when SubstanceEntity is created."
      ],

      "fields": {

        "default_amount": {

          "type": "float",

          "default": 100.0,

          "description": [

            "Initial amount."
          ]
        },

        "active": {

          "type": "bool",

          "default": true,

          "description": [

            "Whether interaction logic is enabled."
          ]
        }
      }
    },

    "dynamics": {

      "type": "object",

      "description": [

        "World-side autonomous updates.",

        "Executed by DynamicsEngine."
      ],

      "fields": {

        "diffusion": {

          "type": "object",

          "fields": {

            "enabled": {

              "type": "bool",

              "default": true
            },

            "fraction": {

              "type": "float",

              "default": 0.2,

              "description": [

                "Fraction distributed each tick."
              ]
            },

            "directions": {

              "type": "int",

              "default": 4,

              "description": [

                "Neighbor count used by diffusion."
              ]
            }
          }
        },

        "decay": {

          "type": "object",

          "fields": {

            "enabled": {

              "type": "bool",

              "default": true
            },

            "rate": {

              "type": "float",

              "default": 0.05,

              "description": [

                "Fraction removed each tick."
              ]
            }
          }
        },

        "aggregation": {

          "type": "object",

          "fields": {

            "enabled": {

              "type": "bool",

              "default": true
            },

            "distance": {

              "type": "float",

              "default": 1.0,

              "description": [

                "Merge radius."
              ]
            }
          }
        },

        "cleanup": {

          "type": "object",

          "fields": {

            "minimum_amount": {

              "type": "float",

              "default": 1.0,

              "description": [

                "Entities below threshold are removed."
              ]
            }
          }
        }
      }
    },

    "interaction": {

      "type": "object",

      "description": [

        "Active interaction definition.",

        "Executed by SubstanceMaster."
      ],

      "fields": {

        "interaction_mode": {

          "type": "string",

          "description": [

            "Interaction mode.",

            "Examples:",

            "passive",

            "active"
          ]
        },

        "interaction_rules": {

          "type": "list[object]",

          "description": [

            "Active interaction rules."
          ],

          "example": [

            {

              "rule_id":
                "perforin_membrane_damage",

              "target_type":
                "cell",

              "effect_type":
                "membrane_damage",

              "base_strength":
                1.0
            }
          ]
        }
      }
    },

    "runtime_params": {

      "type": "object",

      "description": [

        "Substance-specific tuning parameters.",

        "Does not define biology."
      ],

      "fields": {

        "strength_scale": {

          "type": "float",

          "default": 1.0
        },

        "interaction_radius": {

          "type": "float",

          "default": 1.0
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
