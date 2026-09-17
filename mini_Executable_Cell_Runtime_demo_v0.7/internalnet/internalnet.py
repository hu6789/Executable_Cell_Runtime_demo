from __future__ import annotations

from internalnet.compute_plan.schema import CellComputePlan
from internalnet.node_engine.engine import NodeEngine
from internalnet.node_engine.repository import NodeRepository
from internalnet.node_engine.schema import (
    NodeInput,
    NodeRuntimeState,
)
from internalnet.runtime.merger import RuntimeMerger
from internalnet.runtime.schema import Runtime
from internalnet.passive_engine.engine import PassiveEngine
from internalnet.gene_engine.engine import GeneEngine
from internalnet.gene_engine.repository import GeneRepository
from internalnet.hir.engine import HIREngine
from internalnet.hir.schema import HIROutput
from typing import Any, Optional

class InternalNet:
    """Orchestrate InternalNet runtime stages for one cell."""

    def __init__(
        self,
        node_engine: NodeEngine,
        passive_engine: PassiveEngine,
        node_repository: NodeRepository,
        runtime_merger: RuntimeMerger,
        gene_engine: GeneEngine | None = None,
        gene_repository: GeneRepository | None = None,
        hir_engine: HIREngine | None = None,
        trace: Optional[Any] = None,
    ) -> None:
        self._node_engine = node_engine
        self._passive_engine = passive_engine
        self._node_repository = node_repository
        self._runtime_merger = runtime_merger
        self._gene_engine = gene_engine
        self._gene_repository = gene_repository
        self._hir_engine = hir_engine
        self._trace = trace
    
    def run_node_stage(
        self,
        runtime: Runtime,
        plan: CellComputePlan,
    ) -> Runtime:
        current_runtime = runtime

        for node_name in plan.node_execution_order:
            node_state = current_runtime.get_node(node_name)

            related_inputs = {}

            for edge in plan.edges:
                if edge.type != "node-node":
                    continue
                if edge.target != node_name:
                    continue

                source_state = current_runtime.get_node(edge.source)

                related_inputs[edge.source] = {
                    "total": source_state.total,
                    "states": dict(source_state.states),
                }

            node_input = NodeInput(
                node_name=node_name,
                total=node_state.total,
                states=dict(node_state.states),
                related_inputs=related_inputs,
            )

            before_state = current_runtime.get_node(
                node_name
            )

            delta = self._node_engine.run(node_input)

            current_runtime = self._runtime_merger.merge_node(
                current_runtime,
                delta,
            )

            after_state = current_runtime.get_node(
                node_name
            )

            if self._trace is not None:
                self._trace.record_node(
                    cell_id=plan.cell_id,
                    before=before_state,
                    after=after_state,
                    delta=delta,
                )

        return current_runtime
        
    def run_passive_stage(
        self,
        runtime: Runtime,
        plan: CellComputePlan,
        dt: float,
    ) -> Runtime:
        current_runtime = runtime

        for node_name in plan.node_execution_order:
            node_definition = self._node_repository.get(node_name)

            if node_definition.half_life is not None:
                passive_name = "half_life_decay"
                
                before_state = current_runtime.get_node(
                    node_name
                )

                runtime_state = NodeRuntimeState(
                    node_name=before_state.name,
                    total=before_state.total,
                    states=dict(before_state.states),
                )

                delta = self._passive_engine.run(
                    passive_name=passive_name,
                    runtime_state=runtime_state,
                    dt=dt,
                )

                current_runtime = self._runtime_merger.merge_passive(
                    current_runtime,
                    delta,
                )

                after_state = current_runtime.get_node(
                    node_name
                )

                if self._trace is not None:
                    self._trace.record_passive(
                        cell_id=plan.cell_id,
                        before=before_state,
                        after=after_state,
                        delta=delta,
                    )

            for passive in self._passive_engine.applicable_passives(
                node_name
            ):
                if passive.name == "diffusion":
                    continue

                before_state = current_runtime.get_node(
                    node_name
                )


                runtime_state = NodeRuntimeState(
                    node_name=before_state.name,
                    total=before_state.total,
                    states=dict(before_state.states),
                )
  
                delta = self._passive_engine.run(
                    passive_name=passive.name,
                    runtime_state=runtime_state,
                    dt=dt,
                )

                current_runtime = self._runtime_merger.merge_passive(
                    current_runtime,
                    delta,
                )
                
                after_state = current_runtime.get_node(
                    node_name
                )

                if self._trace is not None:
                    self._trace.record_passive(
                    cell_id=plan.cell_id,
                    before=before_state,
                    after=after_state,
                    delta=delta,
                )

            if node_definition.diffusion is not None:
                passive_name = "diffusion"

                before_state = current_runtime.get_node(
                    node_name
                )


                runtime_state = NodeRuntimeState(
                    node_name=before_state.name,
                    total=before_state.total,
                    states=dict(before_state.states),
                )

                delta = self._passive_engine.run(
                    passive_name=passive_name,
                    runtime_state=runtime_state,
                    dt=dt,
                )

                current_runtime = self._runtime_merger.merge_passive(
                    current_runtime,
                    delta,
                )
                
                after_state = current_runtime.get_node(
                    node_name
                )

                if self._trace is not None:
                    self._trace.record_passive(
                        cell_id=plan.cell_id,
                        before=before_state,
                        after=after_state,
                        delta=delta,
                    )

        return current_runtime
        
        
    def run_gene_stage(
        self,
        runtime: Runtime,
        plan: CellComputePlan,
    ) -> Runtime:
        if self._gene_engine is None:
            raise RuntimeError(
                "GeneEngine is required for gene stage"
            )

        if self._gene_repository is None:
            raise RuntimeError(
                "GeneRepository is required for gene stage"
            )

        current_runtime = runtime

        for gene_name in plan.candidate_genes:
            gene_state = current_runtime.get_gene(gene_name)

            node_states = {}

            for edge in plan.edges:
                if edge.type != "node-gene":
                    continue

                if edge.target != gene_name:
                    continue
 
                node_state = current_runtime.get_node(edge.source)

                node_states[edge.source] = NodeRuntimeState(
                    node_name=node_state.name,
                    total=node_state.total,
                    states=dict(node_state.states),
                )

            before_state = gene_state

            delta = self._gene_engine.run(
                gene_name=gene_name,
                gene_state=gene_state,
                node_states=node_states,
            )

            current_runtime = self._runtime_merger.merge_gene(
                current_runtime,
                delta,
            )

            after_state = current_runtime.get_gene(
                gene_name
            )

            if self._trace is not None:
                self._trace.record_gene(
                    cell_id=plan.cell_id,
                    before=before_state,
                    after=after_state,
                    delta=delta,
                )

        return current_runtime
        
    def run_hir_stage(
        self,
        runtime: Runtime,
        plan: CellComputePlan,
        gene_definitions: dict,
        node_definitions: dict,
        behavior_parameters: dict,
        resource_coefficients: dict,
        available_resources: dict,
    ) -> HIROutput:

        if self._hir_engine is None:
            raise RuntimeError(
                "HIREngine is required for HIR stage"
            )

        if self._gene_repository is not None:
            gene_definitions = {
                gene_name: self._gene_repository.get(gene_name)
                for gene_name in plan.candidate_genes
            }
            
        if self._node_repository is not None:
            node_definitions = {
                node_name: self._node_repository.get(node_name)
                for node_name in plan.candidate_nodes
            }

        return self._hir_engine.run(
            plan=plan,
            node_states=dict(runtime.node_states),
            gene_states=dict(runtime.gene_states),
            gene_definitions=gene_definitions,
            node_definitions=node_definitions,
            behavior_parameters=behavior_parameters,
            resource_coefficients=resource_coefficients,
            available_resources=available_resources,
        )
        
    def run(
        self,
        runtime: Runtime,
        plan: CellComputePlan,
        dt: float,
        gene_definitions: dict,
        node_definitions: dict,
        behavior_parameters: dict,
        resource_coefficients: dict,
        available_resources: dict,
    ) -> HIROutput:
        current_runtime = self.run_node_stage(
            runtime,
            plan,
        )

        current_runtime = self.run_passive_stage(
            current_runtime,
            plan,
            dt,
        )

        current_runtime = self.run_gene_stage(
            current_runtime,
            plan,
        )

        return self.run_hir_stage(
            current_runtime,
            plan,
            gene_definitions,
            node_definitions,
            behavior_parameters,
            resource_coefficients,
            available_resources,
        )
