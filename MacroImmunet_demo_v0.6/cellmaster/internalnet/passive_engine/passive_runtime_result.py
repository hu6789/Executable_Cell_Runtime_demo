# cellmaster/internalnet/passive_engine/passive_runtime_result.py

def build_passive_runtime_result(
    passive_definition,
    computed_value,
    transformed_value,
    gate_result,
    runtime_metadata=None
):

    passive_name = passive_definition.get("name", "unknown_passive")

    return {
        "runtime_type": "passive",
        "passive_name": passive_name,

        # ✅ FIX: 关键字段补上
        "target_node": passive_definition.get("update_target"),

        "computed_value": computed_value,
        "transformed_value": transformed_value,

        "gate_passed": gate_result.get("gate_passed", True),

        "runtime_metadata": runtime_metadata or {}
    }


def build_passive_runtime_metadata(passive_definition, tick=None):

    return {
        "tick": tick,
        "formula": passive_definition.get("formula", {}),
        "transform": passive_definition.get("passive_transform", {}),
        "gate": passive_definition.get("passive_gate", {})
    }
