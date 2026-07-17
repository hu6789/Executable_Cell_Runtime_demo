# demo/observer/console_logger.py

"""
=========================================================
Console Logger
=========================================================

Human-readable runtime logger.

Responsibilities
----------------
- display TickRecord
- format runtime information
- provide demo-friendly console output

DOES NOT
--------
- access SimulationWorld
- compute statistics
- store history
"""

from pprint import pprint


class ConsoleLogger:

    """
    Console output for demo runtime.

    Input:
        TickRecord
    """

    # =====================================================
    # Public
    # =====================================================
    
    def __init__(

        self,

        enabled=True

    ):

        self.enabled = enabled
    

    def log(

        self,

        record

    ):

        if not self.enabled:

            return

        self._print_header(record)

        self._print_statistics(record)

        self._print_cells(record)

        self._print_substances(record)

        self._print_fields(record)

    # =====================================================
    # Header
    # =====================================================

    def _print_header(

        self,

        record

    ):

        print()

        print("=" * 60)

        print(f"Tick {record.tick}")

        print("=" * 60)

    # =====================================================
    # Statistics
    # =====================================================

    def _print_statistics(

        self,

        record

    ):

        stats = record.statistics

        print("\n[Statistics]")

        print(f"Cells       : {stats.cell_count}")

        print(f"Substances  : {stats.substance_count}")

        print(f"Fields      : {stats.field_count}")

        if stats.average_runtime_state:

            print("\nAverage Runtime State")

            for k, v in sorted(

                stats.average_runtime_state.items()

            ):

                print(f"  {k:<20}: {v:.3f}")

    # =====================================================
    # Cells
    # =====================================================

    def _print_cells(

        self,

        record

    ):

        print("\n[Cells]")

        for cell_id, cell in record.snapshot.cells.items():

            print(f"\n{cell_id}")

            print(

                f"  template : "

                f"{cell['template_id']}"

            )

            print(

                f"  position : "

                f"{cell['position']}"

            )

            runtime = cell["runtime_state"]

            for key, value in sorted(runtime.items()):

                print(

                    f"  {key:<20}: "

                    f"{value}"

                )

    # =====================================================
    # Substances
    # =====================================================

    def _print_substances(

        self,

        record

    ):

        if not record.snapshot.substances:

            return

        print("\n[Substances]")

        for sid, sub in (

            record.snapshot.substances.items()

        ):

            print(f"\n{sid}")

            pprint(sub)

    # =====================================================
    # Fields
    # =====================================================

    def _print_fields(

        self,

        record

    ):

        if not record.snapshot.fields:

            return

        print("\n[Fields]")

        for name, values in (

            record.snapshot.fields.items()

        ):

            print(f"\n{name}")

            for pos, value in sorted(values.items()):

                print(

                    f"  {pos} : {value:.3f}"

                )
