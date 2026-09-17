import pytest

from internalnet.gene_engine.schema import (
    GeneDefinition,
)


from internalnet.runtime.delta import (
    GeneDelta,
)

from internalnet.runtime.state import (
    GeneState,
    NodeState,
)

from internalnet.runtime.delta import (
    GeneDelta,
)


    
from internalnet.gene_engine.repository import GeneRepository

def test_gene_repository_register_and_get():
    repository = GeneRepository()

    gene = GeneDefinition(name="FOXA2")

    repository.register(gene)

    assert repository.has("FOXA2")
    assert repository.get("FOXA2") == gene


def test_gene_repository_unknown_gene_raises():
    repository = GeneRepository()

    with pytest.raises(KeyError, match="Unknown gene: FOXA2"):
        repository.get("FOXA2")


def test_gene_repository_duplicate_registration_raises():
    repository = GeneRepository()

    repository.register(
        GeneDefinition(name="FOXA2")
    )

    with pytest.raises(
        ValueError,
        match="Gene already registered: FOXA2",
    ):
        repository.register(
            GeneDefinition(name="FOXA2")
        )


def test_gene_repository_names():
    repository = GeneRepository(
        [
            GeneDefinition(name="FOXA2"),
            GeneDefinition(name="SHH"),
        ]
    )

    assert repository.names() == (
        "FOXA2",
        "SHH",
    )


def test_gene_repository_initial_genes():
    foxa2 = GeneDefinition(name="FOXA2")
    shh = GeneDefinition(name="SHH")

    repository = GeneRepository(
        [
            foxa2,
            shh,
        ]
    )

    assert repository.get("FOXA2") == foxa2
    assert repository.get("SHH") == shh
    
from internalnet.gene_engine.formulation import GeneFormulationEngine
from internalnet.node_engine.schema import NodeRuntimeState

def test_gene_formulation_hill_activation():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "equation": "R = H_nuclear^n / (K_H^n + H_nuclear^n)",
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.0,
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=0.5,
            states={
                "nuclear":0.5,
            },
        )
    }

    engine = GeneFormulationEngine()

    result = engine.evaluate(
        gene,
        gene_state,
        node_states,
    )

    assert result.source == "gene_engine"
    assert result.gene_name == "FOXA2"
    assert result.value_delta == pytest.approx(0.5)
    assert result.modification_deltas == {
        "lysine_modified": pytest.approx(0.5),
    }


def test_gene_formulation_uses_new_node_state():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "equation": "R = H_nuclear^n / (K_H^n + H_nuclear^n)",
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.2,
        modifications={
            "lysine_modified": 0.2,
        },
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=1.0,
            states={
                "nuclear": 1.0,
            },
        )
    }

    engine = GeneFormulationEngine()

    result = engine.evaluate(
        gene,
        gene_state,
        node_states,
    )

    expected = 1.0 ** 2 / (0.5 ** 2 + 1.0 ** 2)

    assert result.value_delta == pytest.approx(
        expected - gene_state.value
    )
    assert result.modification_deltas == {
        "lysine_modified": pytest.approx(0.8 - 0.2),
    }


def test_gene_formulation_does_not_accumulate_modification():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.8,
        modifications={
            "lysine_modified": 0.8,
        },
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=0.0,
            states={
                "nuclear": 0.0,
            },
        )
    }

    engine = GeneFormulationEngine()

    result = engine.evaluate(
        gene,
        gene_state,
        node_states,
    )

    assert result.value_delta == pytest.approx(
        0.0 - 0.8
    )
    assert result.modification_deltas == {
        "lysine_modified": pytest.approx(-0.8)
    }


def test_gene_formulation_without_formula_returns_empty_delta():

    gene = GeneDefinition(
        name="SHH"
    )

    gene_state = GeneState(
        name="SHH",
        baseline=1.0,
        value=0.7,
    )

    engine = GeneFormulationEngine()

    result = engine.evaluate(
        gene,
        gene_state,
        {},
    )

    assert result.source == "gene_engine"
    assert result.gene_name == "SHH"
    assert result.value_delta == 0.0
    assert result.modification_deltas == {}

def test_gene_formulation_missing_required_node_raises():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.0,
    )

    engine = GeneFormulationEngine()

    with pytest.raises(
        KeyError,
        match="Missing NodeRuntimeState: H3K27ac",
    ):
        engine.evaluate(
            gene,
            gene_state,
            {},
        )


def test_gene_formulation_does_not_mutate_input_state():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.2,
        modifications={
            "lysine_modified": 0.2,
        },
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=0.5,
            states={
                "nuclear": 0.5,
            },
        )
    }

    original_value = gene_state.value
    original_modifications = dict(gene_state.modifications)

    engine = GeneFormulationEngine()

    engine.evaluate(
        gene,
        gene_state,
        node_states,
    )


    assert gene_state.value == original_value
    assert gene_state.modifications == original_modifications
    
    
from internalnet.gene_engine.engine import GeneEngine

def test_gene_engine_run():
    gene = GeneDefinition(
        name="FOXA2",
        formula={
            "parameters": {
                "H_nuclear": "H3K27ac.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    repository = GeneRepository([gene])
    engine = GeneEngine(repository)

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=0.0,
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=0.5,
            states={
                "nuclear": 0.5,
            },
        )
    }

    result = engine.run(
        gene_name="FOXA2",
        gene_state=gene_state,
        node_states=node_states,
    )

    assert result.source=="gene_engine"
    assert result.gene_name=="FOXA2"
    assert result.value_delta==pytest.approx(0.5)
    assert result.modification_deltas == {
        "lysine_modified": pytest.approx(0.5)
    }


def test_gene_engine_delegates_to_formulation():
    class FakeFormulation:
        def __init__(self):
            self.called = False

        def evaluate(
            self,
            gene,
            gene_state,
            node_states,
        ):
            self.called = True

            assert gene.name=="FOXA2"
            assert gene_state.name=="FOXA2"
            assert "H3K27ac" in node_states

            return GeneDelta(
                source="gene_engine",
                gene_name="FOXA2",
                value_delta=0.42,
                modification_deltas={
                    "lysine_modified":0.42,
                }
            )

    gene = GeneDefinition(name="FOXA2")
    repository = GeneRepository([gene])
    formulation = FakeFormulation()

    engine = GeneEngine(
        repository=repository,
        formulation=formulation,
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=1.0,
    )

    node_states = {
        "H3K27ac": NodeState(
            name="H3K27ac",
            total=0.5,
            states={
                "nuclear": 0.5,
            },
        )
    }

    result = engine.run(
        gene_name="FOXA2",
        gene_state=gene_state,
        node_states=node_states,
    )

    assert formulation.called
    assert result.value_delta == pytest.approx(0.42)


def test_gene_engine_unknown_gene_raises():
    repository = GeneRepository()
    engine = GeneEngine(repository)

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=1.0,
    )

    with pytest.raises(
        KeyError,
        match="Unknown gene: FOXA2",
    ):
        engine.run(
            gene_name="FOXA2",
            gene_state=gene_state,
            node_states={},
        )


def test_gene_engine_repository_helpers():
    repository = GeneRepository(
        [
            GeneDefinition(name="FOXA2"),
            GeneDefinition(name="SHH"),
        ]
    )

    engine = GeneEngine(repository)

    assert engine.has("FOXA2")
    assert engine.has("SHH")
    assert not engine.has("GLI2")

    assert engine.get("FOXA2").name == "FOXA2"

    assert engine.names() == (
        "FOXA2",
        "SHH",
    )
    
def test_gene_formulation_resolves_node_from_input_reference():
    gene = GeneDefinition(
        name="TEST_GENE",
        formula={
            "parameters": {
                "H_nuclear": "OTHER_NODE.states.nuclear",
                "K_H": 0.5,
                "n": 2,
            },
            "output": "lysine_modification",
        },
    )

    gene_state = GeneState(
        name="TEST_GENE",
        baseline=1.0,
        value=0.0,
    )

    node_states = {
        "OTHER_NODE": NodeState(
            name="OTHER_NODE",
            total=0.5,
            states={
                "nuclear": 0.5,
            },
        )
    }

    engine = GeneFormulationEngine()

    result = engine.evaluate(
        gene,
        gene_state,
        node_states,
    )

    assert result.value_delta == pytest.approx(0.5)
    assert result.modification_deltas == {
        "lysine_modified": pytest.approx(0.5),
    }
