# internalnet/node_engine/formulation.py

from __future__ import annotations

from typing import Any, Dict

from .schema import NodeDefinition, NodeInput


class FormulationEngine:
    """Execute node formulations declared in NodeDefinition.

    The formulation engine performs mathematical calculations only.
    It does not perform state transitions or mutate runtime state.
    """

    def evaluate(
        self,
        node: NodeDefinition,
        node_input: NodeInput,
    ) -> Dict[str, float]:
        """Evaluate the formulation of a node.

        Returns a mapping from the formulation output name
        to its computed value.
        """
        formulation = node.formulation

        if formulation is None:
            return {}

        formulation_type = formulation.get("type")

        if formulation_type == "hill_inhibition":
            return self._evaluate_hill_inhibition(
                formulation,
                node_input,
            )

        if formulation_type == "SMO_dependent_dissociation":
            return self._evaluate_smo_dependent_dissociation(
                formulation,
                node_input,
            )

        raise ValueError(
            f"Unsupported formulation type: {formulation_type}"
        )

    def _evaluate_hill_inhibition(
        self,
        formulation: Dict[str, Any],
        node_input: NodeInput,
    ) -> Dict[str, float]:

        input_name = formulation["input"]

        related = node_input.related_inputs.get(input_name)

        if related is None:
            raise KeyError(
                f"Related input not found: {input_name}"
            )

        states = related.get("states", {})

        state_mapping = formulation.get(
            "state_mapping",
            {},
        )

        input_value = sum(
            states.get(state, 0.0) * weight
            for state, weight in state_mapping.items()
        )

        parameters = formulation["parameters"]

        k = parameters["K_PTCH1"]
        n = parameters["n"]

        if k <= 0:
            raise ValueError(
                "K_PTCH1 must be greater than zero"
            )

        activity = 1.0 / (
            1.0 + (input_value / k) ** n
        )

        return {
            "A_SMO": activity,
        }

    def _evaluate_smo_dependent_dissociation(
        self,
        formulation: Dict[str, Any],
        node_input: NodeInput,
    ) -> Dict[str, float]:

        input_name = formulation["input"]

        related = node_input.related_inputs.get(input_name)

        if related is None:
            raise KeyError(
                f"Related input not found: {input_name}"
            )

        states = related.get("states", {})

        # For the current v0.7 mini-demo,
        # the SMO activation state is represented
        # by the "recruited" quantity.
        smo_activity = states.get(
            "recruited",
            0.0,
        )

        parameters = formulation["parameters"]

        k_diss = parameters["k_diss"]
        k_smo = parameters["K_SMO"]
        n = parameters["n"]

        if k_diss is None:
            raise ValueError(
                "k_diss is not configured"
            )

        if k_smo is None:
            raise ValueError(
                "K_SMO is not configured"
            )

        if k_smo <= 0:
            raise ValueError(
                "K_SMO must be greater than zero"
            )

        dissociation = (
            k_diss
            * smo_activity ** n
            / (
                k_smo ** n
                + smo_activity ** n
            )
        )

        return {
            "D_GLI": dissociation,
        }
