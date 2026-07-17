# intentbuilder/intent_builder.py

from intentbuilder.request_collector import (
    collect_requests
)

from intentbuilder.signal_translation import (
    translate_signal
)

from intentbuilder.value_scaler import (
    scale_request_values
)

from intentbuilder.intent_standardizer import (
    standardize_intent
)

from intentbuilder.semantic_merge import (
    semantic_merge
)


class IntentBuilder:

    """
    v0.6 World Semantic Translation Layer
    """

    def __init__(self):

        self.request_queue = []

    # =====================================
    # collect runtime requests
    # =====================================

    def collect(self, requests):

        result = collect_requests(

            request_queue=self.request_queue,

            incoming_requests=requests
        )

        accepted = len(
            result["accepted"]
        )

        rejected = len(
            result["rejected"]
        )

        print(

            f"[IntentBuilder] "

            f"accepted={accepted} "

            f"rejected={rejected}"
        )

    # =====================================
    # build intents
    # =====================================

    def build(self):

        standardized = []

        for request in self.request_queue:

            # ---------------------------------
            # value scaling
            # ---------------------------------

            scaled = scale_request_values(
                request
            )

            # ---------------------------------
            # semantic translation
            # ---------------------------------

            translated = translate_signal(
                scaled
            )

            # ---------------------------------
            # standardization
            # ---------------------------------

            intent = standardize_intent(
                translated
            )

            if intent is not None:

                standardized.append(
                    intent
                )

        # =====================================
        # semantic merge
        # =====================================

        merged = semantic_merge(
            standardized
        )

        # clear queue
        self.request_queue.clear()

        return merged
