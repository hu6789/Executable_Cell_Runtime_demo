# demo/trace.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class NodeTrace:
    cell_id: str
    node_name: str
    before_total: float
    after_total: float
    before_states: Dict[str, float]
    after_states: Dict[str, float]
    delta: Any


@dataclass
class PassiveTrace:
    cell_id: str
    node_name: str
    passive_name: str
    before_states: Dict[str, float]
    after_states: Dict[str, float]
    delta: Any


@dataclass
class GeneTrace:
    cell_id: str
    gene_name: str
    before_value: float
    after_value: float
    delta: Any


@dataclass
class BehaviorTrace:
    cell_id: str
    behavior_name: str
    source_type: str
    source_name: str
    intention_value: float
    intention_inputs: Dict[str, float]
    tf_delta: float
    resource_allocation: Dict[str, float]
    resource_delta: float
    final_value: float


@dataclass
class HIRTrace:
    cell_id: str
    behaviors: List[BehaviorTrace] = field(
        default_factory=list
    )
    labels: List[str] = field(
        default_factory=list
    )
    type_name: Optional[str] = None


@dataclass
class CellTrace:
    cell_id: str
    nodes: List[NodeTrace] = field(
        default_factory=list
    )
    passives: List[PassiveTrace] = field(
        default_factory=list
    )
    genes: List[GeneTrace] = field(
        default_factory=list
    )
    hir: Optional[HIRTrace] = None


class DemoTraceRecorder:
    """
    Demo-only observation recorder.

    This object does not calculate biology and does not
    participate in runtime decisions.

    It records intermediate results produced by the real
    InternalNet/HIR execution so the demo can display them.
    """

    def __init__(self) -> None:
        self.cells: Dict[str, CellTrace] = {}

    def cell(self, cell_id: str) -> CellTrace:
        if cell_id not in self.cells:
            self.cells[cell_id] = CellTrace(
                cell_id=cell_id
            )

        return self.cells[cell_id]

    def record_node(
        self,
        cell_id: str,
        before,
        after,
        delta,
    ) -> None:
        self.cell(cell_id).nodes.append(
            NodeTrace(
                cell_id=cell_id,
                node_name=after.name,
                before_total=before.total,
                after_total=after.total,
                before_states=dict(before.states),
                after_states=dict(after.states),
                delta=delta,
            )
        )

    def record_passive(
        self,
        cell_id: str,
        before,
        after,
        delta,
    ) -> None:
        self.cell(cell_id).passives.append(
            PassiveTrace(
                cell_id=cell_id,
                node_name=after.name,
                passive_name=delta.passive_name,
                before_states=dict(before.states),
                after_states=dict(after.states),
                delta=delta,
            )
        )

    def record_gene(
        self,
        cell_id: str,
        before,
        after,
        delta,
    ) -> None:
        self.cell(cell_id).genes.append(
            GeneTrace(
                cell_id=cell_id,
                gene_name=delta.gene_name,
                before_value=before.value,
                after_value=after.value,
                delta=delta,
            )
        )

    def record_behavior(
        self,
        cell_id: str,
        behavior_name: str,
        source_type: str,
        source_name: str,
        intention_value: float,
        intention_inputs: Dict[str, float],
        tf_delta: float,
        resource_allocation: Dict[str, float],
        resource_delta: float,
        final_value: float,
    ) -> None:
        hir = self.cell(cell_id).hir

        if hir is None:
            hir = HIRTrace(cell_id=cell_id)
            self.cell(cell_id).hir = hir

        hir.behaviors.append(
            BehaviorTrace(
                cell_id=cell_id,
                behavior_name=behavior_name,
                source_type=source_type,
                source_name=source_name,
                intention_value=intention_value,
                intention_inputs=dict(intention_inputs),
                tf_delta=tf_delta,
                resource_allocation=dict(
                    resource_allocation
                ),
                resource_delta=resource_delta,
                final_value=final_value,
            )
        )
        
        
    def record_hir_summary(
        self,
        cell_id: str,
        labels,
        type_name,
    ) -> None:
        hir = self.cell(cell_id).hir

        if hir is None:
            hir = HIRTrace(cell_id=cell_id)
            self.cell(cell_id).hir = hir

        hir.labels = list(labels)
        hir.type_name = type_name        
        
    def record_hir(
        self,
        cell_id: str,
        hir_trace: HIRTrace,
    ) -> None:
        self.cell(cell_id).hir = hir_trace

    def clear(self) -> None:
        self.cells.clear()
