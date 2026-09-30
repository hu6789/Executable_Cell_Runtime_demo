import json
import pytest
from pathlib import Path

from internalnet.behavior_engine.schema import (
    BehaviorDefinition,
    BehaviorIntention,
    BehaviorRuntimeState,
)
from internalnet.behavior_engine.input_resolver import (
    BehaviorExecution,
    BehaviorInputs,
)
from internalnet.runtime.state import NodeState


def test_behavior_definition_defaults():
    behavior = BehaviorDefinition(name="production")

    assert behavior.name == "production"
    assert behavior.category is None
    assert behavior.formula == {}
    assert behavior.resources == {}
    assert behavior.internal_outputs == {}
    assert behavior.outputs == {}


def test_behavior_definition_fields():
    behavior = BehaviorDefinition(
        name="production",
        category="biosynthesis",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
        resources={
            "consumption": {
                "ATP": 2.0,
                "molecule": 1.0,
            },
            "occupancy": {
                "enzyme": 0.1,
            },
        },
        internal_outputs={
            "node": {
                "target": "source_name",
                "state": "total",
            },
        },
    )

    assert behavior.name == "production"
    assert behavior.category == "biosynthesis"
    assert behavior.formula["equation"] == "v = α × R"
    assert behavior.resources["consumption"]["ATP"] == 2.0
    assert behavior.internal_outputs["node"]["target"] == "source_name"
    assert behavior.internal_outputs["node"]["state"] == "total"
    assert behavior.outputs == {}

def test_behavior_definition_is_frozen():
    behavior = BehaviorDefinition(name="production")

    try:
        behavior.name = "release"
        assert False
    except AttributeError:
        pass


def test_behavior_intention_defaults():
    intention = BehaviorIntention(
        behavior_name="production",
        value=0.8,
    )

    assert intention.behavior_name == "production"
    assert intention.value == 0.8
    assert intention.inputs == {}


def test_behavior_intention_preserves_inputs():
    intention = BehaviorIntention(
        behavior_name="production",
        value=0.8,
        inputs={
            "FOXA2": 0.7,
            "H3K27ac": 0.4,
        },
    )

    assert intention.inputs["FOXA2"] == 0.7
    assert intention.inputs["H3K27ac"] == 0.4


def test_behavior_runtime_state():
    state = BehaviorRuntimeState(
        behavior_name="production",
        intention=0.8,
        value=0.6,
    )

    assert state.behavior_name == "production"
    assert state.intention == 0.8
    assert state.value == 0.6


def test_behavior_runtime_state_is_frozen():
    state = BehaviorRuntimeState(
        behavior_name="production",
        intention=0.8,
        value=0.6,
    )

    try:
        state.value = 1.0
        assert False
    except AttributeError:
        pass
        
        
from internalnet.behavior_engine.repository import BehaviorRepository

def test_behavior_repository_register_and_get():
    behavior = BehaviorDefinition(
        name="production",
        formula={"equation": "v = α × R"},
        internal_outputs={
            "node": {
                "target": "source_name",
                "state": "total",
            },
        },
    )

    repository = BehaviorRepository()
    repository.register(behavior)

    assert repository.get("production") == behavior


def test_behavior_repository_has():
    behavior = BehaviorDefinition(name="production")

    repository = BehaviorRepository([behavior])

    assert repository.has("production")
    assert not repository.has("release")


def test_behavior_repository_names():
    behaviors = [
        BehaviorDefinition(name="production"),
        BehaviorDefinition(name="release"),
    ]

    repository = BehaviorRepository(behaviors)

    assert repository.names() == ("production", "release")


def test_behavior_repository_rejects_duplicate():
    behavior = BehaviorDefinition(name="production")
    repository = BehaviorRepository([behavior])

    try:
        repository.register(behavior)
        assert False
    except ValueError as exc:
        assert str(exc) == "Behavior already registered: production"


def test_behavior_repository_rejects_unknown():
    repository = BehaviorRepository()

    try:
        repository.get("production")
        assert False
    except KeyError as exc:
        assert str(exc) == "'Unknown behavior: production'"
        
        
from internalnet.behavior_engine.input_resolver import (
    BehaviorInputs,
    BehaviorInputResolver,
)
from internalnet.graph_engine.schema import GraphEdge
from internalnet.compute_plan.schema import CellComputePlan
from internalnet.node_engine.schema import NodeRuntimeState
from internalnet.runtime.state import GeneState


def test_behavior_inputs_defaults():
    inputs = BehaviorInputs()

    assert inputs.nodes == {}
    assert inputs.genes == {}


def test_behavior_input_resolver_resolves_node_behavior():
    plan = CellComputePlan(
        cell_id="cell_A",
        edges=(
            GraphEdge(
                name="SHH_release",
                type="node-behavior",
                source="SHH",
                target="release",
            ),
        ),
    )

    shh_state = NodeRuntimeState(
        node_name="SHH",
        total=0.8,
        states={"free": 0.8},
    )

    resolver = BehaviorInputResolver()

    inputs = resolver.resolve(
        behavior_name="release",
        plan=plan,
        node_states={"SHH": shh_state},
        gene_states={},
    )

    assert inputs.nodes["SHH"] == shh_state
    assert inputs.genes == {}


def test_behavior_input_resolver_resolves_gene_behavior():
    plan = CellComputePlan(
        cell_id="cell_B",
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ),
    )

    foxa2_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.7,
        modifications={"lysine_modification": 0.4},
    )

    resolver = BehaviorInputResolver()

    inputs = resolver.resolve(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states={"FOXA2": foxa2_state},
    )

    assert inputs.genes["FOXA2"] == foxa2_state
    assert inputs.nodes == {}


def test_behavior_input_resolver_resolves_multiple_inputs():
    plan = CellComputePlan(
        cell_id="cell_B",
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
            GraphEdge(
                name="SHH_production",
                type="node-behavior",
                source="SHH",
                target="production",
            ),
        ),
    )

    foxa2_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.7,
    )

    shh_state = NodeRuntimeState(
        node_name="SHH",
        total=0.5,
        states={"free": 0.5},
    )

    resolver = BehaviorInputResolver()

    inputs = resolver.resolve(
        behavior_name="production",
        plan=plan,
        node_states={"SHH": shh_state},
        gene_states={"FOXA2": foxa2_state},
    )

    assert inputs.nodes["SHH"] == shh_state
    assert inputs.genes["FOXA2"] == foxa2_state


def test_behavior_input_resolver_returns_empty_for_no_edge():
    plan = CellComputePlan(
        cell_id="cell_A",
        edges=(),
    )

    resolver = BehaviorInputResolver()

    inputs = resolver.resolve(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states={},
    )

    assert inputs.nodes == {}
    assert inputs.genes == {}


def test_behavior_input_resolver_rejects_missing_node_state():
    plan = CellComputePlan(
        cell_id="cell_A",
        edges=(
            GraphEdge(
                name="SHH_release",
                type="node-behavior",
                source="SHH",
                target="release",
            ),
        ),
    )

    resolver = BehaviorInputResolver()

    try:
        resolver.resolve(
            behavior_name="release",
            plan=plan,
            node_states={},
            gene_states={},
        )
        assert False
    except KeyError as exc:
        assert str(exc) == (
            "'Missing NodeState for behavior input: SHH'"
        )


def test_behavior_input_resolver_rejects_missing_gene_state():
    plan = CellComputePlan(
        cell_id="cell_B",
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ),
    )

    resolver = BehaviorInputResolver()

    try:
        resolver.resolve(
            behavior_name="production",
            plan=plan,
            node_states={},
            gene_states={},
        )
        assert False
    except KeyError as exc:
        assert str(exc) == (
            "'Missing GeneState for behavior input: FOXA2'"
        )
        
        

from internalnet.behavior_engine.formulation import BehaviorFormulationEngine
from internalnet.behavior_engine.schema import BehaviorDefinition
from internalnet.behavior_engine.input_resolver import BehaviorInputs
from internalnet.node_engine.schema import NodeRuntimeState
from internalnet.runtime.state import GeneState


def test_production_formula_uses_gene_value_and_parameter():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    inputs = BehaviorInputs(
        genes={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=1.0,
                value=2.0,
                modifications={},
            )
        }
    )

    engine = BehaviorFormulationEngine()

    intention = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "production_rate": 0.5,
        },
    )

    assert intention.behavior_name == "production"
    assert intention.value == 1.0
    assert intention.inputs["gene_behavior_signal"] == 2.0


def test_release_formula_uses_node_free_and_parameter():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.free",
            },
        },
    )

    inputs = BehaviorInputs(
        nodes={
            "SHH": NodeRuntimeState(
                node_name="SHH",
                total=0.0,
                states={
                    "free": 4.0,
                },
            )
        }
    )

    engine = BehaviorFormulationEngine()

    intention = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "release_rate": 0.25,
        },
    )

    assert intention.behavior_name == "release"
    assert intention.value == 1.0
    assert intention.inputs["source_node.free"] == 4.0


def test_production_requires_production_rate():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    inputs = BehaviorInputs(
        genes={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=1.0,
                value=2.0,
                modifications={},
            )
        }
    )

    engine = BehaviorFormulationEngine()

    try:
        engine.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters={},
        )
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_release_requires_release_rate():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.total",
            },
        },
    )

    inputs = BehaviorInputs(
        nodes={
            "SHH": NodeRuntimeState(
                node_name="SHH",
                total=4.0,
                states={},
            )
        }
    )

    engine = BehaviorFormulationEngine()

    try:
        engine.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters={
                "production_rate": 0.5,
            },
        )
        assert False, "Expected KeyError"
    except KeyError as exc:
        assert exc.args[0] == "Missing behavior parameter: release_rate"

def test_release_skips_without_node_input():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.total",
            },
        },
    )

    inputs = BehaviorInputs()

    engine = BehaviorFormulationEngine()

    result = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "release_rate": 0.25,
        },
    )

    assert result is None


def test_release_skips_without_node_input():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.total",
            },
        },
    )

    inputs = BehaviorInputs()

    engine = BehaviorFormulationEngine()

    result = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "release_rate": 0.25,
        },
    )

    assert result is None


def test_formulation_does_not_mutate_inputs():
    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=2.0,
        modifications={},
    )

    inputs = BehaviorInputs(
        genes={
            "FOXA2": gene_state,
        }
    )

    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    engine = BehaviorFormulationEngine()

    try:
        engine.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters={
                "production_rate": 0.5,
            },
        )
    except Exception:
        pass

    assert inputs.genes["FOXA2"] == gene_state
    

from internalnet.behavior_engine.engine import BehaviorEngine
from internalnet.behavior_engine.repository import BehaviorRepository
from internalnet.behavior_engine.schema import BehaviorDefinition
from internalnet.behavior_engine.input_resolver import BehaviorInputResolver

from internalnet.compute_plan.schema import CellComputePlan
from internalnet.graph_engine.schema import GraphEdge
from internalnet.node_engine.schema import NodeRuntimeState
from internalnet.runtime.state import GeneState


def test_behavior_engine_runs_production():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_A",
        graph_ids=("test_graph",),
        candidate_behaviors=("production",),
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ),
    )

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=1.0,
            value=2.0,
            modifications={},
        )
    }

    intention = engine.run(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states=gene_states,
        parameters={
            "production_rate": 0.5,
        },
    )

    assert intention.behavior_name == "production"
    assert intention.value == 1.0


def test_behavior_engine_runs_release():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.free",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_B",
        graph_ids=("test_graph",),
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

    node_states = {
        "SHH": NodeRuntimeState(
            node_name="SHH",
            total=0.0,
            states={
                "free": 4.0,
            },
        )
    }

    intention = engine.run(
        behavior_name="release",
        plan=plan,
        node_states=node_states,
        gene_states={},
        parameters={
            "release_rate": 0.25,
        },
    )

    assert intention.behavior_name == "release"
    assert intention.value == 1.0


def test_behavior_engine_uses_graph_edges_to_resolve_inputs():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_A",
        candidate_behaviors=("production",),
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ),
    )

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=1.0,
            value=3.0,
            modifications={},
        ),
        "SHH": GeneState(
            name="SHH",
            baseline=1.0,
            value=99.0,
            modifications={},
        ),
    }

    intention = engine.run(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states=gene_states,
        parameters={
            "production_rate": 0.5,
        },
    )

    # Only FOXA2 is connected to production by the Graph.
    assert intention.inputs["gene_behavior_signal"] == 3.0
    assert intention.value == 1.5


def test_behavior_engine_rejects_unknown_behavior():
    repository = BehaviorRepository()

    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_A",
        candidate_behaviors=(),
        edges=(),
    )

    try:
        engine.run(
            behavior_name="unknown",
            plan=plan,
            node_states={},
            gene_states={},
            parameters={},
        )
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_behavior_engine_does_not_mutate_runtime_states():
    behavior = BehaviorDefinition(
        name="release",
        formula={
            "equation": "v = k_r × X_source",
            "parameters": {
                "k_r": "release_rate",
                "X_source": "source_node.total",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_B",
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

    node_state = NodeRuntimeState(
        node_name="SHH",
        total=4.0,
        states={},
    )

    node_states = {
        "SHH": node_state,
    }

    engine.run(
        behavior_name="release",
        plan=plan,
        node_states=node_states,
        gene_states={},
        parameters={
            "release_rate": 0.25,
        },
    )

    assert node_states["SHH"] == node_state
    
    
def test_behavior_input_resolver_resolves_gene_execution():
    plan = CellComputePlan(
        cell_id="cell_B",
        edges=(
            GraphEdge(
                name="FOXA2_production",
                type="gene-behavior",
                source="FOXA2",
                target="production",
            ),
        ),
    )

    foxa2_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.7,
    )

    resolver = BehaviorInputResolver()

    executions = resolver.resolve_executions(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states={"FOXA2": foxa2_state},
    )

    assert len(executions) == 1

    execution = executions[0]

    assert execution.behavior_name == "production"
    assert execution.source_type == "gene"
    assert execution.source_name == "FOXA2"
    assert execution.inputs.genes == {
        "FOXA2": foxa2_state,
    }
    assert execution.inputs.nodes == {}
    
def test_behavior_input_resolver_resolves_independent_gene_executions():
    plan = CellComputePlan(
        cell_id="cell_B",
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

    foxa2_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.7,
    )

    shh_state = GeneState(
        name="SHH",
        baseline=1.0,
        value=0.2,
    )

    resolver = BehaviorInputResolver()

    executions = resolver.resolve_executions(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states={
            "FOXA2": foxa2_state,
            "SHH": shh_state,
        },
    )

    assert len(executions) == 2

    assert executions[0].behavior_name == "production"
    assert executions[0].source_type == "gene"
    assert executions[0].source_name == "FOXA2"
    assert executions[0].inputs.genes == {
        "FOXA2": foxa2_state,
    }
    assert executions[0].inputs.nodes == {}

    assert executions[1].behavior_name == "production"
    assert executions[1].source_type == "gene"
    assert executions[1].source_name == "SHH"
    assert executions[1].inputs.genes == {
        "SHH": shh_state,
    }
    assert executions[1].inputs.nodes == {}
    
def test_behavior_input_resolver_resolves_node_execution():
    plan = CellComputePlan(
        cell_id="cell_B",
        edges=(
            GraphEdge(
                name="SHH_release",
                type="node-behavior",
                source="SHH",
                target="release",
            ),
        ),
    )

    shh_state = NodeRuntimeState(
        node_name="SHH",
        total=0.8,
        states={"free": 0.8},
    )

    resolver = BehaviorInputResolver()

    executions = resolver.resolve_executions(
        behavior_name="release",
        plan=plan,
        node_states={"SHH": shh_state},
        gene_states={},
    )

    assert len(executions) == 1

    execution = executions[0]

    assert execution.behavior_name == "release"
    assert execution.source_type == "node"
    assert execution.source_name == "SHH"
    assert execution.inputs.nodes == {
        "SHH": shh_state,
    }
    assert execution.inputs.genes == {}
    
def test_behavior_engine_runs_one_production_execution():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_B",
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

    foxa2_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=2.0,
    )

    shh_state = GeneState(
        name="SHH",
        baseline=1.0,
        value=99.0,
    )

    executions = engine._input_resolver.resolve_executions(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states={
            "FOXA2": foxa2_state,
            "SHH": shh_state,
        },
    )

    foxa2_execution = executions[0]

    intention = engine.run_execution(
        execution=foxa2_execution,
        parameters={
            "production_rate": 0.5,
        },
    )

    assert intention.behavior_name == "production"
    assert intention.value == 1.0
    assert intention.inputs["gene_behavior_signal"] == 2.0
    
def test_behavior_engine_runs_independent_production_executions():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    plan = CellComputePlan(
        cell_id="cell_B",
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

    gene_states = {
        "FOXA2": GeneState(
            name="FOXA2",
            baseline=1.0,
            value=2.0,
        ),
        "SHH": GeneState(
            name="SHH",
            baseline=1.0,
            value=0.4,
        ),
    }

    executions = engine._input_resolver.resolve_executions(
        behavior_name="production",
        plan=plan,
        node_states={},
        gene_states=gene_states,
    )

    foxa2_intention = engine.run_execution(
        execution=executions[0],
        parameters={"production_rate": 0.5},
    )

    shh_intention = engine.run_execution(
        execution=executions[1],
        parameters={"production_rate": 0.5},
    )

    assert foxa2_intention.value == 1.0
    assert shh_intention.value == 0.2
    
    
def test_behavior_intention_keeps_output_declarations():
    intention = BehaviorIntention(
        behavior_name="production",
        value=0.5,
        internal_outputs={
            "node": {
                "target": "source_name",
                "state": "total",
            }
        },
        outputs={},
    )

    assert intention.internal_outputs == {
        "node": {
            "target": "source_name",
            "state": "total",
        }
    }
    assert intention.outputs == {}
    
    
def test_behavior_engine_passes_output_declarations():
    behavior = BehaviorDefinition(
        name="production",
        formula={
            "equation": "v = α × R",
            "parameters": {
                "α": "production_rate",
                "R": "gene_behavior_signal",
            },
        },
        internal_outputs={
            "node": {
                "target": "source_name",
                "state": "total",
            }
        },
        outputs={},
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository)

    execution = BehaviorExecution(
        behavior_name="production",
        source_type="gene",
        source_name="FOXA2",
        inputs=BehaviorInputs(
            genes={
                "FOXA2": GeneState(
                    name="FOXA2",
                    baseline=1.0,
                    value=1.0,
                )
            }
        ),
    )

    intention = engine.run_execution(
        execution=execution,
        parameters={
            "production_rate": 0.5,
        },
    )

    assert intention is not None
    assert intention.value == 0.5
    assert intention.internal_outputs == {
        "node": {
            "target": "source_name",
            "state": "total",
        }
    }
    assert intention.outputs == {}
    
def test_gli3_truncation_calculates_michaelis_menten_rate():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
        category="special",
        formula={
            "equation": "v = V_max × X_free / (K_m + X_free)"
        },
        internal_outputs={
            "node": [
                {
                    "target": "GLI3",
                    "state": "free",
                    "mode": "consume",
                },
                {
                    "target": "GLI3",
                    "state": "repressor",
                    "mode": "produce",
                },
            ]
        },
    )

    inputs = BehaviorInputs(
        nodes={
            "GLI3": NodeState(
                name="GLI3",
                total=10.0,
                states={
                    "free": 4.0,
                    "repressor": 2.0,
                },
            )
        }
    )

    engine = BehaviorFormulationEngine()

    intention = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "truncation_rate": 2.0,
            "truncation_Km": 4.0,
        },
    )

    assert intention is not None

    # v = 2 × 4 / (4 + 4) = 1
    assert intention.value == 1.0

    assert intention.inputs["GLI3.free"] == 4.0
    
    
def test_gli3_truncation_returns_zero_when_free_is_zero():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
    )

    inputs = BehaviorInputs(
        nodes={
            "GLI3": NodeState(
                name="GLI3",
                total=10.0,
                states={
                    "free": 0.0,
                    "repressor": 5.0,
                },
            )
        }
    )

    engine = BehaviorFormulationEngine()

    intention = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "truncation_rate": 2.0,
            "truncation_Km": 4.0,
        },
    )

    assert intention is not None
    assert intention.value == 0.0
    
def test_gli3_truncation_requires_truncation_rate():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
    )

    inputs = BehaviorInputs(
        nodes={
            "GLI3": NodeState(
                name="GLI3",
                total=10.0,
                states={"free": 4.0},
            )
        }
    )

    engine = BehaviorFormulationEngine()

    with pytest.raises(KeyError, match="truncation_rate"):
        engine.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters={
                "truncation_Km": 4.0,
            },
        )
        
        
def test_gli3_truncation_requires_truncation_Km():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
    )

    inputs = BehaviorInputs(
        nodes={
            "GLI3": NodeState(
                name="GLI3",
                total=10.0,
                states={"free": 4.0},
            )
        }
    )

    engine = BehaviorFormulationEngine()

    with pytest.raises(KeyError, match="truncation_Km"):
        engine.evaluate(
            behavior=behavior,
            inputs=inputs,
            parameters={
                "truncation_rate": 2.0,
            },
        )
        
def test_gli3_truncation_returns_none_without_gli3_input():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
    )

    inputs = BehaviorInputs()

    engine = BehaviorFormulationEngine()

    intention = engine.evaluate(
        behavior=behavior,
        inputs=inputs,
        parameters={
            "truncation_rate": 2.0,
            "truncation_Km": 4.0,
        },
    )

    assert intention is None
    
    
def test_gli3_truncation_preserves_multiple_internal_outputs():
    behavior = BehaviorDefinition(
        name="GLI3_truncation",
        formula={
            "equation": "v = V_max × X_free / (K_m + X_free)",
            "parameters": {
                "V_max": "truncation_rate",
                "K_m": "truncation_Km",
                "X_free": "GLI3.free",
            },
        },
        internal_outputs={
            "node": [
                {
                    "target": "GLI3",
                    "state": "free",
                    "mode": "consume",
                },
                {
                    "target": "GLI3",
                    "state": "repressor",
                    "mode": "produce",
                },
            ]
        },
    )

    repository = BehaviorRepository([behavior])
    engine = BehaviorEngine(repository=repository)

    execution = BehaviorExecution(
        behavior_name="GLI3_truncation",
        source_type="node",
        source_name="GLI3",
        inputs=BehaviorInputs(
            nodes={
                "GLI3": NodeState(
                    name="GLI3",
                    total=10.0,
                    states={
                        "free": 4.0,
                        "repressor": 2.0,
                    },
                )
            }
        ),
    )

    intention = engine.run_execution(
        execution=execution,
        parameters={
            "truncation_rate": 2.0,
            "truncation_Km": 4.0,
        },
    )

    assert intention is not None
    assert intention.value == 1.0

    assert intention.internal_outputs == {
        "node": [
            {
                "target": "GLI3",
                "state": "free",
                "mode": "consume",
            },
            {
                "target": "GLI3",
                "state": "repressor",
                "mode": "produce",
            },
        ]
    }
