from copy import deepcopy

from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import NodeState, GeneState

from internalnet.runtime.delta import (
    NodeDelta,
    GeneDelta,
    PassiveDelta,
    BehaviorInternalDelta,
)


class RuntimeMerger:
    """
    Merge engine outputs into Runtime.

    RuntimeMerger does not calculate biology.
    It only applies deltas.
    """


    def merge_node(
        self,
        runtime: Runtime,
        delta: NodeDelta,
    ) -> Runtime:

        new_runtime = deepcopy(runtime)

        old = new_runtime.get_node(
            delta.node_name
        )

        new_state = dict(old.states)

        for key, value in delta.state_deltas.items():
            new_state[key] = new_state.get(key, 0.0) + value

        new_runtime.set_node(
            NodeState(
                name=old.name,
                total=old.total + delta.total_delta,
                states=new_state,
            )
        )

        return new_runtime

    def merge_passive(
        self,
        runtime: Runtime,
        delta: PassiveDelta,
    ) -> Runtime:

        new_runtime = deepcopy(runtime)

        old = new_runtime.get_node(
            delta.node_name
        )


        new_states = dict(old.states)

        for key,value in delta.state_deltas.items():
            new_states[key] = (
                new_states.get(key,0.0)
                + value
            )


        new_runtime.set_node(
            NodeState(
                name=old.name,
                total=old.total + delta.total_delta,
                states=new_states,
            )
        )


        return new_runtime

    def merge_gene(
        self,
        runtime: Runtime,
        delta: GeneDelta,
    ) -> Runtime:

        new_runtime = deepcopy(runtime)

        old = new_runtime.get_gene(
            delta.gene_name
        )

        modifications = {
            key: old.modifications.get(key, 0.0)
            + value
            for key, value in delta.modification_deltas.items()
        }

        new_runtime.set_gene(
            GeneState(
                name=old.name,
                baseline=old.baseline,
                value=old.value + delta.value_delta,
                modifications=modifications,
            )
        )

        return new_runtime
        
    def merge_behavior_internal(
        self,
        runtime: Runtime,
        delta: BehaviorInternalDelta,
    ) -> Runtime:
        """
        Merge internal changes produced by BehaviorEngine.

        BehaviorInternalDelta is only a container.
        Actual node/gene updates are delegated to
        existing merge functions.
        """

        new_runtime = deepcopy(runtime)

        for node_delta in delta.node_deltas.values():
            new_runtime = self.merge_node(
                new_runtime,
                node_delta,
            )

        for gene_delta in delta.gene_deltas.values():
            new_runtime = self.merge_gene(
                new_runtime,
                gene_delta,
            )

        return new_runtime
