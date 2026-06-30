# minisio/core/minisio.py

from typing import Any, Dict, List

from minisio.normalizer.request_normalizer import RequestNormalizer
from minisio.core.router import MiniSIORouter

from minisio.compiler.runtime_state_compiler import (
    RuntimeStateCompiler
)
from minisio.compiler.field_compiler import (
    FieldCompiler
)
from minisio.compiler.entity_compiler import (
    EntityCompiler
)
from minisio.compiler.substance_compiler import (
    SubstanceCompiler
)
from minisio.compiler.event_compiler import (
    EventCompiler
)

from minisio.minisio_schema import (
    MiniSIORequestPackage
)


# =========================================================
# MiniSIO Core v0.7
# =========================================================

class MiniSIO:

    """
    MiniSIO Runtime Orchestrator

    Responsibilities
    ----------------
    - normalize external requests
    - route normalized requests
    - dispatch compiler pipelines
    - package compiler outputs

    DOES NOT
    --------
    - execute simulation
    - modify LabelCenter
    - invoke dynamics
    - perform biological reasoning
    """

    def __init__(
        self,
        schema: Dict[str, Any] = None
    ):

        self.schema = schema or {}

        self.normalizer = RequestNormalizer()

        self.router = MiniSIORouter()

        self.compilers = {

            "runtime_state":
                RuntimeStateCompiler(
                    schema=self.schema
                ),

            "field":
                FieldCompiler(
                    schema=self.schema
                ),

            "entity":
                EntityCompiler(
                    schema=self.schema
                ),

            "substance":
                SubstanceCompiler(
                    schema=self.schema
                ),

            "event":
                EventCompiler()

        }

    # =====================================================
    # Public Entry
    # =====================================================

    def receive(

        self,

        raw_requests: List[Dict[str, Any]],

        metadata: Dict[str, Any] = None

    ) -> MiniSIORequestPackage:

        metadata = metadata or {}

        # -------------------------------------------------
        # Normalize
        # -------------------------------------------------

        normalized_requests = self.normalizer.normalize_batch(
            raw_requests
        )

        # -------------------------------------------------
        # Route
        # -------------------------------------------------

        routed_requests = self.router.route(
            normalized_requests
        )

        # -------------------------------------------------
        # Compile
        # -------------------------------------------------

        compiled_packages = []

        for write_mode, requests in routed_requests.items():

            compiler = self.compilers.get(
                write_mode
            )

            if compiler is None:
                continue

            compiled_packages.extend(

                compiler.compile(

                    requests,

                    metadata=metadata

                )

            )

        # -------------------------------------------------
        # Package
        # -------------------------------------------------

        return MiniSIORequestPackage(

            requests=compiled_packages,

            metadata={

                "status": "ok",

                "raw_count": len(raw_requests),

                "normalized_count": len(normalized_requests),

                "compiled_count": len(compiled_packages),

                "write_modes": list(routed_requests.keys()),

                "source": metadata.get(
                    "source",
                    "MiniSIO"
                )

            }

        )
