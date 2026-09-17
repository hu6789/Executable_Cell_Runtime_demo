import pytest

from internalnet.node_engine.schema import (
    NodeDefinition,
    NodeInput,
    NodeRuntimeState,
)


# ============================================================
# Schema
# ============================================================

class TestNodeDefinition:

    def test_basic_fields(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            polymorphism=["unrecruited", "recruited"],
            half_life=60.0,
            diffusion=0.5,
        )

        assert node.name == "SMO"
        assert node.category == "functional_protein"
        assert node.polymorphism == ["unrecruited", "recruited"]
        assert node.half_life == 60.0
        assert node.diffusion == 0.5
        assert node.formulation is None

    def test_default_values(self):
        node = NodeDefinition(
            name="ATP",
            category="resource",
        )

        assert node.polymorphism == []
        assert node.half_life is None
        assert node.diffusion is None
        assert node.formulation is None

    def test_formulation_is_preserved(self):
        formulation = {
            "type": "hill_inhibition",
            "input": "PTCH1",
            "parameters": {
                "K_PTCH1": 0.5,
                "n": 2.0,
            },
        }

        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation=formulation,
        )

        assert node.formulation == formulation
        assert node.formulation["type"] == "hill_inhibition"
        assert node.formulation["input"] == "PTCH1"

    def test_is_frozen(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
        )

        with pytest.raises(Exception):
            node.name = "PTCH1"


class TestNodeInput:

    def test_basic_fields(self):
        node_input = NodeInput(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 7.0,
                "recruited": 3.0,
            },
            related_inputs={
                "PTCH1": {
                    "total": 2.0,
                    "states": {
                        "active": 1.0,
                        "inactive": 1.0,
                    },
                }
            },
        )

        assert node_input.node_name == "SMO"
        assert node_input.total == 10.0
        assert node_input.states["unrecruited"] == 7.0
        assert node_input.states["recruited"] == 3.0

        assert "PTCH1" in node_input.related_inputs
        assert node_input.related_inputs["PTCH1"]["total"] == 2.0

    def test_default_values(self):
        node_input = NodeInput(
            node_name="ATP",
            total=100.0,
        )

        assert node_input.states == {}
        assert node_input.related_inputs == {}

    def test_is_frozen(self):
        node_input = NodeInput(
            node_name="ATP",
            total=100.0,
        )

        with pytest.raises(Exception):
            node_input.node_name = "enzyme"


class TestNodeRuntimeState:

    def test_basic_fields(self):
        state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 6.0,
                "recruited": 4.0,
            },
        )

        assert state.node_name == "SMO"
        assert state.total == 10.0
        assert state.states["unrecruited"] == 6.0
        assert state.states["recruited"] == 4.0

    def test_default_values(self):
        state = NodeRuntimeState(
            node_name="ATP",
            total=100.0,
        )

        assert state.states == {}

    def test_is_frozen(self):
        state = NodeRuntimeState(
            node_name="ATP",
            total=100.0,
        )

        with pytest.raises(Exception):
            state.total = 200.0
            

# ============================================================
# Repository
# ============================================================

from internalnet.node_engine.repository import NodeRepository


class TestNodeRepository:

    def test_register_and_get(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
        )

        repository = NodeRepository()
        repository.register(node)

        assert repository.get("SMO") == node

    def test_register_multiple_nodes(self):
        nodes = [
            NodeDefinition(
                name="ATP",
                category="resource",
            ),
            NodeDefinition(
                name="PTCH1",
                category="receptor",
            ),
            NodeDefinition(
                name="SMO",
                category="functional_protein",
            ),
        ]

        repository = NodeRepository(nodes)

        assert len(repository) == 3
        assert repository.names() == (
            "ATP",
            "PTCH1",
            "SMO",
        )

    def test_has_and_contains(self):
        node = NodeDefinition(
            name="PTCH1",
            category="receptor",
        )

        repository = NodeRepository([node])

        assert repository.has("PTCH1")
        assert "PTCH1" in repository
        assert not repository.has("SMO")
        assert "SMO" not in repository

    def test_all(self):
        nodes = [
            NodeDefinition(
                name="ATP",
                category="resource",
            ),
            NodeDefinition(
                name="SMO",
                category="functional_protein",
            ),
        ]

        repository = NodeRepository(nodes)

        assert repository.all() == tuple(nodes)

    def test_duplicate_registration_raises(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
        )

        repository = NodeRepository()
        repository.register(node)

        with pytest.raises(ValueError):
            repository.register(node)

    def test_missing_node_raises(self):
        repository = NodeRepository()

        with pytest.raises(KeyError, match="Node not found: SMO"):
            repository.get("SMO")

    def test_remove(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
        )

        repository = NodeRepository([node])

        removed = repository.remove("SMO")

        assert removed == node
        assert len(repository) == 0
        assert not repository.has("SMO")

    def test_remove_missing_node_raises(self):
        repository = NodeRepository()

        with pytest.raises(KeyError, match="Node not found: SMO"):
            repository.remove("SMO")

    def test_clear(self):
        nodes = [
            NodeDefinition(
                name="ATP",
                category="resource",
            ),
            NodeDefinition(
                name="SMO",
                category="functional_protein",
            ),
        ]

        repository = NodeRepository(nodes)

        assert len(repository) == 2

        repository.clear()

        assert len(repository) == 0
        assert repository.names() == ()
        assert repository.all() == ()
        
        
# ============================================================
# Formulation
# ============================================================

from internalnet.node_engine.formulation import FormulationEngine


class TestFormulationEngine:

    def test_hill_inhibition(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "state_mapping": {
                    "active": 1.0,
                    "inactive": 0.0,
                },
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
            },
        )

        node_input = NodeInput(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 10.0,
                "recruited": 0.0,
            },
            related_inputs={
                "PTCH1": {
                    "total": 1.0,
                    "states": {
                        "active": 1.0,
                        "inactive": 0.0,
                    },
                }
            },
        )

        engine = FormulationEngine()

        result = engine.evaluate(
            node,
            node_input,
        )

        assert result["A_SMO"] == pytest.approx(0.2)

    def test_hill_inhibition_uses_state_mapping(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "state_mapping": {
                    "active": 1.0,
                    "inactive": 0.0,
                },
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
            },
        )

        node_input = NodeInput(
            node_name="SMO",
            total=10.0,
            related_inputs={
                "PTCH1": {
                    "total": 10.0,
                    "states": {
                        "active": 0.0,
                        "inactive": 10.0,
                    },
                }
            },
        )

        engine = FormulationEngine()

        result = engine.evaluate(
            node,
            node_input,
        )

        assert result["A_SMO"] == pytest.approx(1.0)

    def test_missing_related_input_raises(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "state_mapping": {
                    "active": 1.0,
                    "inactive": 0.0,
                },
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                },
            },
        )

        node_input = NodeInput(
            node_name="SMO",
            total=10.0,
        )

        engine = FormulationEngine()

        with pytest.raises(
            KeyError,
            match="Related input not found: PTCH1",
        ):
            engine.evaluate(
                node,
                node_input,
            )

    def test_node_without_formulation_returns_empty_result(self):
        node = NodeDefinition(
            name="ATP",
            category="resource",
        )

        node_input = NodeInput(
            node_name="ATP",
            total=100.0,
        )

        engine = FormulationEngine()

        result = engine.evaluate(
            node,
            node_input,
        )

        assert result == {}

    def test_unsupported_formulation_raises(self):
        node = NodeDefinition(
            name="TEST",
            category="test",
            formulation={
                "type": "unknown_formula",
            },
        )

        node_input = NodeInput(
            node_name="TEST",
            total=1.0,
        )

        engine = FormulationEngine()

        with pytest.raises(
            ValueError,
            match="Unsupported formulation type",
        ):
            engine.evaluate(
                node,
                node_input,
            )

    def test_gli2_missing_parameters_raises(self):
        node = NodeDefinition(
            name="GLI2",
            category="TF",
            formulation={
                "type": "SMO_dependent_dissociation",
                "input": "SMO",
                "equation": (
                    "D_GLI = k_diss * A_SMO^n / "
                    "(K_SMO^n + A_SMO^n)"
                ),
                "parameters": {
                    "k_diss": None,
                    "K_SMO": None,
                    "n": 2.0,
                    "theta_diss": None,
                },
            },
        )

        node_input = NodeInput(
            node_name="GLI2",
            total=10.0,
            states={
                "SUFU_bound": 10.0,
                "free": 0.0,
                "nuclear": 0.0,
            },
            related_inputs={
                "SMO": {
                    "total": 10.0,
                    "states": {
                        "unrecruited": 2.0,
                        "recruited": 8.0,
                    },
                }
            },
        )

        engine = FormulationEngine()

        with pytest.raises(
            ValueError,
            match="k_diss is not configured",
        ):
            engine.evaluate(
                node,
                node_input,
            )
            

# ============================================================
# Transition
# ============================================================

from internalnet.node_engine.transition import TransitionEngine


class TestTransitionEngine:

    def test_smo_transition_passes(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            polymorphism=[
                "unrecruited",
                "recruited",
            ],
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        runtime_state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 10.0,
                "recruited": 0.0,
            },
        )

        engine = TransitionEngine()

        result = engine.apply_transition(
            node,
            runtime_state,
            {"A_SMO": 0.8},
        )

        assert result.total == 10.0
        assert result.states["unrecruited"] == 0.0
        assert result.states["recruited"] == 10.0

    def test_smo_transition_fails(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            polymorphism=[
                "unrecruited",
                "recruited",
            ],
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        runtime_state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 10.0,
                "recruited": 0.0,
            },
        )

        engine = TransitionEngine()

        result = engine.apply_transition(
            node,
            runtime_state,
            {"A_SMO": 0.2},
        )

        assert result.total == 10.0
        assert result.states["unrecruited"] == 10.0
        assert result.states["recruited"] == 0.0

    def test_transition_preserves_total(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        runtime_state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 6.0,
                "recruited": 4.0,
            },
        )

        engine = TransitionEngine()

        result = engine.apply_transition(
            node,
            runtime_state,
            {"A_SMO": 0.8},
        )

        assert result.total == runtime_state.total
        assert sum(result.states.values()) == result.total

    def test_transition_does_not_mutate_input(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "input": "PTCH1",
                "parameters": {
                    "K_PTCH1": 0.5,
                    "n": 2.0,
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        runtime_state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "unrecruited": 10.0,
                "recruited": 0.0,
            },
        )

        engine = TransitionEngine()

        engine.apply_transition(
            node,
            runtime_state,
            {"A_SMO": 0.8},
        )

        assert runtime_state.states["unrecruited"] == 10.0
        assert runtime_state.states["recruited"] == 0.0

    def test_missing_computed_value_raises(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "parameters": {
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        engine = TransitionEngine()

        with pytest.raises(
            KeyError,
            match="Computed value not found: A_SMO",
        ):
            engine.evaluate_condition(
                node,
                {},
            )

    def test_missing_transition_parameter_raises(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "parameters": {},
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        engine = TransitionEngine()

        with pytest.raises(
            KeyError,
            match="Transition parameter not found: theta_SMO",
        ):
            engine.evaluate_condition(
                node,
                {"A_SMO": 0.8},
            )

    def test_missing_source_state_raises(self):
        node = NodeDefinition(
            name="SMO",
            category="functional_protein",
            formulation={
                "type": "hill_inhibition",
                "parameters": {
                    "theta_SMO": 0.5,
                },
                "transition": {
                    "from": "unrecruited",
                    "to": "recruited",
                    "condition": "A_SMO >= theta_SMO",
                },
            },
        )

        runtime_state = NodeRuntimeState(
            node_name="SMO",
            total=10.0,
            states={
                "recruited": 0.0,
            },
        )

        engine = TransitionEngine()

        with pytest.raises(
            KeyError,
            match="Transition source state not found: unrecruited",
        ):
            engine.apply_transition(
                node,
                runtime_state,
                {"A_SMO": 0.8},
            )
            
            
from internalnet.node_engine.engine import NodeEngine

def test_engine_runs_formulation_and_transition():
    repository = NodeRepository(
        [
            NodeDefinition(
                name="SMO",
                category="functional_protein",
                polymorphism=[
                    "unrecruited",
                    "recruited",
                ],
                formulation={
                    "type": "hill_inhibition",
                    "input": "PTCH1",
                    "state_mapping": {
                        "active": 1.0,
                        "inactive": 0.0,
                    },
                    "equation": (
                        "A_SMO = 1 / "
                        "(1 + (I_PTCH1 / K_PTCH1)^n)"
                    ),
                    "parameters": {
                        "K_PTCH1": 0.5,
                        "n": 2.0,
                        "theta_SMO": 0.5,
                    },
                    "transition": {
                        "from": "unrecruited",
                        "to": "recruited",
                        "condition": "A_SMO >= theta_SMO",
                    },
                },
            )
        ]
    )

    engine = NodeEngine(repository)

    node_input = NodeInput(
        node_name="SMO",
        total=10.0,
        states={
            "unrecruited": 10.0,
            "recruited": 0.0,
        },
        related_inputs={
            "PTCH1": {
                "states": {
                    "active": 0.0,
                    "inactive": 1.0,
                }
            }
        },
    )

    result = engine.run(node_input)

    assert result.source == "node_engine"
    assert result.node_name == "SMO"
    assert result.state_deltas["unrecruited"] == -10.0
    assert result.state_deltas["recruited"] == 10.0


def test_engine_without_transition_keeps_runtime_state():
    repository = NodeRepository(
        [
            NodeDefinition(
                name="ATP",
                category="resource",
            )
        ]
    )

    engine = NodeEngine(repository)

    node_input = NodeInput(
        node_name="ATP",
        total=20.0,
        states={},
    )

    result = engine.run(node_input)

    assert result.source == "node_engine"
    assert result.node_name == "ATP"
    assert result.total_delta == 0.0
    assert result.state_deltas == {}


def test_engine_does_not_mutate_input_states():
    repository = NodeRepository(
        [
            NodeDefinition(
                name="SMO",
                category="functional_protein",
                polymorphism=[
                    "unrecruited",
                    "recruited",
                ],
                formulation={
                    "type": "hill_inhibition",
                    "input": "PTCH1",
                    "state_mapping": {
                        "active": 1.0,
                        "inactive": 0.0,
                    },
                    "parameters": {
                        "K_PTCH1": 0.5,
                        "n": 2.0,
                        "theta_SMO": 0.5,
                    },
                    "transition": {
                        "from": "unrecruited",
                        "to": "recruited",
                        "condition": "A_SMO >= theta_SMO",
                    },
                },
            )
        ]
    )

    engine = NodeEngine(repository)

    node_input = NodeInput(
        node_name="SMO",
        total=10.0,
        states={
            "unrecruited": 10.0,
            "recruited": 0.0,
        },
        related_inputs={
            "PTCH1": {
                "states": {
                    "active": 0.0,
                    "inactive": 1.0,
                }
            }
        },
    )

    original_states = dict(node_input.states)

    engine.run(node_input)

    assert node_input.states == original_states
