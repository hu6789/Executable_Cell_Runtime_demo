# intentbuilder/signal_translation.py

"""
Translate InternalNet field names into world field names.

Behavior requests already use `field_type`.

This translator only performs semantic alias mapping.
"""

from semantic.cell_to_world_map import (
    CELL_TO_WORLD_SIGNAL_MAP
)


def translate_signal(request):

    translated = dict(request)

    payload = dict(

        translated.get(
            "payload",
            {}
        )
    )

    field_type = payload.get(
        "field_type"
    )

    translated_field = (

        CELL_TO_WORLD_SIGNAL_MAP.get(
            field_type,
            field_type
        )

    )

    payload["field_type"] = translated_field

    translated["payload"] = payload

    return translated
