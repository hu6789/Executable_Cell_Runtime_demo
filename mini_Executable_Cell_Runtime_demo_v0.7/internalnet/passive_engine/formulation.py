# internalnet/passive_engine/formulation.py

from __future__ import annotations

import math

from internalnet.node_engine.schema import (
    NodeDefinition,
    NodeRuntimeState,
)

from .schema import PassiveDefinition


class PassiveFormulationEngine:
    """Evaluate passive dynamics without mutating runtime state."""

    def evaluate(
        self,
        passive: PassiveDefinition,
        node: NodeDefinition,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> dict[str, float]:
        if dt < 0:
            raise ValueError("dt must be non-negative")

        if passive.name == "diffusion":
            return self._evaluate_diffusion(
                passive,
                node,
                runtime_state,
                dt,
            )

        if passive.name == "half_life_decay":
            return self._evaluate_half_life_decay(
                passive,
                node,
                runtime_state,
                dt,
            )
            
        if passive.name == "sufu_binding":
            return self._evaluate_sufu_binding(
                passive,
                node,
                runtime_state,
                dt,
            )

        raise ValueError(
            f"Unsupported passive formulation: {passive.name}"
        )

    @staticmethod
    def _evaluate_diffusion(
        passive: PassiveDefinition,
        node: NodeDefinition,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> dict[str, float]:
        if node.diffusion is None:
            raise ValueError(
                f"Node has no diffusion coefficient: {node.name}"
            )

        source_state = passive.update.get("source_state")
        target_state = passive.update.get("target_state")

        if source_state is None or target_state is None:
            raise ValueError(
                "Diffusion passive requires source_state "
                "and target_state"
            )

        source_value = runtime_state.states.get(
            source_state,
            0.0,
        )


        delta = min(
            node.diffusion * source_value * dt,
            source_value,
        )

        return {
            source_state: -delta,
            target_state: +delta,
        }

    @staticmethod
    def _evaluate_half_life_decay(
        passive: PassiveDefinition,
        node: NodeDefinition,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> dict[str, float]:
        if node.half_life is None:
            raise ValueError(
                f"Node has no half-life: {node.name}"
            )

        if node.half_life <= 0:
            raise ValueError(
                f"Node half-life must be positive: {node.name}"
            )

        if runtime_state.total <= 0:
            return {
                state: 0.0
                for state in runtime_state.states
            }

        mode = passive.update.get("mode")
        target = passive.update.get("target")

        if target != "all_states" or mode != "proportional_decay":
            raise ValueError(
                "Half-life decay requires target='all_states' "
                "and mode='proportional_decay'"
            )

        fraction = 1.0 - math.exp(
            -math.log(2.0) * dt / node.half_life
        )

        delta_total = runtime_state.total * fraction

        return {
            state: -delta_total * (
                value / runtime_state.total
            )
            for state, value in runtime_state.states.items()
        }
    
    @staticmethod
    def _evaluate_sufu_binding(
        passive: PassiveDefinition,
        node: NodeDefinition,
        runtime_state: NodeRuntimeState,
        dt: float,
    ) -> dict[str, float]:
        if dt < 0:
            raise ValueError(
                "dt must be non-negative"
            )

        source_state = passive.update.get("source_state")
        target_state = passive.update.get("target_state")

        if source_state is None or target_state is None:
            raise ValueError(
                "SUFU binding passive requires source_state "
                "and target_state"
            )

        k_bind = passive.formula.get(
            "parameters",
            {}
        ).get("k_bind")

        if k_bind is None:
            raise ValueError(
                "SUFU binding passive requires k_bind"
        )

        if k_bind < 0:
            raise ValueError(
                "k_bind must be non-negative"
            )

        source_value = runtime_state.states.get(
            source_state,
            0.0,
        )
        
        delta = min(
            k_bind * source_value * dt,
            source_value,
        )

        return {
            source_state: -delta,
            target_state: +delta,
        }
