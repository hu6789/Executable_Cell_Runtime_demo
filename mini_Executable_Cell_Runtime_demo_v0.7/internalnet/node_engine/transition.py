# internalnet/node_engine/transition.py

from __future__ import annotations

from typing import Any, Dict

from .schema import NodeDefinition, NodeRuntimeState


class TransitionEngine:
    """Evaluate and apply node state transitions.

    Transitions are declared by NodeDefinition.formulation.transition.

    The engine evaluates the declared condition and, when the
    condition is satisfied, redistributes quantity between
    polymorphic states while preserving total quantity.
    """

    def evaluate_condition(
        self,
        node: NodeDefinition,
        computed_values: Dict[str, float],
    ) -> bool:
        """Evaluate the transition condition of a node."""

        formulation = node.formulation

        if formulation is None:
            return False

        transition = formulation.get("transition")

        if transition is None:
            return False

        condition = transition.get("condition")

        if condition is None:
            return False

        return self._evaluate_condition(
            condition=condition,
            computed_values=computed_values,
            parameters=formulation.get(
                "parameters",
                {},
            ),
        )

    def apply_transition(
        self,
        node: NodeDefinition,
        runtime_state: NodeRuntimeState,
        computed_values: Dict[str, float],
    ) -> NodeRuntimeState:
        """Apply a state transition if its condition is satisfied."""

        formulation = node.formulation

        if formulation is None:
            return runtime_state

        transition = formulation.get("transition")

        if transition is None:
            return runtime_state

        if not self.evaluate_condition(
            node,
            computed_values,
        ):
            return runtime_state

        from_state = transition["from"]
        to_state = transition["to"]

        states = dict(runtime_state.states)

        if from_state not in states:
            raise KeyError(
                f"Transition source state not found: {from_state}"
            )

        if to_state not in states:
            raise KeyError(
                f"Transition target state not found: {to_state}"
            )

        quantity = states[from_state]

        states[from_state] = 0.0
        states[to_state] += quantity

        return NodeRuntimeState(
            node_name=runtime_state.node_name,
            total=runtime_state.total,
            states=states,
        )

    def _evaluate_condition(
        self,
        condition: str,
        computed_values: Dict[str, float],
        parameters: Dict[str, Any],
    ) -> bool:
        """Evaluate a simple v0.7 comparison condition."""

        parts = condition.split()

        if len(parts) != 3:
            raise ValueError(
                f"Unsupported transition condition: {condition}"
            )

        value_name, operator, threshold_name = parts

        if value_name not in computed_values:
            raise KeyError(
                f"Computed value not found: {value_name}"
            )

        if threshold_name not in parameters:
            raise KeyError(
                f"Transition parameter not found: {threshold_name}"
            )

        value = computed_values[value_name]
        threshold = parameters[threshold_name]

        if operator == ">=":
            return value >= threshold

        if operator == ">":
            return value > threshold

        if operator == "<=":
            return value <= threshold

        if operator == "<":
            return value < threshold

        if operator == "==":
            return value == threshold

        raise ValueError(
            f"Unsupported transition operator: {operator}"
        )
