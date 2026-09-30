# test/test_passive.py
import pytest
from internalnet.passive_engine.schema import (
    PassiveDefinition,
    PassiveRuntimeState,
)


def test_passive_definition_defaults():
    passive = PassiveDefinition(
        name="diffusion",
    )

    assert passive.name == "diffusion"
    assert passive.formula == {}
    assert passive.update == {}


def test_passive_definition_stores_formula_and_update():
    passive = PassiveDefinition(
        name="diffusion",
        formula={
            "equation": "Δ = min(D × X_free × Δt, X_free)",
            "parameters": {
                "D": "node.diffusion",
            },
        },
        update={
            "target_state": "nuclear",
        },
    )

    assert passive.name == "diffusion"
    assert passive.formula["equation"] == (
        "Δ = min(D × X_free × Δt, X_free)"
    )
    assert passive.formula["parameters"]["D"] == "node.diffusion"
    assert passive.update["target_state"] == "nuclear"


def test_passive_runtime_state_defaults():
    runtime_state = PassiveRuntimeState(
        node_name="FOXA2",
        passive_name="diffusion",
        
    )

    assert runtime_state.node_name == "FOXA2"
    assert runtime_state.passive_name == "diffusion"
    assert runtime_state.state_changes == {}


def test_passive_runtime_state_stores_state_changes():
    runtime_state = PassiveRuntimeState(
        node_name="FOXA2",
        passive_name="diffusion",
        state_changes={
            "free": -1.5,
            "nuclear": 1.5,
        },
    )

    assert runtime_state.node_name == "FOXA2"
    assert runtime_state.passive_name == "diffusion"
    assert runtime_state.state_changes == {
        "free": -1.5,
        "nuclear": 1.5,
    }


def test_passive_runtime_state_is_immutable():
    runtime_state = PassiveRuntimeState(
        node_name="FOXA2",
        passive_name="diffusion",
        state_changes={
            "free": -1.5,
            "nuclear": 1.5,
        },
    )

    try:
        runtime_state.node_name = "GLI2"
    except Exception:
        pass
    else:
        raise AssertionError("PassiveRuntimeState should be immutable")
        
        
        
from internalnet.passive_engine.repository import PassiveRepository

def test_passive_repository_register_and_get():
    passive = PassiveDefinition(name="diffusion")

    repository = PassiveRepository()
    repository.register(passive)

    assert repository.get("diffusion") == passive


def test_passive_repository_has():
    repository = PassiveRepository(
        [
            PassiveDefinition(name="diffusion"),
            PassiveDefinition(name="half_life_decay"),
        ]
    )

    assert repository.has("diffusion")
    assert repository.has("half_life_decay")
    assert not repository.has("unknown")


def test_passive_repository_names():
    repository = PassiveRepository(
        [
            PassiveDefinition(name="diffusion"),
            PassiveDefinition(name="half_life_decay"),
        ]
    )

    assert repository.names() == (
        "diffusion",
        "half_life_decay",
    )


def test_passive_repository_all():
    diffusion = PassiveDefinition(name="diffusion")
    decay = PassiveDefinition(name="half_life_decay")

    repository = PassiveRepository([diffusion, decay])

    assert repository.all() == (
        diffusion,
        decay,
    )


def test_passive_repository_rejects_duplicate_name():
    repository = PassiveRepository()

    repository.register(
        PassiveDefinition(name="diffusion")
    )

    try:
        repository.register(
            PassiveDefinition(name="diffusion")
        )
    except ValueError as exc:
        assert str(exc) == "Passive already registered: diffusion"
    else:
        raise AssertionError(
            "Duplicate passive registration should raise ValueError"
        )


def test_passive_repository_get_missing_raises():
    repository = PassiveRepository()

    try:
        repository.get("unknown")
    except KeyError as exc:
        assert str(exc) == "'Passive not found: unknown'"
    else:
        raise AssertionError(
            "Missing passive should raise KeyError"
        )


def test_passive_repository_remove():
    passive = PassiveDefinition(name="diffusion")
    repository = PassiveRepository([passive])

    removed = repository.remove("diffusion")

    assert removed == passive
    assert not repository.has("diffusion")


def test_passive_repository_clear():
    repository = PassiveRepository(
        [
            PassiveDefinition(name="diffusion"),
            PassiveDefinition(name="half_life_decay"),
        ]
    )

    repository.clear()

    assert len(repository) == 0
    assert repository.names() == ()


def test_passive_repository_len_and_contains():
    repository = PassiveRepository(
        [
            PassiveDefinition(name="diffusion"),
            PassiveDefinition(name="half_life_decay"),
        ]
    )

    assert len(repository) == 2
    assert "diffusion" in repository
    assert "half_life_decay" in repository
    assert "unknown" not in repository
    
    
    
from internalnet.node_engine.schema import (
    NodeDefinition,
    NodeRuntimeState,
)

from internalnet.passive_engine.formulation import (
    PassiveFormulationEngine,
)

def test_diffusion():
    passive = PassiveDefinition(
        name="diffusion",
        formula={
            "equation": "Δ = min(D × X_free × Δt, X_free)",
        },
        update={
            "target_state": "nuclear",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        diffusion=0.5,
        diffusion_source_states=["free"],
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=1.0,
    )

    assert result == {
        "free": -3.0,
        "nuclear": 3.0,
    }


def test_diffusion_does_not_exceed_source_state():
    passive = PassiveDefinition(
        name="diffusion",
        update={
            "target_state": "nuclear",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        diffusion=10.0,
        diffusion_source_states=["free"],
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=1.0,
        states={
            "free": 2.0,
            "nuclear": 0.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=1.0,
    )

    assert result == {
        "free": -2.0,
        "nuclear": 2.0,
    }


def test_diffusion_with_zero_dt():
    passive = PassiveDefinition(
        name="diffusion",
        update={
            "target_state": "nuclear",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        diffusion=0.5,
        diffusion_source_states=["free"],
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=0.0,
    )

    assert result == {
        "free": 0.0,
        "nuclear": 0.0,
    }


def test_diffusion_with_no_coefficient_raises():
    passive = PassiveDefinition(
        name="diffusion",
        update={
            "target_state": "nuclear",
        },
    )

    node = NodeDefinition(
        name="ATP",
        category="resource",
        diffusion=None,
    )

    runtime_state = NodeRuntimeState(
        node_name="ATP",
        total=10.0,
        states={
            "free": 10.0,
        },
    )

    try:
        PassiveFormulationEngine().evaluate(
            passive,
            node,
            runtime_state,
            dt=1.0,
        )
    except ValueError as exc:
        assert str(exc) == (
            "Node has no diffusion coefficient: ATP"
        )
    else:
        raise AssertionError(
            "Missing diffusion coefficient should raise ValueError"
        )


def test_half_life_decay_is_proportional_across_states():
    passive = PassiveDefinition(
        name="half_life_decay",
        formula={
            "equation": (
                "Δ = X_total × "
                "(1 - exp(-ln(2) × Δt / t_half))"
            ),
        },
        update={
            "target": "all_states",
            "mode": "proportional_decay",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        half_life=60.0,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=60.0,
    )

    assert result["free"] == -3.0
    assert result["nuclear"] == -2.0


def test_half_life_decay_preserves_state_proportions():
    passive = PassiveDefinition(
        name="half_life_decay",
        update={
            "target": "all_states",
            "mode": "proportional_decay",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        half_life=60.0,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=20.0,
        states={
            "free": 5.0,
            "nuclear": 15.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=60.0,
    )

    assert result["free"] == -2.5
    assert result["nuclear"] == -7.5


def test_half_life_decay_with_zero_dt():
    passive = PassiveDefinition(
        name="half_life_decay",
        update={
            "target": "all_states",
            "mode": "proportional_decay",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        half_life=60.0,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=0.0,
    )

    assert result == {
        "free": 0.0,
        "nuclear": 0.0,
    }


def test_half_life_decay_with_zero_total():
    passive = PassiveDefinition(
        name="half_life_decay",
        update={
            "target": "all_states",
            "mode": "proportional_decay",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        half_life=60.0,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=0.0,
        states={
            "free": 0.0,
            "nuclear": 0.0,
        },
    )

    result = PassiveFormulationEngine().evaluate(
        passive,
        node,
        runtime_state,
        dt=60.0,
    )

    assert result == {
        "free": 0.0,
        "nuclear": 0.0,
    }


def test_half_life_decay_requires_positive_half_life():
    passive = PassiveDefinition(
        name="half_life_decay",
        update={
            "target": "all_states",
            "mode": "proportional_decay",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        half_life=0.0,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    try:
        PassiveFormulationEngine().evaluate(
            passive,
            node,
            runtime_state,
            dt=1.0,
        )
    except ValueError as exc:
        assert str(exc) == (
            "Node half-life must be positive: FOXA2"
        )
    else:
        raise AssertionError(
            "Non-positive half-life should raise ValueError"
        )

def test_sufu_binding():
    passive = PassiveDefinition(
        name="sufu_binding",
        applies_to=["GLI2"],
        formula={
            "equation": "Δ = min(k_bind × X_free × Δt, X_free)",
            "parameters": {
                "k_bind": 0.5,
            },
        },
        update={
            "source_state": "free",
            "target_state": "SUFU_bound",
        },
    )

    node = NodeDefinition(
        name="GLI2",
        category="TF",
        polymorphism=(
            "SUFU_bound",
            "free",
            "nuclear",
        ),
        half_life=60,
        diffusion=0.5,
        diffusion_source_states=("free",),
    )

    runtime_state = NodeRuntimeState(
        node_name="GLI2",
        total=1.0,
        states={
            "SUFU_bound": 0.2,
            "free": 0.8,
            "nuclear": 0.0,
        },
    )

    engine = PassiveFormulationEngine()

    delta = engine.evaluate(
        passive=passive,
        node=node,
        runtime_state=runtime_state,
        dt=1.0,
    )

    assert delta["free"] == -0.4
    assert delta["SUFU_bound"] == 0.4
    
    
def test_sufu_binding_does_not_exceed_free_state():
    passive = PassiveDefinition(
        name="sufu_binding",
        applies_to=["GLI2"],
        formula={
            "equation": "Δ = min(k_bind × X_free × Δt, X_free)",
            "parameters": {
                "k_bind": 0.5,
            },
        },
        update={
            "source_state": "free",
            "target_state": "SUFU_bound",
        },
    )

    node = NodeDefinition(
        name="GLI2",
        category="TF",
        polymorphism=("SUFU_bound", "free"),
        half_life=60,
        diffusion=None,
        diffusion_source_states=(),
    )

    runtime_state = NodeRuntimeState(
        node_name="GLI2",
        total=1.0,
        states={
            "SUFU_bound": 0.9,
            "free": 0.1,
        },
    )

    engine = PassiveFormulationEngine()

    delta = engine.evaluate(
        passive=passive,
        node=node,
        runtime_state=runtime_state,
        dt=10.0,
    )

    assert delta["free"] == -0.1
    assert delta["SUFU_bound"] == 0.1
    
    
def test_sufu_binding_with_zero_dt():
    passive = PassiveDefinition(
        name="sufu_binding",
        applies_to=["GLI2"],
        formula={
            "equation": "Δ = min(k_bind × X_free × Δt, X_free)",
            "parameters": {
                "k_bind": 0.5,
            },
        },
        update={
            "source_state": "free",
            "target_state": "SUFU_bound",
        },
    )

    node = NodeDefinition(
        name="GLI2",
        category="TF",
        polymorphism=("SUFU_bound", "free"),
    )

    runtime_state = NodeRuntimeState(
        node_name="GLI2",
        total=1.0,
        states={
            "SUFU_bound": 0.2,
            "free": 0.8,
        },
    )

    engine = PassiveFormulationEngine()

    delta = engine.evaluate(
        passive=passive,
        node=node,
        runtime_state=runtime_state,
        dt=0.0,
    )

    assert delta["free"] == 0.0
    assert delta["SUFU_bound"] == 0.0
    

def test_sufu_binding_requires_source_and_target_states():
    passive = PassiveDefinition(
        name="sufu_binding",
        applies_to=["GLI2"],
        formula={
            "parameters": {
                "k_bind": 0.5,
            },
        },
        update={},
    )

    node = NodeDefinition(
        name="GLI2",
        category="TF",
        polymorphism=("SUFU_bound", "free"),
    )

    runtime_state = NodeRuntimeState(
        node_name="GLI2",
        total=1.0,
        states={
            "SUFU_bound": 0.2,
            "free": 0.8,
        },
    )

    engine = PassiveFormulationEngine()

    with pytest.raises(ValueError):
        engine.evaluate(
            passive=passive,
            node=node,
            runtime_state=runtime_state,
            dt=1.0,
        )


def test_unsupported_passive_raises():
    passive = PassiveDefinition(
        name="unknown_passive",
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 10.0,
        },
    )

    try:
        PassiveFormulationEngine().evaluate(
            passive,
            node,
            runtime_state,
            dt=1.0,
        )
    except ValueError as exc:
        assert str(exc) == (
            "Unsupported passive formulation: unknown_passive"
        )
    else:
        raise AssertionError(
            "Unsupported passive should raise ValueError"
        )


def test_negative_dt_raises():
    passive = PassiveDefinition(
        name="diffusion",
        update={
            "target_state": "nuclear",
        },
    )

    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        diffusion=0.5,
        diffusion_source_states=["free"],
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    try:
        PassiveFormulationEngine().evaluate(
            passive,
            node,
            runtime_state,
            dt=-1.0,
        )
    except ValueError as exc:
        assert str(exc) == "dt must be non-negative"
    else:
        raise AssertionError(
            "Negative dt should raise ValueError"
        )
        

 
from internalnet.node_engine.repository import NodeRepository

from internalnet.passive_engine.engine import PassiveEngine
from internalnet.passive_engine.schema import (
    PassiveDefinition,
    PassiveRuntimeState,
)

from internalnet.runtime.delta import PassiveDelta
def test_passive_engine_evaluate():
    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        polymorphism=["free", "nuclear"],
        diffusion=0.5,
        diffusion_source_states=["free"],

    )

    passive = PassiveDefinition(
        name="diffusion",
        formula={
            "equation": "Δ = min(D × X_free × Δt, X_free)",
            "parameters": {
                "D": "node.diffusion",
            },
        },
        update={
            "target_state": "nuclear",
        },
    )

    node_repository = NodeRepository([node])
    passive_repository = PassiveRepository([passive])

    engine = PassiveEngine(
        passive_repository=passive_repository,
        node_repository=node_repository,
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = engine.evaluate(
        passive_name="diffusion",
        runtime_state=runtime_state,
        dt=1.0,
    )

    assert result == PassiveDelta(
        source="passive_engine",
        passive_name="diffusion",
        node_name="FOXA2",
        total_delta=0.0,
        state_deltas={
            "free": -3.0,
            "nuclear": 3.0,
        },
    )



def test_passive_engine_run():
    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        polymorphism=["free", "nuclear"],
        diffusion=0.5,
        diffusion_source_states=["free"],
    )

    passive = PassiveDefinition(
        name="diffusion",
        formula={
            "equation": "Δ = min(D × X_free × Δt, X_free)",
            "parameters": {
                "D": "node.diffusion",
            },
        },
        update={
            "target_state": "nuclear",
        },
    )

    engine = PassiveEngine(
        passive_repository=PassiveRepository([passive]),
        node_repository=NodeRepository([node]),
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    result = engine.run(
        passive_name="diffusion",
        runtime_state=runtime_state,
        dt=1.0,
    )

    assert result == PassiveDelta(
        source="passive_engine",
        passive_name="diffusion",
        node_name="FOXA2",
        total_delta=0.0,
        state_deltas={
            "free": -3.0,
            "nuclear": 3.0,
        },
    )


def test_passive_engine_run_does_not_mutate_original_state():
    node = NodeDefinition(
        name="FOXA2",
        category="TF",
        polymorphism=["free", "nuclear"],
        diffusion=0.5,
        diffusion_source_states=["free"],
    )

    passive = PassiveDefinition(
        name="diffusion",
        formula={},
        update={
            "target_state": "nuclear",
        },
    )

    engine = PassiveEngine(
        passive_repository=PassiveRepository([passive]),
        node_repository=NodeRepository([node]),
    )

    runtime_state = NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )

    engine.run(
        passive_name="diffusion",
        runtime_state=runtime_state,
        dt=1.0,
    )

    assert runtime_state == NodeRuntimeState(
        node_name="FOXA2",
        total=10.0,
        states={
            "free": 6.0,
            "nuclear": 4.0,
        },
    )
