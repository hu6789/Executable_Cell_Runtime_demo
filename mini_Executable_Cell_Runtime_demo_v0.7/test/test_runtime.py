import pytest

from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import NodeState, GeneState


def test_runtime_stores_cell_identity_and_type():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    assert runtime.id == "cell_001"
    assert runtime.type == "neural_progenitor"


def test_runtime_stores_node_runtime_states():
    node_state = NodeState(
        name="PTCH1",
        total=10.0,
        states={
            "active": 5.0,
            "inactive": 5.0,
        },
    )

    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
        node_states={
            "PTCH1": node_state,
        },
    )

    assert runtime.has_node("PTCH1")
    assert runtime.get_node("PTCH1") == node_state
    assert runtime.get_node("PTCH1").total == 10.0


def test_runtime_stores_gene_runtime_states():
    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=1.2,
        modifications={},
    )

    runtime = Runtime(
        id="cell_001",
        type="floor_plate_progenitor",
        gene_states={
            "FOXA2": gene_state,
        },
    )

    assert runtime.has_gene("FOXA2")
    assert runtime.get_gene("FOXA2") == gene_state
    assert runtime.get_gene("FOXA2").value == 1.2


def test_runtime_can_store_node_and_gene_together():
    node_state = NodeState(
        name="SHH",
        total=2.0,
        states={},
    )

    gene_state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=1.5,
        modifications={},
    )

    runtime = Runtime(
        id="cell_001",
        type="floor_plate_progenitor",
        node_states={
            "SHH": node_state,
        },
        gene_states={
            "FOXA2": gene_state,
        },
    )

    assert runtime.get_node("SHH").total == 2.0
    assert runtime.get_gene("FOXA2").value == 1.5


def test_runtime_reports_missing_node():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    assert not runtime.has_node("PTCH1")

    with pytest.raises(KeyError):
        runtime.get_node("PTCH1")


def test_runtime_reports_missing_gene():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    assert not runtime.has_gene("FOXA2")

    with pytest.raises(KeyError):
        runtime.get_gene("FOXA2")


def test_runtime_can_update_node_state():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    state = NodeState(
        name="PTCH1",
        total=10.0,
        states={
            "active": 3.0,
            "inactive": 7.0,
        },
    )

    runtime.set_node(state)

    assert runtime.get_node("PTCH1") == state


def test_runtime_can_update_gene_state():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    state = GeneState(
        name="FOXA2",
        baseline=1.0,
        value=1.2,
        modifications={},
    )

    runtime.set_gene(state)

    assert runtime.get_gene("FOXA2") == state


def test_runtime_does_not_define_process_values():
    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
    )

    assert not hasattr(runtime, "passive")
    assert not hasattr(runtime, "behavior")
    assert not hasattr(runtime, "delta")
    
    
    
from internalnet.runtime.delta import (
    NodeDelta,
    PassiveDelta,
    GeneDelta,
    BehaviorInternalDelta,
)


def test_node_delta_contains_source_engine():
    delta = NodeDelta(
        source="node_engine",
        node_name="PTCH1",
        total_delta=2.0,
        state_deltas={
            "active": 1.0,
        },
    )

    assert delta.source == "node_engine"
    assert delta.node_name == "PTCH1"
    assert delta.total_delta == 2.0


def test_passive_delta_contains_source_engine():
    delta = PassiveDelta(
        source="passive_engine",
        passive_name="diffusion",
        node_name="SHH",
        total_delta=-0.5,
    )

    assert delta.source == "passive_engine"
    assert delta.passive_name == "diffusion"
    assert delta.node_name == "SHH"

def test_gene_delta_contains_source_engine():
    delta = GeneDelta(
        source="gene_engine",
        gene_name="FOXA2",
        value_delta=1.2,
        modification_deltas={
            "H3K27ac": 1.0,
        },
    )

    assert delta.source == "gene_engine"
    assert delta.gene_name == "FOXA2"
    assert delta.value_delta == 1.2


def test_behavior_internal_delta_contains_source_engine():
    node_delta = NodeDelta(
        source="behavior_engine",
        node_name="ATP",
        total_delta=-2.0,
    )

    gene_delta = GeneDelta(
        source="behavior_engine",
        gene_name="FOXA2",
        value_delta=0.5,
    )

    delta = BehaviorInternalDelta(
        source="behavior_engine",
        behavior_name="some_behavior",
        node_deltas={
            "ATP": node_delta,
        },
        gene_deltas={
            "FOXA2": gene_delta,
        },
    )

    assert delta.source == "behavior_engine"
    assert delta.behavior_name == "some_behavior"

    assert (
        delta.node_deltas["ATP"].source
        == "behavior_engine"
    )

    assert (
        delta.gene_deltas["FOXA2"].source
        == "behavior_engine"
    )


def test_behavior_internal_delta_has_no_external_output():
    delta = BehaviorInternalDelta(
        source="behavior_engine",
        behavior_name="some_behavior",
    )

    assert not hasattr(delta, "external_effects")
    assert not hasattr(delta, "labels")
    assert not hasattr(delta, "type_name")
    
    
from internalnet.runtime.schema import Runtime
from internalnet.runtime.state import (
    NodeState,
    GeneState,
)
from internalnet.runtime.delta import (
    NodeDelta,
    GeneDelta,
)

from internalnet.runtime.merger import RuntimeMerger


def test_merge_node_delta():

    runtime = Runtime(
        id="cell_001",
        type="neural_progenitor",
        node_states={
            "PTCH1": NodeState(
                name="PTCH1",
                total=10,
                states={
                    "active":5
                }
            )
        }
    )


    delta = NodeDelta(
        source="node_engine",
        node_name="PTCH1",
        total_delta=2,
        state_deltas={
            "active":1
        }
    )


    result = RuntimeMerger().merge_node(
        runtime,
        delta,
    )


    assert result.get_node(
        "PTCH1"
    ).total == 12


    assert result.get_node(
        "PTCH1"
    ).states["active"] == 6



def test_merge_gene_delta():

    runtime = Runtime(
        id="cell_001",
        type="floor_plate_progenitor",
        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=1,
                value=1.5,
                modifications={}
            )
        }
    )


    delta = GeneDelta(
        source="gene_engine",
        gene_name="FOXA2",
        value_delta=0.5
    )


    result = RuntimeMerger().merge_gene(
        runtime,
        delta,
    )


    assert result.get_gene(
        "FOXA2"
    ).value == 2.0
    
from internalnet.runtime.delta import PassiveDelta


def test_merge_passive_delta():

    runtime = Runtime(
        id="cell_001",
        type="floor_plate_progenitor",
        node_states={
            "FOXA2": NodeState(
                name="FOXA2",
                total=10,
                states={
                    "free":6,
                    "nuclear":4,
                }
            )
        }
    )


    delta = PassiveDelta(
        source="passive_engine",
        passive_name="diffusion",
        node_name="FOXA2",
        state_deltas={
            "free":-3,
            "nuclear":3,
        }
    )


    result = RuntimeMerger().merge_passive(
        runtime,
        delta,
    )


    assert result.get_node(
        "FOXA2"
    ).total == 10


    assert result.get_node(
        "FOXA2"
    ).states == {
        "free":3,
        "nuclear":7,
    }
    
    
from internalnet.runtime.delta import BehaviorInternalDelta


def test_merge_behavior_internal_delta():

    runtime = Runtime(
        id="cell_001",
        type="floor_plate_progenitor",

        node_states={
            "ATP": NodeState(
                name="ATP",
                total=10,
                states={
                    "available":10,
                }
            )
        },

        gene_states={
            "FOXA2": GeneState(
                name="FOXA2",
                baseline=1,
                value=1.0,
                modifications={}
            )
        }
    )


    behavior_delta = BehaviorInternalDelta(
        source="behavior_engine",
        behavior_name="energy_consumption",

        node_deltas={
            "ATP": NodeDelta(
                source="behavior_engine",
                node_name="ATP",
                total_delta=-2,
                state_deltas={
                    "available":-2,
                }
            )
        },

        gene_deltas={
            "FOXA2": GeneDelta(
                source="behavior_engine",
                gene_name="FOXA2",
                value_delta=0.5,
            )
        }
    )


    result = RuntimeMerger().merge_behavior_internal(
        runtime,
        behavior_delta,
    )


    assert result.get_node(
        "ATP"
    ).total == 8


    assert result.get_node(
        "ATP"
    ).states["available"] == 8


    assert result.get_gene(
        "FOXA2"
    ).value == 1.5
