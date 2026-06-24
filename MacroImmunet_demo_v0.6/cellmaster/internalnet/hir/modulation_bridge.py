# cellmaster/internalnet/hir/modulation_bridge.py

from aip.vml.hir_bridge import (
    build_hir_interpretation_delta
)


def extract_hir_interpretation_delta(
    modulation_runtime_state
):

    payloads = (
        modulation_runtime_state.get(
            "payloads",
            []
        )
    )

    for payload_entry in payloads:

        if payload_entry.get(
            "_payload_type"
        ) == "vml":

            return (
                build_hir_interpretation_delta(
                    payload_entry.get(
                        "payload",
                        {}
                    )
                )
            )

    return {}
