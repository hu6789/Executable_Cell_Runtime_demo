# intentbuilder/signal_translation.py

from semantic.cell_to_world_map import (
    CELL_TO_WORLD_SIGNAL_MAP
)


def translate_signal(request):

    translated = dict(request)

    signal = request.get(
        "signal"
    )

    translated["translated_signal"] = (

        CELL_TO_WORLD_SIGNAL_MAP.get(
            signal,
            signal
        )
    )

    return translated
