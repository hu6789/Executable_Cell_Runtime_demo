# internalnet/gene_engine/formulation.py

import math
from typing import Dict

from .schema import GeneDefinition
from internalnet.runtime.delta import GeneDelta
from internalnet.node_engine.schema import NodeRuntimeState


class GeneFormulationEngine:
    """
    Calculates Node -> Gene regulation.

    This engine does not:
    - resolve TF -> Element relationships
    - combine multiple TFs
    - tune behaviors
    - access Graph
    - access World
    """

    def evaluate(
        self,
        gene,
        gene_state,
        node_states,
    ) -> GeneDelta:

        formula = gene.formula

        if not formula:
            return GeneDelta(
                source="gene_engine",
                gene_name=gene_state.name,
            )


        output = formula.get("output")

        if output == "lysine_modification":

            modification_value = (
                self._evaluate_hill_activation(
                    formula,
                    node_states,
                )
            )

            return GeneDelta(
                source="gene_engine",
                gene_name=gene_state.name,
                value_delta=(
                    modification_value
                    -
                    gene_state.value
                ),
                modification_deltas={
                    "lysine_modified":
                        (
                            modification_value
                            -
                            gene_state.modifications.get(
                                "lysine_modified",
                                0.0,
                            )
                        )
                },
            )

        if output == "value":

            value = (
                self._evaluate_value_activation(
                    formula,
                    node_states,
                )
            )

            return GeneDelta(
                source="gene_engine",
                gene_name=gene_state.name,
                value_delta=(
                    value
                    -
                    gene_state.value
                ),
            )

        raise ValueError(
            f"Unsupported gene formula output: {output}"
        )

    def _evaluate_hill_activation(
        self,
        formula: dict,
        node_states: Dict[str, NodeRuntimeState],
    ) -> float:
        parameters = formula.get("parameters", {})

        input_ref = parameters.get("H_nuclear")

        if not input_ref:
            raise ValueError(
                "Gene input reference H_nuclear is not configured"
            )

        parts = input_ref.split(".")

        if len(parts) != 3 or parts[1] != "states":
            raise ValueError(
                f"Unsupported gene input reference: {input_ref}"
            )

        node_name = parts[0]
        state_name = parts[2]

        node_state = node_states.get(node_name)

        if node_state is None:
            raise KeyError(
                f"Missing NodeRuntimeState: {node_name}"
            )

        h_nuclear = node_state.states.get(
            state_name,
            0.0,
        )

        k_h = float(parameters.get("K_H", 0.5))
        n = float(parameters.get("n", 2.0))

        if k_h <= 0:
            raise ValueError("K_H must be greater than 0")

        if n <= 0:
            raise ValueError("n must be greater than 0")

        numerator = h_nuclear ** n
        denominator = k_h ** n + numerator

        if denominator == 0:
            return 0.0

        return numerator / denominator
        
        
    def _evaluate_value_activation(
        self,
        formula: dict,
        node_states: Dict[str, NodeRuntimeState],
    ) -> float:

        parameters = formula.get("parameters", {})

        input_ref = parameters.get("RAR_nuclear")

        if not input_ref:
            raise ValueError(
                "Gene input reference RAR_nuclear is not configured"
            )

        parts = input_ref.split(".")

        if len(parts) != 3 or parts[1] != "states":
            raise ValueError(
                f"Unsupported gene input reference: {input_ref}"
            )

        node_name = parts[0]
        state_name = parts[2]

        node_state = node_states.get(node_name)

        if node_state is None:
            raise KeyError(
                f"Missing NodeRuntimeState: {node_name}"
            )

        rar_nuclear = node_state.states.get(
            state_name,
            0.0,
        )

        r_max = float(parameters.get("R_max", 1.0))
        k_rar = float(parameters.get("K_RAR", 0.5))
        n = float(parameters.get("n", 2.0))

        if k_rar <= 0:
            raise ValueError("K_RAR must be greater than 0")

        if n <= 0:
            raise ValueError("n must be greater than 0")

        numerator = rar_nuclear ** n
        denominator = k_rar ** n + numerator

        if denominator == 0:
            return 0.0

        return r_max * numerator / denominator
