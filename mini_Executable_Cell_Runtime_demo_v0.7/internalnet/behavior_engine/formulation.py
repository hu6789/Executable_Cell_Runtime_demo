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
            
        if behavior.name == "GLI3_truncation":
            return self._evaluate_gli3_truncation(
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
        # NodeRuntimeState.states["free"] is the source amount X_source.
        node_name, node_state = next(iter(inputs.nodes.items()))
        source_node_free = node_state.states.get("free", 0.0)

        release_rate = parameters["release_rate"]
        value = release_rate * source_node_free

        return BehaviorIntention(
            behavior_name=behavior.name,
            value=value,
            inputs={
                "source_node.free": source_node_free,
            },
        )
        
    def _evaluate_gli3_truncation(
        self,
        behavior: BehaviorDefinition,
        inputs: BehaviorInputs,
        parameters: Dict[str, float],
    ) -> Optional[BehaviorIntention]:

        if "truncation_rate" not in parameters:
            raise KeyError(
                "Missing behavior parameter: truncation_rate"
            )

        if "truncation_Km" not in parameters:
            raise KeyError(
                "Missing behavior parameter: truncation_Km"
            )
 
        if "GLI3" not in inputs.nodes:
            return None

        gli3 = inputs.nodes["GLI3"]
        x_free = gli3.states.get("free", 0.0)

        vmax = parameters["truncation_rate"]
        km = parameters["truncation_Km"]

        value = (
            vmax * x_free / (km + x_free)
            if x_free > 0.0
            else 0.0
        )

        return BehaviorIntention(
            behavior_name=behavior.name,
            value=value,
            inputs={
                "GLI3.free": x_free,
            },
        )
