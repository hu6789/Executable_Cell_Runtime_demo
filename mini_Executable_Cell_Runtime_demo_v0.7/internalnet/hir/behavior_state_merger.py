from typing import Dict

from internalnet.hir.schema import (
    BehaviorIntention,
    BehaviorRuntimeState,
    ResourceDelta,
    TFRegulationDelta,
)
from internalnet.runtime.state import GeneState, NodeState


class BehaviorStateMerger:

    def merge(
        self,
        intention,
        tf_delta,
        resource_delta,
        node_states,
        gene_states,
        source_type,
        source_name,
        internal_outputs=None,
    ) -> BehaviorRuntimeState:

        value = (
            intention.value
            + resource_delta.delta
        )

        return BehaviorRuntimeState(
            behavior_name=intention.behavior_name,
            source_type=source_type,
            source_name=source_name,
            node_states=dict(node_states),
            gene_states=dict(gene_states),
            value=value,
            internal_outputs=internal_outputs or {},
        )
