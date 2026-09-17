from typing import Dict, Set

from internalnet.node_engine.schema import NodeRuntimeState


class LabelDetermination:

    def determine(
        self,
        node_states: Dict[str, NodeRuntimeState],
        node_definitions: Dict[str, Dict],
    ) -> Set[str]:

        labels = set()

        for node_name, definition in node_definitions.items():

            if isinstance(definition, dict):
                category = definition.get("category")
            else:
                category = definition.category

            if category != "receptor":
                continue

            state = node_states.get(node_name)

            if state is None:
                continue

            if state.total > 0.0:
                labels.add(node_name)

        return labels
