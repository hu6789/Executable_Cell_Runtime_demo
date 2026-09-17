from typing import Dict, List
from typing import Any, Optional
from internalnet.behavior_engine.engine import BehaviorEngine
from internalnet.behavior_engine.schema import BehaviorIntention
from internalnet.compute_plan.schema import CellComputePlan
from internalnet.gene_engine.schema import GeneDefinition
from internalnet.runtime.state import GeneState, NodeState
from internalnet.behavior_engine.input_resolver import (
    BehaviorInputResolver,
)
from .behavior_state_merger import BehaviorStateMerger
from .label.determination import LabelDetermination
from .realization.resource_allocator import ResourceAllocator
from .realization.resource_realizer import ResourceRealizer
from .regulation.tf_regulator import TFRegulator
from .schema import (
    BehaviorExternalEffect,
    BehaviorRuntimeState,
    HIROutput,
)
from .type.determination import TypeDetermination
from .type.repository import TypeCriteriaRepository


class HIREngine:
    """
    Orchestrate HIR behavior regulation and current-cell classification.

    Responsibilities:
    - run candidate behaviors
    - resolve genes connected to each behavior
    - apply TF regulation
    - allocate and realize resources
    - merge the final behavior runtime state
    - determine current labels
    - determine current cell type

    HIREngine does NOT:
    - access World
    - write World
    - apply Intent
    - perform biological formulas itself
    - resolve graphs directly
    """

    def __init__(
        self,
        behavior_engine: BehaviorEngine,
        tf_regulator: TFRegulator,
        resource_allocator: ResourceAllocator,
        resource_realizer: ResourceRealizer,
        behavior_state_merger: BehaviorStateMerger,
        label_determination: LabelDetermination,
        type_determination: TypeDetermination,
        type_criteria_repository: TypeCriteriaRepository,
            trace: Optional[Any] = None,
    ) -> None:
        self._behavior_engine = behavior_engine
        self._behavior_input_resolver = BehaviorInputResolver()
        self._tf_regulator = tf_regulator
        self._resource_allocator = resource_allocator
        self._resource_realizer = resource_realizer
        self._behavior_state_merger = behavior_state_merger
        self._label_determination = label_determination
        self._type_determination = type_determination
        self._type_criteria_repository = type_criteria_repository
        self._trace = trace

    def run(
        self,
        plan: CellComputePlan,
        node_states: Dict[str, NodeState],
        gene_states: Dict[str, GeneState],
        gene_definitions: Dict[str, GeneDefinition],
        node_definitions: Dict[str, Dict],
        behavior_parameters: Dict[str, Dict[str, float]],
        resource_coefficients: Dict[str, Dict[str, float]],
        available_resources: Dict[str, float],
    ) -> HIROutput:
        """
        Execute the HIR pipeline for one cell and one compute plan.
        """

        behaviors: Dict[str, BehaviorRuntimeState] = {}
        external_effects: Dict[str, BehaviorExternalEffect] = {}

        for behavior_name in plan.candidate_behaviors:

            executions = self._behavior_input_resolver.resolve_executions(
                behavior_name=behavior_name,
                plan=plan,
                node_states=node_states,
                gene_states=gene_states,
            )

            for execution in executions:

                # ---------------------------------------------------------
                # 1. Behavior intention for this execution
                # ---------------------------------------------------------
                intention = self._behavior_engine.run_execution(
                    execution=execution,
                    parameters=behavior_parameters.get(
                        behavior_name,
                        {},
                    ),
                )

                if intention is None:
                    continue
                    
                internal_outputs = intention.internal_outputs
                
                
                resolved_internal_output = (
                    self._resolve_internal_output_target(
                        internal_outputs=internal_outputs,
                        source_name=execution.source_name,
                    )
                )

                # ---------------------------------------------------------
                # 2. TF regulation for this execution only
                # ---------------------------------------------------------
                if execution.source_type == "gene":
                    behavior_genes = [execution.source_name]
                else:
                    behavior_genes = []


                tf_delta = self._tf_regulator.regulate(
                    intention=intention,
                    behavior_genes=behavior_genes,
                    node_states=node_states,
                    gene_definitions=gene_definitions,
                )

                # TF-adjusted behavior value.
                tf_adjusted_intention = BehaviorIntention(
                    behavior_name=intention.behavior_name,
                    value=intention.value + tf_delta.delta,
                    inputs=intention.inputs,
                    internal_outputs=intention.internal_outputs,
                    outputs=intention.outputs,
                )

                # ---------------------------------------------------------
                # 3. Resource allocation
                # ---------------------------------------------------------
                allocation = self._resource_allocator.allocate(
                    behavior_name=behavior_name,
                    behavior_value=tf_adjusted_intention.value,
                    resource_coefficients=resource_coefficients.get(
                        behavior_name,
                        {},
                    ),
                )

                # ---------------------------------------------------------
                # 4. Resource realization
                # ---------------------------------------------------------
                resource_delta = self._resource_realizer.realize(
                    intention=tf_adjusted_intention,
                    allocation=allocation,
                    available_resources=available_resources,
                )

                # ---------------------------------------------------------
                # 5. Merge final runtime state for this execution
                # ---------------------------------------------------------
                runtime_state = self._behavior_state_merger.merge(
                    intention=tf_adjusted_intention,
                    tf_delta=tf_delta,
                    resource_delta=resource_delta,
                    node_states=node_states,
                    gene_states=gene_states,
                    source_type=execution.source_type,
                    source_name=execution.source_name,
                    internal_outputs=resolved_internal_output,
                )

                execution_key = "{}:{}".format(
                    execution.behavior_name,
                    execution.source_name,
                )

                behaviors[execution_key] = runtime_state
                
                if self._trace is not None:
                    self._trace.record_behavior(
                        cell_id=plan.cell_id,
                        behavior_name=execution.behavior_name,
                        source_type=execution.source_type,
                        source_name=execution.source_name,
                        intention_value=intention.value,
                        intention_inputs=dict(intention.inputs),
                        tf_delta=tf_delta.delta,
                        resource_allocation=dict(
                            allocation.resources
                        ),
                        resource_delta=resource_delta.delta,
                        final_value=runtime_state.value,
                    )
                
                external_output = intention.outputs.get("extracellular")

                if (
                    external_output
                    and execution.source_type == "node"
                ):
                    target = external_output.get("target")

                    if target == "source_name":
                        target = execution.source_name

                    if target is not None:
                        effect_key = "{}:{}".format(
                            execution.behavior_name,
                            target,
                        )

                        external_effects[effect_key] = BehaviorExternalEffect(
                            behavior_name=execution.behavior_name,
                            effect_type="extracellular",
                            target=target,
                            value=runtime_state.value,
                        )

        # -------------------------------------------------------------
        # 7. Label determination
        #
        # Label is a capability/interface output and is independent
        # from BehaviorRuntimeState.
        # -------------------------------------------------------------
        labels = self._label_determination.determine(
            node_states=node_states,
            node_definitions=node_definitions,
        )

        # -------------------------------------------------------------
        # 8. Type determination
        #
        # Type is determined from current node/gene evidence and
        # TypeCriteria. It is independent from behavior runtime state.
        # -------------------------------------------------------------
        criteria = self._type_criteria_repository.all()

        type_name = self._type_determination.determine(
            criteria=criteria,
            node_states=node_states,
            gene_states=gene_states,
        )

        if self._trace is not None:
            self._trace.record_hir_summary(
                cell_id=plan.cell_id,
                labels=labels,
                type_name=type_name,
            )

        return HIROutput(
            behaviors=behaviors,
            external_effects=external_effects,
            labels=labels,
            type_name=type_name,
        )

    @staticmethod
    def _genes_for_behavior(
        plan: CellComputePlan,
        behavior_name: str,
    ) -> List[str]:
        """
        Return genes connected to a behavior through gene-behavior edges.
        """

        return [
            edge.source
            for edge in plan.edges
            if edge.type == "gene-behavior"
            and edge.target == behavior_name
        ]
        
        
    @staticmethod
    def _resolve_internal_output_target(
        internal_outputs: Dict,
        source_name: str,
    ):
        node_output = internal_outputs.get("node")

        if not node_output:
            return None

        target = node_output.get("target")

        if target == "source_name":
            target = source_name

        return {
            "target": target,
            "state": node_output.get("state"),
        }
