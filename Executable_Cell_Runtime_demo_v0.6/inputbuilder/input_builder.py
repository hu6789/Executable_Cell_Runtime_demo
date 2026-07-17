# inputbuilder/input_builder.py

from inputbuilder.event_dispatcher import (
    dispatch_events
)

from inputbuilder.signalmap_translation import (
    translate_perception
)

from inputbuilder.semantic_processor import (
    process_semantics
)

from inputbuilder.receptor_processor import (
    process_receptors
)

from inputbuilder.field_processor import (
    process_field_inputs
)

from inputbuilder.node_input_standardizer import (
    standardize_node_inputs
)

from inputbuilder.interaction_request_builder import (
    build_interaction_requests
)

from inputbuilder.asi_plugin import (
    AdaptiveSpecificityInterpreter
)

DEBUG = False


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)
             
class InputBuilder:

    """
    standardized biological event
    →
    intracellular computable input
    """

    def __init__(self):

        self.event_buffer = []

        self.asi = (
            AdaptiveSpecificityInterpreter()
        )

    # =====================================
    # collect events
    # =====================================

    def collect(
        self,
        events
    ):

        if not events:

            return

        self.event_buffer.extend(
            events
        )

    # =====================================
    # build pipeline
    # =====================================

    def build(self):

        # ---------------------------------
        # dispatch
        # ---------------------------------

        grouped = dispatch_events(

            self.event_buffer
        )

        translated = {}

        # ---------------------------------
        # signal translation
        # ---------------------------------

        for target_id, events in grouped.items():

            translated[target_id] = (

                translate_perception(
                    target_id,
                    events
                )
            )
        debug_print(
            "\n===== TRANSLATED ====="
        )
        debug_print(translated)
        # ---------------------------------
        # semantic processing
        # ---------------------------------

        semantic_processed = (

            process_semantics(
                translated
            )
        )
        debug_print(
            "\n===== SEMANTIC ====="
        )
        debug_print(semantic_processed)
        # ---------------------------------
        # receptor processing
        # ---------------------------------

        receptor_processed = (

            process_receptors(
                semantic_processed
            )
        )
        debug_print(
            "\n===== RECEPTOR ====="
        )
        debug_print(receptor_processed)
        # ---------------------------------
        # field processing
        # ---------------------------------

        field_processed = (

            process_field_inputs(
                receptor_processed
            )
        )

        # ---------------------------------
        # standardize
        # ---------------------------------

        node_inputs = (

            standardize_node_inputs(
                field_processed
            )
        )

        # ---------------------------------
        # ASI plugin
        # ---------------------------------

        node_inputs = self.asi.apply(
            node_inputs
        )

        # ---------------------------------
        # interaction requests
        # ---------------------------------

        interaction_requests = (

            build_interaction_requests(
                node_inputs
            )
        )

        # cleanup
        self.event_buffer.clear()

        return {

            "node_inputs": node_inputs,

            "interaction_requests":
                interaction_requests
        }
