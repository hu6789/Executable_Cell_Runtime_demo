# demo/trace_formatter.py

from __future__ import annotations

from typing import Dict


def _fmt(value: float) -> str:
    return "{:.4f}".format(value)


def _state_changes(
    before: Dict[str, float],
    after: Dict[str, float],
) -> str:
    names = sorted(
        set(before).union(after)
    )

    lines = []

    for name in names:
        old = before.get(name, 0.0)
        new = after.get(name, 0.0)

        if abs(new - old) < 1e-12:
            continue

        lines.append(
            "    {:<12} {} → {}".format(
                name,
                _fmt(old),
                _fmt(new),
            )
        )

    return "\n".join(lines)


def print_cell_trace(
    trace,
    cell_id: str,
) -> None:

    cell = trace.cells.get(cell_id)

    if cell is None:
        return

    print()
    print("  Cell {}".format(cell_id))

    # ---------------------------------------------------------
    # NODE
    # ---------------------------------------------------------

    if cell.nodes:
        print()
        print("  [NODE]")

        for item in cell.nodes:
            print(
                "    {}".format(
                    item.node_name
                )
            )

            if (
                abs(
                    item.after_total
                    - item.before_total
                )
                > 1e-12
            ):
                print(
                    "      total : {} → {}".format(
                        _fmt(item.before_total),
                        _fmt(item.after_total),
                    )
                )

            changes = _state_changes(
                item.before_states,
                item.after_states,
            )

            if changes:
                print(changes)

    # ---------------------------------------------------------
    # PASSIVE
    # ---------------------------------------------------------

    if cell.passives:
        print()
        print("  [PASSIVE]")

        for item in cell.passives:
            print(
                "    {}".format(
                    item.passive_name
                )
            )

            print(
                "      {}".format(
                    item.node_name
                )
            )

            changes = _state_changes(
                item.before_states,
                item.after_states,
            )

            if changes:
                print(changes)

    # ---------------------------------------------------------
    # GENE
    # ---------------------------------------------------------

    if cell.genes:
        print()
        print("  [GENE]")

        for item in cell.genes:
            print(
                "    {:<12} {} → {}".format(
                    item.gene_name,
                    _fmt(item.before_value),
                    _fmt(item.after_value),
                )
            )

    # ---------------------------------------------------------
    # HIR
    # ---------------------------------------------------------

    if cell.hir is not None:
        print()
        print("  [HIR]")

        if cell.hir.behaviors:
            print()
            print("    Behavior")

            for item in cell.hir.behaviors:
                print(
                    "      {} · {}".format(
                        item.behavior_name,
                        item.source_name,
                    )
                )

                print(
                    "        intention : {}".format(
                        _fmt(item.intention_value)
                    )
                )

                if item.intention_inputs:
                    print(
                        "        inputs    : {}".format(
                            item.intention_inputs
                        )
                    )

                if abs(item.tf_delta) > 1e-12:
                    print(
                        "        TF Δ      : {}".format(
                            _fmt(item.tf_delta)
                        )
                    )

                if item.resource_allocation:
                    print(
                        "        resources : {}".format(
                            item.resource_allocation
                        )
                    )

                if abs(item.resource_delta) > 1e-12:
                    print(
                        "        resource Δ: {}".format(
                            _fmt(item.resource_delta)
                        )
                    )

                print(
                    "        final     : {}".format(
                        _fmt(item.final_value)
                    )
                )

        if cell.hir.labels:
            print()
            print(
                "    Labels : {}".format(
                    ", ".join(
                        sorted(cell.hir.labels)
                    )
                )
            )

        if cell.hir.type_name is not None:
            print(
                "    Type   : {}".format(
                    cell.hir.type_name
                )
            )


def print_tick_trace(
    trace,
    detailed_cell_id="B",
) -> None:
    """
    Print one tick.

    Cell B gets the detailed trace.
    Other cells are intentionally omitted here;
    the main demo can print their final summary separately.
    """

    print_cell_trace(
        trace,
        detailed_cell_id,
    )
