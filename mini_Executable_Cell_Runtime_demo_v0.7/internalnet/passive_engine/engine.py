from __future__ import annotations

from internalnet.node_engine.repository import NodeRepository
from internalnet.node_engine.schema import NodeRuntimeState

from .formulation import PassiveFormulationEngine
from .repository import PassiveRepository
from .schema import PassiveDefinition
from internalnet.runtime.delta import PassiveDelta


class PassiveEngine:
    """
    Passive calculation engine.

    Flow:

        PassiveDefinition
              +
        NodeDefinition
              +
        NodeRuntimeState

              ↓

        PassiveDelta


    PassiveEngine does NOT:
    - mutate runtime
    - apply state changes
    - manage Runtime
    """


    def __init__(
        self,
        passive_repository: PassiveRepository,
        node_repository: NodeRepository,
        formulation_engine: PassiveFormulationEngine | None = None,
    ):

        self._passive_repository = passive_repository
        self._node_repository = node_repository

        self._formulation_engine = (
            formulation_engine
            if formulation_engine is not None
            else PassiveFormulationEngine()
        )


    def evaluate(
        self,
        passive_name: str,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> PassiveDelta:

        passive = self._passive_repository.get(
            passive_name
        )

        node = self._node_repository.get(
            runtime_state.node_name
        )


        state_changes = (
            self._formulation_engine.evaluate(
                passive=passive,
                node=node,
                runtime_state=runtime_state,
                dt=dt,
            )
        )


        return PassiveDelta(
            source="passive_engine",
            passive_name=passive.name,
            node_name=runtime_state.node_name,
            state_deltas=state_changes,
        )
        
        
    def applicable_passives(
        self,
        node_name: str,
    ) -> tuple[PassiveDefinition, ...]:
        return tuple(
            passive
            for passive in self._passive_repository.all()
            if node_name in passive.applies_to
        )


    def run(
        self,
        passive_name: str,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> PassiveDelta:

        return self.evaluate(
            passive_name=passive_name,
            runtime_state=runtime_state,
            dt=dt,
        )
