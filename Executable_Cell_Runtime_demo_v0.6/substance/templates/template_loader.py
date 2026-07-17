# substance/templates/template_loader.py

import json
from pathlib import Path

from substance.templates.substance_template import (
    SubstanceTemplate
)


# =========================================
# load template
# =========================================

def load_substance_template(
    json_path
):

    """
    load a single substance template

    Parameters
    ----------
    json_path : str | Path

    Returns
    -------
    SubstanceTemplate
    """

    path = Path(json_path)

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return SubstanceTemplate(
        data
    )


# =========================================
# load template directory
# =========================================

def load_template_directory(
    directory
):

    """
    load all templates from folder

    Returns
    -------
    dict

    {
        "IFN_alpha": template,
        "TNF_alpha": template
    }
    """

    directory = Path(directory)

    templates = {}

    for file in directory.glob("*.json"):

        template = (
            load_substance_template(
                file
            )
        )

        templates[
            template.substance_type
        ] = template

    return templates
