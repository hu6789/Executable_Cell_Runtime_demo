# internalnet/node_engine/engine.py

from __future__ import annotations

from .formulation import FormulationEngine
from .repository import NodeRepository
from .schema import NodeInput, NodeRuntimeState
from internalnet.runtime.delta import NodeDelta
from .transition import TransitionEngine


class NodeEngine:
    """Coordinate node definition lookup, formulation evaluation,
    and polymorphic state transitions.

    The engine is a thin orchestration layer. It does not implement
    formulation equations or transition conditions itself.
    """

    def __init__(
        self,
        repository: NodeRepository,
        formulation_engine: FormulationEngine | None = None,
        transition_engine: TransitionEngine | None = None,
    ) -> None:
        self.repository = repository
        self.formulation_engine = (
            formulation_engine
            if formulation_engine is not None
            else FormulationEngine()
        )
        self.transition_engine = (
            transition_engine
            if transition_engine is not None
            else TransitionEngine()
        )

    def run(
        self,
        node_input: NodeInput,
    ) -> NodeDelta:
        """Execute one node evaluation cycle."""

        node = self.repository.get(
            node_input.node_name
        )

        computed_values = self.formulation_engine.evaluate(
            node=node,
            node_input=node_input,
        )

        runtime_state = NodeRuntimeState(
            node_name=node_input.node_name,
            total=node_input.total,
            states=dict(node_input.states),
        )

        runtime_state = self.transition_engine.apply_transition(
            node=node,
            runtime_state=runtime_state,
            computed_values=computed_values,
        )

        return NodeDelta(
            source="node_engine",
            node_name=node_input.node_name,
            total_delta=(
                runtime_state.total
                -
                node_input.total
            ),
            state_deltas={
                state_name:
                    runtime_state.states.get(
                        state_name,
                        0.0,
                    )
                    -
                    node_input.states.get(
                        state_name,
                        0.0,
                    )
                for state_name in set(
                    runtime_state.states
                ).union(
                    node_input.states
                )
            },
        )
