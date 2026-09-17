import pytest

from internalnet.hir.schema import (
    TFRegulationDelta,
    ResourceAllocation,
    ResourceDelta,
    BehaviorRuntimeState,
    BehaviorExternalEffect,
    HIROutput,
)
from internalnet.behavior_engine.schema import BehaviorIntention

def test_behavior_intention():
    intention = BehaviorIntention(
        behavior_name="production",
        value=0.8,
        inputs={"FOXA2": 0.8},
    )

    assert intention.behavior_name == "production"
    assert intention.value == 0.8
    assert intention.inputs["FOXA2"] == 0.8


def test_tf_regulation_delta():
    delta = TFRegulationDelta(
        behavior_name="production",
        delta=0.2,
    )

    assert delta.behavior_name == "production"
    assert delta.delta == 0.2


def test_resource_allocation():
    allocation = ResourceAllocation(
        behavior_name="production",
        resources={
            "ATP": 1.5,
            "enzyme": 0.1,
        },
    )

    assert allocation.behavior_name == "production"
    assert allocation.resources["ATP"] == 1.5
    assert allocation.resources["enzyme"] == 0.1


def test_resource_delta():
    delta = ResourceDelta(
        behavior_name="production",
        delta=-0.4,
    )

    assert delta.behavior_name == "production"
    assert delta.delta == -0.4


def test_behavior_runtime_state():
    state = BehaviorRuntimeState(
        behavior_name="production",
        source_type="gene",
        source_name="FOXA2",
        node_states={},
        gene_states={},
        value=0.6,
    )

    assert state.behavior_name == "production"
    assert state.source_type == "gene"
    assert state.source_name == "FOXA2"
    assert state.node_states == {}
    assert state.gene_states == {}
    assert state.value == 0.6

def test_behavior_external_effect():
    effect = BehaviorExternalEffect(
        behavior_name="release",
        effect_type="extracellular",
        target="SHH",
        value=0.4,
    )

    assert effect.behavior_name == "release"
    assert effect.effect_type == "extracellular"
    assert effect.target == "SHH"
    assert effect.value == 0.4


def test_hir_output():
    behavior_state = BehaviorRuntimeState(
        behavior_name="production",
        source_type="gene",
        source_name="FOXA2",
        node_states={},
        gene_states={},
        value=0.6,
    )
    
    effect = BehaviorExternalEffect(
        behavior_name="release",
        effect_type="extracellular",
        target="SHH",
        value=0.4,
    )

    output = HIROutput(
        behaviors={"production:FOXA2": behavior_state},
        external_effects={"release:SHH": effect},
        labels={"SHH_releasing"},
        type_name="floor_plate_progenitor",
    )

    assert (
        output.behaviors["production:FOXA2"].behavior_name
        == "production"
    )

    assert (
        output.behaviors["production:FOXA2"].source_name
        == "FOXA2"
    )

    assert output.behaviors["production:FOXA2"].value == 0.6
    assert output.external_effects["release:SHH"].target == "SHH"
    assert "SHH_releasing" in output.labels
    assert output.type_name == "floor_plate_progenitor"


def test_hir_output_defaults():
    output = HIROutput()

    assert output.behaviors == {}
    assert output.external_effects == {}
    assert output.labels == set()
    assert output.type_name is None
    
    
from pathlib import Path

from internalnet.hir.regulation.repository import (
    TFElementRelationRepository,
)


HIR_LIBRARY = (
    Path(__file__).resolve().parents[1]
    / "internalnet"
    / "hir"
    / "library"
)


def test_tf_element_relation_repository_loads_relations():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    relations = repository.find_by_tf("FOXA2")

    assert len(relations) == 1

    relation = relations[0]

    assert relation.name == "FOXA2_SFPE2_regulation"
    assert relation.tf == "FOXA2"
    assert relation.element == "SFPE2"
    assert relation.category == "transcriptional_regulation"
    assert relation.effect == "activation"
    assert relation.value == 1.0


def test_tf_element_relation_repository_find_by_element():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    relations = repository.find_by_element(
        "FOXA2_Gli_Response_Enhancer"
    )

    assert len(relations) == 1

    relation = relations[0]

    assert relation.tf == "GLI2"
    assert relation.element == "FOXA2_Gli_Response_Enhancer"
    assert relation.effect == "activation"
    assert relation.value == 1.0


def test_tf_element_relation_repository_returns_empty_for_unknown_tf():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    assert repository.find_by_tf("UNKNOWN_TF") == []


def test_tf_element_relation_repository_returns_empty_for_unknown_element():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    assert repository.find_by_element("UNKNOWN_ELEMENT") == []
    
from internalnet.gene_engine.schema import GeneDefinition
from internalnet.node_engine.schema import NodeRuntimeState

from internalnet.hir.regulation.tf_regulator import (
    TFRegulator,
)


def test_tf_regulator_scopes_regulation_to_behavior_genes():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    regulator = TFRegulator(repository)

    intention = BehaviorIntention(
        behavior_name="release",
        value=0.5,
    )

    gene_definitions = {
        "SHH": GeneDefinition(
            name="SHH",
            elements=[
                {
                    "name": "SFPE2",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 0.0,
                }
            ],
        ),
        "FOXA2": GeneDefinition(
            name="FOXA2",
            elements=[
                {
                    "name": "FOXA2_Gli_Response_Enhancer",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 0.0,
                }
            ],
        ),
    }

    node_states = {
        "FOXA2": NodeRuntimeState(
            node_name="FOXA2",
            total=0.8,
            states={"nuclear": 0.8},
        ),
        "GLI2": NodeRuntimeState(
            node_name="GLI2",
            total=0.6,
            states={"nuclear": 0.6},
        ),
    }

    delta = regulator.regulate(
        intention=intention,
        behavior_genes=["SHH"],
        node_states=node_states,
        gene_definitions=gene_definitions,
    )

    assert delta.behavior_name == "release"
    assert delta.delta == 0.8
    
def test_tf_regulator_uses_all_genes_of_behavior():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    regulator = TFRegulator(repository)

    intention = BehaviorIntention(
        behavior_name="production",
        value=0.5,
    )

    gene_definitions = {
        "SHH": GeneDefinition(
            name="SHH",
            elements=[
                {
                    "name": "SFPE2",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 0.0,
                }
            ],
        ),
        "FOXA2": GeneDefinition(
            name="FOXA2",
            elements=[
                {
                    "name": "FOXA2_Gli_Response_Enhancer",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 0.0,
                }
            ],
        ),
    }

    node_states = {
        "FOXA2": NodeRuntimeState(
            node_name="FOXA2",
            total=0.8,
            states={"nuclear": 0.8},
        ),
        "GLI2": NodeRuntimeState(
            node_name="GLI2",
            total=0.6,
            states={"nuclear": 0.6},
        ),
    }

    delta = regulator.regulate(
        intention=intention,
        behavior_genes=["FOXA2", "SHH"],
        node_states=node_states,
        gene_definitions=gene_definitions,
    )

    assert delta.behavior_name == "production"
    assert delta.delta == 1.4
    
def test_tf_regulator_applies_distance_factor():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    regulator = TFRegulator(repository)

    intention = BehaviorIntention(
        behavior_name="release",
        value=0.5,
    )

    gene_definitions = {
        "SHH": GeneDefinition(
            name="SHH",
            elements=[
                {
                    "name": "SFPE2",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 1.0,
                }
            ],
        ),
    }

    node_states = {
        "FOXA2": NodeRuntimeState(
            node_name="FOXA2",
            total=0.8,
            states={"nuclear": 0.8},
        ),

    }

    delta = regulator.regulate(
        intention=intention,
        behavior_genes=["SHH"],
        node_states=node_states,
        gene_definitions=gene_definitions,
    )

    assert delta.delta == 0.4
    
def test_tf_regulator_ignores_missing_tf_state():
    repository = TFElementRelationRepository(
        HIR_LIBRARY / "tf_element_relations.json"
    )

    regulator = TFRegulator(repository)

    intention = BehaviorIntention(
        behavior_name="release",
        value=0.5,
    )

    gene_definitions = {
        "SHH": GeneDefinition(
            name="SHH",
            elements=[
                {
                    "name": "SFPE2",
                    "category": "enhancer",
                    "effect": "activation",
                    "value": 1.0,
                    "distance": 0.0,
                }
            ],
        ),
    }

    delta = regulator.regulate(
        intention=intention,
        behavior_genes=["SHH"],
        node_states={},
        gene_definitions=gene_definitions,
    )

    assert delta.behavior_name == "release"
    assert delta.delta == 0.0
    
from internalnet.hir.realization.resource_allocator import (
    ResourceAllocator,
)

from internalnet.hir.realization.resource_allocator import (
    ResourceAllocator,
)


def test_resource_allocator_scales_consumable_resources():
    allocator = ResourceAllocator()

    allocation = allocator.allocate(
        behavior_name="production",
        behavior_value=0.5,
        resource_coefficients={
            "ATP": 2.0,
            "molecule": 1.0,
        },
    )

    assert allocation.behavior_name == "production"
    assert allocation.resources["ATP"] == 1.0
    assert allocation.resources["molecule"] == 0.5


def test_resource_allocator_includes_occupancy_resources():
    allocator = ResourceAllocator()

    allocation = allocator.allocate(
        behavior_name="production",
        behavior_value=0.5,
        resource_coefficients={
            "ATP": 2.0,
            "enzyme": 0.1,
        },
    )

    assert allocation.resources["ATP"] == 1.0
    assert allocation.resources["enzyme"] == 0.05


def test_resource_allocator_uses_tf_adjusted_behavior_value():
    allocator = ResourceAllocator()

    allocation = allocator.allocate(
        behavior_name="production",
        behavior_value=1.5,
        resource_coefficients={
            "ATP": 2.0,
            "molecule": 1.0,
        },
    )

    assert allocation.resources["ATP"] == 3.0
    assert allocation.resources["molecule"] == 1.5


def test_resource_allocator_returns_zero_for_zero_behavior_value():
    allocator = ResourceAllocator()

    allocation = allocator.allocate(
        behavior_name="release",
        behavior_value=0.0,
        resource_coefficients={
            "ATP": 0.2,
            "enzyme": 0.05,
        },
    )

    assert allocation.resources["ATP"] == 0.0
    assert allocation.resources["enzyme"] == 0.0
    
from internalnet.hir.engine import HIREngine


def test_hir_engine_orchestrates_behavior_tf_resource_and_merge():
    """
    Verify the HIR pipeline:

        Behavior intention
            -> TF regulation
            -> TF-adjusted resource allocation
            -> resource realization
            -> final behavior state
    """

    class FakeBehaviorEngine:

        def run_execution(
            self,
            execution,
            parameters,
        ):
            return BehaviorIntention(
                behavior_name=execution.behavior_name,
                value=1.0,
                internal_outputs={
                    "node": {
                        "target": "source_name",
                        "state": "total",
                    }
                },
            )
 
    class FakeTFRegulator:

        def __init__(self):
            self.calls = []

        def regulate(
            self,
            intention,
            behavior_genes,
            node_states,
            gene_definitions,
        ):
            assert intention.value == 1.0

            self.calls.append(list(behavior_genes))

            return TFRegulationDelta(
                behavior_name=intention.behavior_name,
                delta=0.5,
            )

    class FakeResourceAllocator:

        def allocate(
            self,
            behavior_name,
            behavior_value,
            resource_coefficients,
        ):
            assert behavior_name == "production"
            assert behavior_value == 1.5
            assert resource_coefficients == {
                "ATP": 2.0,
            }

            return ResourceAllocation(
                behavior_name=behavior_name,
                resources={
                    "ATP": 3.0,
                },
            )

    class FakeResourceRealizer:

        def realize(
            self,
            intention,
            allocation,
            available_resources,
        ):
            assert intention.value == 1.5
            assert allocation.resources["ATP"] == 3.0
            assert available_resources["ATP"] == 1.5

            return ResourceDelta(
                behavior_name=intention.behavior_name,
                delta=-0.75,
            )

    class FakeBehaviorStateMerger:

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
            
            
    class FakeLabelDetermination:

        def determine(
            self,
            node_states,
            node_definitions,
        ):
            return {"PTCH1"}

    class FakeTypeDetermination:

        def determine(
            self,
            criteria,
            node_states,
            gene_states,
        ):
            return "floor_plate_progenitor"

    class FakeTypeCriteriaRepository:

        def all(self):
            return []

    plan = CellComputePlan(
        cell_id="cell_1",
        candidate_behaviors=("production",),
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
            GraphEdge(
                name="SHH_production",
                type="gene-behavior",
                source="SHH",
                target="production",
            ),
        ),
    )

    tf_regulator = FakeTFRegulator()

    engine = HIREngine(
        behavior_engine=FakeBehaviorEngine(),
        tf_regulator=tf_regulator,
        resource_allocator=FakeResourceAllocator(),
        resource_realizer=FakeResourceRealizer(),
        behavior_state_merger=FakeBehaviorStateMerger(),
        label_determination=FakeLabelDetermination(),
        type_determination=FakeTypeDetermination(),
        type_criteria_repository=FakeTypeCriteriaRepository(),
    )
    
    
    output = engine.run(
        plan=plan,
        node_states={},
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=1.0,
                value=1.0,
            ),
            "SHH": GeneState(
                name="SHH",
                baseline=1.0,
                value=1.0,
            ),
        },
        gene_definitions={},
        node_definitions={},
        behavior_parameters={
            "production": {},
        },
        resource_coefficients={
            "production": {
                "ATP": 2.0,
            },
        },
        available_resources={
            "ATP": 1.5,
        },
    )

    state_foxA2 = output.behaviors["production:FOXA2"]
    state_shh = output.behaviors["production:SHH"]

    assert state_foxA2.value == 0.75
    assert state_shh.value == 0.75

    assert state_foxA2.source_type == "gene"
    assert state_foxA2.source_name == "FOXA2"

    assert state_shh.source_type == "gene"
    assert state_shh.source_name == "SHH"

    assert tf_regulator.calls == [
        ["FOXA2"],
        ["SHH"],
    ]

    assert output.labels == {"PTCH1"}
    assert output.type_name == "floor_plate_progenitor"
    
    assert output.behaviors["production:FOXA2"].internal_outputs == {
         "target": "FOXA2",
         "state": "total",
    }

    assert output.behaviors["production:SHH"].internal_outputs == {
        "target": "SHH",
        "state": "total",
    }
    
    
from internalnet.hir.realization.resource_realizer import (
    ResourceRealizer,
)

def test_resource_realizer_returns_zero_when_resources_are_sufficient():
    realizer = ResourceRealizer()

    intention = BehaviorIntention(
        behavior_name="production",
        value=0.5,
    )

    allocation = ResourceAllocation(
        behavior_name="production",
        resources={
            "ATP": 1.0,
            "molecule": 0.5,
        },
    )

    delta = realizer.realize(
        intention=intention,
        allocation=allocation,
        available_resources={
            "ATP": 2.0,
            "molecule": 1.0,
        },
    )

    assert delta.behavior_name == "production"
    assert delta.delta == 0.0
    
def test_resource_realizer_limits_behavior_by_scarce_resource():
    realizer = ResourceRealizer()

    intention = BehaviorIntention(
        behavior_name="production",
        value=0.5,
    )

    allocation = ResourceAllocation(
        behavior_name="production",
        resources={
            "ATP": 1.0,
            "molecule": 0.5,
        },
    )

    delta = realizer.realize(
        intention=intention,
        allocation=allocation,
        available_resources={
            "ATP": 0.5,
            "molecule": 0.5,
        },
    )

    assert delta.behavior_name == "production"
    assert delta.delta == -0.25
    
def test_resource_realizer_uses_most_limiting_resource():
    realizer = ResourceRealizer()

    intention = BehaviorIntention(
        behavior_name="production",
        value=1.0,
    )

    allocation = ResourceAllocation(
        behavior_name="production",
        resources={
            "ATP": 2.0,
            "molecule": 1.0,
            "enzyme": 0.1,
        },
    )

    delta = realizer.realize(
        intention=intention,
        allocation=allocation,
        available_resources={
            "ATP": 1.5,
            "molecule": 0.9,
            "enzyme": 0.02,
        },
    )

    assert delta.delta == -0.8
    
def test_resource_realizer_treats_missing_resource_as_unavailable():
    realizer = ResourceRealizer()

    intention = BehaviorIntention(
        behavior_name="release",
        value=0.5,
    )

    allocation = ResourceAllocation(
        behavior_name="release",
        resources={
            "ATP": 0.2,
        },
    )

    delta = realizer.realize(
        intention=intention,
        allocation=allocation,
        available_resources={},
    )

    assert delta.behavior_name == "release"
    assert delta.delta == -0.5
    
    
from internalnet.hir.behavior_state_merger import (
    BehaviorStateMerger,
)

def test_behavior_state_merger_combines_all_deltas():
    merger = BehaviorStateMerger()

    intention = BehaviorIntention(
        behavior_name="production",
        value=0.7,
    )

    tf_delta = TFRegulationDelta(
        behavior_name="production",
        delta=0.2,
    )

    resource_delta = ResourceDelta(
        behavior_name="production",
        delta=-0.1,
    )

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }
    
    state = merger.merge(
        intention=intention,
        tf_delta=tf_delta,
        resource_delta=resource_delta,
        node_states=node_states,
        gene_states=gene_states,
        source_type="gene",
        source_name="FOXA2",
    )

    

    assert state.node_states == node_states
    assert state.gene_states == gene_states
    assert state.behavior_name == "production"
    assert state.source_type == "gene"
    assert state.source_name == "FOXA2"
    assert state.value == pytest.approx(0.6)
    
def test_behavior_state_merger_preserves_intention_without_deltas():
    merger = BehaviorStateMerger()

    intention = BehaviorIntention(
        behavior_name="release",
        value=0.7,
    )

    tf_delta = TFRegulationDelta(
        behavior_name="release",
        delta=0.0,
    )

    resource_delta = ResourceDelta(
        behavior_name="release",
        delta=0.0,
    )

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }
    
    state = merger.merge(
        intention=intention,
        tf_delta=tf_delta,
        resource_delta=resource_delta,
        node_states=node_states,
        gene_states=gene_states,
        source_type="gene",
        source_name="FOXA2",
    )

    

    assert state.node_states == node_states
    assert state.gene_states == gene_states
    assert state.behavior_name == "release"
    assert state.source_type == "gene"
    assert state.source_name == "FOXA2"
    assert state.value == pytest.approx(0.7)
    
def test_behavior_state_merger_allows_combined_negative_adjustment():
    merger = BehaviorStateMerger()

    intention = BehaviorIntention(
        behavior_name="production",
        value=0.3,
    )

    tf_delta = TFRegulationDelta(
        behavior_name="production",
        delta=-0.2,
    )

    resource_delta = ResourceDelta(
        behavior_name="production",
        delta=-0.1,
    )
    
    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }
    
    state = merger.merge(
        intention=intention,
        tf_delta=tf_delta,
        resource_delta=resource_delta,
        node_states=node_states,
        gene_states=gene_states,
        source_type="gene",
        source_name="FOXA2",
    )

    
    assert state.node_states == node_states
    assert state.gene_states == gene_states
    assert state.behavior_name == "production"
    assert state.source_type == "gene"
    assert state.source_name == "FOXA2"
    assert state.value == pytest.approx(0.2)

from internalnet.hir.label.determination import LabelDetermination

def test_label_determination_exposes_present_receptor():
    determination = LabelDetermination()

    node_definitions = {
        "PTCH1": {
            "category": "receptor",
        },
        "SMO": {
            "category": "functional_protein",
        },
    }

    node_states = {
        "PTCH1": NodeRuntimeState(
            node_name="PTCH1",
            total=1.0,
            states={
                "active": 0.0,
                "inactive": 1.0,
            },
        ),
        "SMO": NodeRuntimeState(
            node_name="SMO",
            total=1.0,
        ),
    }

    labels = determination.determine(
        node_states=node_states,
        node_definitions=node_definitions,
    )

    assert labels == {"PTCH1"}
    
def test_label_determination_hides_receptor_when_total_is_zero():
    determination = LabelDetermination()

    node_definitions = {
        "PTCH1": {
            "category": "receptor",
        },
    }

    node_states = {
        "PTCH1": NodeRuntimeState(
            node_name="PTCH1",
            total=0.0,
        ),
    }

    labels = determination.determine(
        node_states=node_states,
        node_definitions=node_definitions,
    )

    assert labels == set()
    
def test_label_determination_hides_receptor_without_runtime_state():
    determination = LabelDetermination()

    node_definitions = {
        "PTCH1": {
            "category": "receptor",
        },
    }

    labels = determination.determine(
        node_states={},
        node_definitions=node_definitions,
    )

    assert labels == set()
    
from internalnet.hir.type.determination import TypeDetermination
from internalnet.runtime.state import GeneState, NodeState
from internalnet.compute_plan.schema import CellComputePlan
from internalnet.graph_engine.schema import GraphEdge

def test_type_determination_returns_matching_type():
    determination = TypeDetermination()

    criteria = [
        TypeCriterion(
            type_name="floor_plate_progenitor",
            required=[
                {
                    "name": "FOXA2",
                    "source": "gene",
                    "threshold": 1.0,
                },
                {
                    "name": "SHH",
                    "source": "node",
                    "threshold": 1.0,
                },
            ],
        )
    ]

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }

    result = determination.determine(
        criteria=criteria,
        node_states=node_states,
        gene_states=gene_states,
    )

    assert result == "floor_plate_progenitor"


def test_type_determination_returns_none_when_required_evidence_is_missing():
    determination = TypeDetermination()

    criteria = [
        TypeCriterion(
            type_name="floor_plate_progenitor",
            required=[
                {
                    "name": "FOXA2",
                    "source": "gene",
                    "threshold": 1.0,
                },
                {
                    "name": "SHH",
                    "source": "node",
                    "threshold": 1.0,
                },
            ],
        )
    ]

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=0.5,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }

    result = determination.determine(
        criteria=criteria,
        node_states=node_states,
        gene_states=gene_states,
    )

    assert result is None


def test_type_determination_does_not_require_supporting_evidence():
    determination = TypeDetermination()

    criteria = [
        TypeCriterion(
            type_name="floor_plate_progenitor",
            required=[
                {
                    "name": "FOXA2",
                    "source": "gene",
                    "threshold": 1.0,
                },
                {
                    "name": "SHH",
                    "source": "node",
                    "threshold": 1.0,
                },
            ],
            supporting=[
                {
                    "name": "H3K27ac",
                    "source": "node",
                    "threshold": 1.0,
                },
            ],
        )
    ]

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }

    result = determination.determine(
        criteria=criteria,
        node_states=node_states,
        gene_states=gene_states,
    )

    assert result == "floor_plate_progenitor"
    
from internalnet.hir.type.repository import (
    TypeCriteriaRepository,
    TypeCriterion,
)

def test_type_criteria_repository_loads_criteria():
    path = Path(
        "internalnet/hir/library/type_criteria.json"
    )

    repository = TypeCriteriaRepository(path)

    criterion = repository.find_by_type(
        "floor_plate_progenitor"
    )

    assert isinstance(criterion, TypeCriterion)

    assert criterion.type_name == "floor_plate_progenitor"

    assert criterion.required == [
        {
            "name": "FOXA2",
            "source": "gene",
            "threshold": 1.0,
        },
        {
            "name": "SHH",
            "source": "node",
            "threshold": 1.0,
        },
    ]

    assert criterion.supporting == [
        {
            "name": "H3K27ac",
            "source": "node",
            "threshold": 1.0,
        }
    ]
    
def test_type_criteria_repository_raises_for_unknown_type():
    path = Path(
        "internalnet/hir/library/type_criteria.json"
    )

    repository = TypeCriteriaRepository(path)

    with pytest.raises(KeyError):
        repository.find_by_type("unknown_type")
        
def test_type_determination_respects_evidence_source():
    determination = TypeDetermination()

    criteria = [
        TypeCriterion(
            type_name="floor_plate_progenitor",
            required=[
                {
                    "name": "FOXA2",
                    "source": "gene",
                    "threshold": 1.0,
                },
            ],
        )
    ]

    node_states = {
        "FOXA2": NodeRuntimeState(
            node_name="FOXA2",
            total=10.0,
        ),
    }

    result = determination.determine(
        criteria=criteria,
        node_states=node_states,
        gene_states={},
    )

    assert result is None
    
def test_type_determination_works_with_repository():
    repository = TypeCriteriaRepository(
        Path("internalnet/hir/library/type_criteria.json")
    )

    determination = TypeDetermination()

    criteria = repository.all()

    node_states = {
        "SHH": NodeState(
            name="SHH",
            total=1.0,
        ),
    }

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=0.0,
            value=1.0,
        ),
    }

    result = determination.determine(
        criteria=criteria,
        node_states=node_states,
        gene_states=gene_states,
    )

    assert result == "floor_plate_progenitor"
    
    
def test_behavior_runtime_state_keeps_internal_outputs():
    state = BehaviorRuntimeState(
        behavior_name="production",
        source_type="gene",
        source_name="FOXA2",
        value=0.5,
        internal_outputs={
            "node": {
                "target": "FOXA2",
                "state": "total",
            }
        },
    )

    assert state.internal_outputs == {
        "node": {
            "target": "FOXA2",
            "state": "total",
        }
    }
    
def test_hir_engine_resolves_release_external_output_from_behavior_definition():
    class FakeBehaviorEngine:

        def run_execution(
            self,
            execution,
            parameters,
        ):
            return BehaviorIntention(
                behavior_name=execution.behavior_name,
                value=2.0,
                outputs={
                    "extracellular": {
                        "target": "source_name",
                        "amount": 1.0,
                    }
                },
            )

    class FakeTFRegulator:

        def regulate(
            self,
            intention,
            behavior_genes,
            node_states,
            gene_definitions,
        ):
            return TFRegulationDelta(
                behavior_name=intention.behavior_name,
                delta=0.0,
            )

    class FakeResourceAllocator:

        def allocate(
            self,
            behavior_name,
            behavior_value,
            resource_coefficients,
        ):
            return ResourceAllocation(
                behavior_name=behavior_name,
                resources={},
            )

    class FakeResourceRealizer:

        def realize(
            self,
            intention,
            allocation,
            available_resources,
        ):
            return ResourceDelta(
                behavior_name=intention.behavior_name,
                delta=0.0,
            )

    class FakeBehaviorStateMerger:

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
        ):
            return BehaviorRuntimeState(
                behavior_name=intention.behavior_name,
                source_type=source_type,
                source_name=source_name,
                node_states=dict(node_states),
                gene_states=dict(gene_states),
                value=intention.value + resource_delta.delta,
                internal_outputs=internal_outputs or {},
            )

    class FakeLabelDetermination:

        def determine(
            self,
            node_states,
            node_definitions,
        ):
            return set()

    class FakeTypeDetermination:

        def determine(
            self,
            criteria,
            node_states,
            gene_states,
        ):
            return None

    class FakeTypeCriteriaRepository:

        def all(self):
            return []

    plan = CellComputePlan(
        cell_id="cell_1",
        candidate_behaviors=("release",),
        edges=(
            GraphEdge(
                name="SHH_release",
                type="node-behavior",
                source="SHH",
                target="release",
            ),
        ),
    )

    engine = HIREngine(
        behavior_engine=FakeBehaviorEngine(),
        tf_regulator=FakeTFRegulator(),
        resource_allocator=FakeResourceAllocator(),
        resource_realizer=FakeResourceRealizer(),
        behavior_state_merger=FakeBehaviorStateMerger(),
        label_determination=FakeLabelDetermination(),
        type_determination=FakeTypeDetermination(),
        type_criteria_repository=FakeTypeCriteriaRepository(),
    )

    output = engine.run(
        plan=plan,
        node_states={
            "SHH": NodeState(
                name="SHH",
                total=1.0,
            ),
        },
        gene_states={},
        gene_definitions={},
        node_definitions={},
        behavior_parameters={
            "release": {},
        },
        resource_coefficients={},
        available_resources={},
    )

    assert output.external_effects["release:SHH"].behavior_name == "release"
    assert output.external_effects["release:SHH"].effect_type == "extracellular"
    assert output.external_effects["release:SHH"].target == "SHH"
    assert output.external_effects["release:SHH"].value == 2.0
