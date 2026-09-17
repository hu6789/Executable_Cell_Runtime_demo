from typing import Dict, Optional

from internalnet.behavior_engine.input_resolver import BehaviorInputs
from internalnet.behavior_engine.schema import (
    BehaviorDefinition,
    BehaviorIntention,
)


class BehaviorFormulationEngine:
    """Calculate behavioral intention from resolved runtime inputs."""

    def evaluate(
        self,
        behavior: BehaviorDefinition,
        inputs: BehaviorInputs,
        parameters: Dict[str, float],
    ) -> Optional[BehaviorIntention]:
        if behavior.name == "production":
            return self._evaluate_production(
                behavior,
                inputs,
                parameters,
            )

        if behavior.name == "release":
            return self._evaluate_release(
                behavior,
                inputs,
                parameters,
            )

        raise ValueError(
            f"Unsupported behavior formulation: {behavior.name}"
        )

    def _evaluate_production(
        self,
        behavior: BehaviorDefinition,
        inputs: BehaviorInputs,
        parameters: Dict[str, float],
    ) -> Optional[BehaviorIntention]:
        if "production_rate" not in parameters:
            raise KeyError("Missing behavior parameter: production_rate")

        if not inputs.genes:
            return None

        # v = α × R
        # Current v0.7 convention:
        # GeneRuntimeState.value is the gene behavior signal R.
        gene_name, gene_state = next(iter(inputs.genes.items()))
        gene_behavior_signal = gene_state.value

        production_rate = parameters["production_rate"]
        value = production_rate * gene_behavior_signal

        return BehaviorIntention(
            behavior_name=behavior.name,
            value=value,
            inputs={
                "gene_behavior_signal": gene_behavior_signal,
            },
        )

    def _evaluate_release(
        self,
        behavior: BehaviorDefinition,
        inputs: BehaviorInputs,
        parameters: Dict[str, float],
    ) -> Optional[BehaviorIntention]:
        if "release_rate" not in parameters:
            raise KeyError("Missing behavior parameter: release_rate")

        if not inputs.nodes:
            return None

        # v = k_r × X_source
        # Current v0.7 convention:
        # NodeRuntimeState.total is the source amount X_source.
        node_name, node_state = next(iter(inputs.nodes.items()))
        source_node_total = node_state.total

        release_rate = parameters["release_rate"]
        value = release_rate * source_node_total

        return BehaviorIntention(
            behavior_name=behavior.name,
            value=value,
            inputs={
                "source_node.total": source_node_total,
            },
        )
