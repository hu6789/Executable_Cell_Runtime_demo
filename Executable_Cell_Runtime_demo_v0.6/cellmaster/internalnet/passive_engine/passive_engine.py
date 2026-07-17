# cellmaster/internalnet/passive_engine/passive_engine.py


from cellmaster.internalnet.passive_engine.passive_gate import (
    evaluate_passive_gate
)

from cellmaster.internalnet.passive_engine.passive_formula import (
    compute_passive_formula
)

from cellmaster.internalnet.passive_engine.passive_transform import (
    apply_passive_transform
)

from cellmaster.internalnet.passive_engine.passive_runtime_result import (
    build_passive_runtime_result,
    build_passive_runtime_metadata
)


class PassiveEngine:

    def process_all_passives(self,
        runtime_entity,
        runtime_context,
        passive_definitions
    ):

        results = []

        for p in passive_definitions:

            gate = evaluate_passive_gate(p, runtime_context)

            if not gate["passed"]:
                continue

            raw = compute_passive_formula(p, runtime_context)

            final = apply_passive_transform(p, raw, runtime_context)

            meta = build_passive_runtime_metadata(p, runtime_context.get("tick"))

            results.append(
                build_passive_runtime_result(
                    p,
                    raw,
                    final,
                    gate,
                    runtime_metadata=meta
                )
            )

        return results
    def apply_passive_state(
        self,
        runtime_state,
        passive_results
    ):

        new_state = dict(runtime_state)

        for passive in passive_results:

            for output in passive.get(
                "outputs",
                []
            ):

                target = output.get("target")

                if target is None:
                    continue

                delta = output.get(
                    "value",
                    0.0
                )

                mode = output.get(
                    "mode",
                    "add"
                )

                current = new_state.get(
                    target,
                    0.0
                )

                if mode == "add":

                    new_state[target] = (
                        current + delta
                    )

                elif mode == "subtract":

                    new_state[target] = (
                        current - delta
                    )

                elif mode == "replace":

                    new_state[target] = delta

                else:

                    raise ValueError(
                        f"Unknown passive update mode: {mode}"
                    )

        return new_state
