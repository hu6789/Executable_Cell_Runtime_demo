# cellinstance/templates/template_loader.py

import json
import os

from cellinstance.templates.cell_template import (
    CellTemplate
)


# =========================================
# Template Loader
# =========================================

class TemplateLoader:

    """
    biological cell template loader

    responsibilities:
        - load template json files
        - construct CellTemplate objects
        - maintain template registry
        - provide template lookup

    DOES NOT:
        - execute runtime logic
        - create runtime entities
        - modify runtime world
    """

    def __init__(self):

        self.template_registry = {}

    # =====================================
    # load template file
    # =====================================

    def load_template_file(
        self,
        filepath
    ):

        with open(
            filepath,
            "r"
        ) as f:

            template_data = json.load(f)

        template = self.build_template(
            template_data
        )

        self.register_template(
            template
        )
        

        return template

    # =====================================
    # build template object
    # =====================================

    def build_template(
        self,
        template_data
    ):

        return CellTemplate(

            template_id=

                template_data.get(
                    "template_id"
                ),

            identity=

                template_data.get(
                    "identity",
                    {}
                ),

            graph_refs=

                template_data.get(
                    "graph_refs",
                    {}
                ),

            init_node_state=

                template_data.get(
                    "init_node_state",
                    {}
                ),

            hir_capabilities=

                template_data.get(
                    "hir_capabilities",
                    {}
                ),

            exposure_rules=

                template_data.get(
                    "exposure_rules",
                    {}
                ),

            runtime_params=

                template_data.get(
                    "runtime_params",
                    {}
                )
        )

    # =====================================
    # register template
    # =====================================

    def register_template(
        self,
        template
    ):

        self.template_registry[
            template.template_id
        ] = template

    # =====================================
    # get template
    # =====================================

    def get_template(
        self,
        template_id
    ):

        return self.template_registry.get(
            template_id
        )

    # =====================================
    # load template directory
    # =====================================

    def load_template_directory(
        self,
        directory
    ):

        loaded = []

        for filename in os.listdir(
            directory
        ):

            if not filename.endswith(
                ".json"
            ):

                continue

            filepath = os.path.join(

                directory,
                filename
            )

            template = (
                self.load_template_file(
                    filepath
                )
            )

            loaded.append(
                template
            )

        return loaded
