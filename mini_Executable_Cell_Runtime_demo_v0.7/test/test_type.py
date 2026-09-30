from pathlib import Path

from internalnet.hir.type.determination import (
    TypeDetermination,
)
from internalnet.runtime.state import NodeState
from internalnet.hir.type.selection import TypeSelection

from internalnet.hir.type.repository import (
    LineageRepository,
    TypeEvidenceRepository,
    TypeTransitionRepository,
)

from internalnet.hir.type.transition import (
    TypeTransition,
)

LIBRARY = Path("internalnet/hir/library")


def _node(name, states=None):
    return NodeState(
        name=name,
        total=1.0,
        states=states or {},
    )

def test_type_determination_returns_complete_identity():
    repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    evidence = repository.find_by_type(
        "neural_progenitor"
    )

    result = determination.determine(
        evidence_list=[evidence],
        node_states={
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR", {"nuclear": 0.8}),
            "PAX6": _node("PAX6", {"free": 0.7}),
        },
    )

    assert len(result) == 1

    status = result[0]

    assert status.type_name == "neural_progenitor"
    assert status.upstream_complete is True
    assert status.regulatory_complete is True
    assert status.output_complete is True
    assert status.complete is True
    assert status.matched_count == 3
    assert status.total_count == 3
    assert status.evidence == "complete"


def test_type_determination_returns_partial_identity():
    repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    evidence = repository.find_by_type(
        "neural_progenitor"
    )

    result = determination.determine(
        evidence_list=[evidence],
        node_states={
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR"),
        },
    )

    status = result[0]

    assert status.complete is False
    assert status.matched_count == 1
    assert status.total_count == 3
    assert status.evidence == "partial"


def test_type_determination_returns_none_for_no_identity_evidence():
    repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    evidence = repository.find_by_type(
        "neural_progenitor"
    )

    result = determination.determine(
        evidence_list=[evidence],
        node_states={},
    )

    status = result[0]

    assert status.complete is False
    assert status.matched_count == 0
    assert status.total_count == 3
    assert status.evidence == "none"


def test_type_determination_evaluates_multiple_types():
    repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    results = determination.determine(
        evidence_list=repository.all(),
        node_states={
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR", {"nuclear": 0.8}),
            "PAX6": _node("PAX6", {"free": 0.7}),
            "SHH": _node("SHH", {"free": 0.5}),
        },
    )

    statuses = {
        status.type_name: status
        for status in results
    }

    assert statuses[
        "neural_progenitor"
    ].evidence == "complete"

    assert statuses[
        "floor_plate_progenitor"
    ].evidence == "partial"

    assert statuses[
        "motor_neuron_progenitor"
    ].evidence == "none"
    
    
def test_lineage_repository_loads_lineage():
    repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    nodes = repository.all()

    assert len(nodes) == 3

    neural = repository.find_by_type(
        "neural_progenitor"
    )

    assert neural.parent is None
    assert neural.children == [
        "floor_plate_progenitor",
        "motor_neuron_progenitor",
    ]


def test_lineage_repository_resolves_descendant_relation():
    repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    assert repository.relation(
        "neural_progenitor",
        "floor_plate_progenitor",
    ) == "descendant"


def test_lineage_repository_resolves_ancestor_relation():
    repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    assert repository.relation(
        "floor_plate_progenitor",
        "neural_progenitor",
    ) == "ancestor"


def test_lineage_repository_returns_none_for_unrelated_types():
    repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    assert repository.relation(
        "floor_plate_progenitor",
        "motor_neuron_progenitor",
    ) is None
    
def test_type_transition_marks_complete_identity_as_primary():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR", {"nuclear": 0.8}),
            "PAX6": _node("PAX6", {"free": 0.7}),
        },
    )

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert result["neural_progenitor"] == "primary_type"

def test_type_transition_marks_partial_descendant_as_tendency():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            "SHH": _node("SHH", {"free": 0.5}),
        },
    )

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert result["floor_plate_progenitor"] == "tendency"
    
    
def test_type_transition_marks_partial_ancestor_as_legacy():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            "RA": _node("RA", {"free": 1.0}),
        },
    )

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="motor_neuron_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert result["neural_progenitor"] == "legacy"
    
    
def test_type_transition_does_not_classify_unrelated_partial_identity():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            "SHH": _node("SHH"),
        },
    )

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="motor_neuron_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert "floor_plate_progenitor" not in result
    
    
def test_type_transition_current_neural_floor_complete_is_primary():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),
        },
    )

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert result["floor_plate_progenitor"] == "primary_type"
    
    
def test_type_transition_with_multiple_complete_identities():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    lineage_repository = LineageRepository(
        LIBRARY / "lineage.json"
    )

    transition_repository = TypeTransitionRepository(
        LIBRARY / "type_transition.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            # neural_progenitor
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR", {"nuclear": 0.8}),
            "PAX6": _node("PAX6", {"free": 0.7}),

            # floor_plate_progenitor
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),
        },
    )

    statuses_by_type = {
        status.type_name: status
        for status in statuses
    }

    assert statuses_by_type[
        "neural_progenitor"
    ].evidence == "complete"

    assert statuses_by_type[
        "floor_plate_progenitor"
    ].evidence == "complete"

    transition = TypeTransition(
        lineage_repository=lineage_repository,
        transition_repository=transition_repository,
    )

    results = transition.resolve(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    result = {
        item.type_name: item.state
        for item in results
    }

    assert result["neural_progenitor"] == "primary_type"
    assert result["floor_plate_progenitor"] == "primary_type"
    
    
def test_type_selection_keeps_current_type_when_current_identity_is_complete():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            # neural_progenitor
            "RA": _node("RA", {"free": 1.0}),
            "RAR": _node("RAR", {"nuclear": 0.8}),
            "PAX6": _node("PAX6", {"free": 0.7}),

            # floor_plate_progenitor
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),
        },
    )

    selection = TypeSelection(
        lineage_repository=LineageRepository(
            LIBRARY / "lineage.json"
        )
    )

    result = selection.select(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    assert result == "neural_progenitor"


def test_type_selection_switches_to_complete_descendant():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            # neural_progenitor: partial
            "RA": _node("RA", {"free": 1.0}),

            # floor_plate_progenitor: complete
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),
        },
    )

    selection = TypeSelection(
        lineage_repository=LineageRepository(
            LIBRARY / "lineage.json"
        )
    )

    result = selection.select(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    assert result == "floor_plate_progenitor"
    
    
def test_type_selection_does_not_choose_between_multiple_complete_descendants():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            # Current type: neural_progenitor is only partial.
            "RA": _node("RA", {"free": 1.0}),

            # floor_plate_progenitor: complete.
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),

            # motor_neuron_progenitor: complete.
            "GLI3": _node("GLI3", {"repressor": 0.3}),
            "NKX6.1": _node("NKX6.1", {"free": 0.3}),
            "OLIG2": _node("OLIG2", {"free": 0.3}),
            "NEUROG2": _node("NEUROG2", {"free": 0.2}),
            "TUBB3": _node("TUBB3", {"free": 0.2}),
        },
    )

    statuses_by_type = {
        status.type_name: status
        for status in statuses
    }

    assert statuses_by_type[
        "neural_progenitor"
    ].evidence == "partial"

    assert statuses_by_type[
        "floor_plate_progenitor"
    ].evidence == "complete"

    assert statuses_by_type[
        "motor_neuron_progenitor"
    ].evidence == "complete"

    selection = TypeSelection(
        lineage_repository=LineageRepository(
            LIBRARY / "lineage.json"
        )
    )

    result = selection.select(
        current_type="neural_progenitor",
        statuses=statuses,
    )

    assert result == "neural_progenitor"
    
    
def test_type_selection_does_not_switch_to_unrelated_complete_type():
    evidence_repository = TypeEvidenceRepository(
        LIBRARY / "type_evidence.json"
    )

    determination = TypeDetermination()

    statuses = determination.determine(
        evidence_list=evidence_repository.all(),
        node_states={
            # Current type: motor_neuron_progenitor is partial.
            "GLI3": _node("GLI3", {"repressor": 0.3}),

            # floor_plate_progenitor: complete.
            "SHH": _node("SHH", {"free": 0.5}),
            "H3K27ac": _node("H3K27ac", {"nuclear": 0.5}),
            "CORIN": _node("CORIN", {"free": 0.3}),
        },
    )

    statuses_by_type = {
        status.type_name: status
        for status in statuses
    }

    assert statuses_by_type[
        "motor_neuron_progenitor"
    ].evidence == "partial"

    assert statuses_by_type[
        "floor_plate_progenitor"
    ].evidence == "complete"

    selection = TypeSelection(
        lineage_repository=LineageRepository(
            LIBRARY / "lineage.json"
        )
    )

    result = selection.select(
        current_type="motor_neuron_progenitor",
        statuses=statuses,
    )

    assert result == "motor_neuron_progenitor"
