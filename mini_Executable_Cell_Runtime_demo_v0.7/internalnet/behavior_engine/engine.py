# internalnet/behavior_engine/engine.py

from typing import Dict, Optional

from internalnet.behavior_engine.formulation import (
    BehaviorFormulationEngine,
)
from internalnet.behavior_engine.input_resolver import (
    BehaviorExecution,
    BehaviorInputResolver,
)
from internalnet.behavior_engine.repository import BehaviorRepository
from internalnet.behavior_engine.schema import BehaviorIntention
from internalnet.compute_plan.schema import CellComputePlan
from internalnet.runtime.state import GeneState, NodeState


class BehaviorEngine:
    """Thin façade for behavior input resolution and formulation."""

    def __init__(
        self,
        repository: BehaviorRepository,
        input_resolver: Optional[BehaviorInputResolver] = None,
        formulation: Optional[BehaviorFormulationEngine] = None,
    ):
        self._repository = repository

        self._input_resolver = (
            input_resolver
            if input_resolver is not None
            else BehaviorInputResolver()
        )

        self._formulation = (
            formulation
            if formulation is not None
            else BehaviorFormulationEngine()
        )

    def run(
        self,
        behavior_name: str,
        plan: CellComputePlan,
        node_states: Dict[str, NodeState],
        gene_states: Dict[str, GeneState],
        parameters: Dict[str, float],
    ) -> BehaviorIntention:
        behavior = self._repository.get(behavior_name)

        inputs = self._input_resolver.resolve(
            behavior_name=behavior_name,
            plan=plan,
            node_states=node_states,
            gene_states=gene_states,
        )

        return self._formulation.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters=parameters,
        )
        
        
    def run_execution(
        self,
        execution: BehaviorExecution,
        parameters: Dict[str, float],
    ) -> Optional[BehaviorIntention]:
        behavior = self._repository.get(
            execution.behavior_name
        )

        intention = self._formulation.evaluate(
            behavior=behavior,
            inputs=execution.inputs,
            parameters=parameters,
        )

        if intention is None:
            return None

        return BehaviorIntention(
            behavior_name=intention.behavior_name,
            value=intention.value,
            inputs=intention.inputs,
            internal_outputs=behavior.internal_outputs,
            outputs=behavior.outputs,
        )

