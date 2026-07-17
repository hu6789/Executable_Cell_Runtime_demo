# visualization/sidebar.py

"""
Visualization Sidebar

Right inspection panel for MacroImmunet Viewer.

Shows

    - basic information
    - important nodes
    - active behaviors
    - labels

Everything comes from visualization snapshot.
"""

import pygame


# ==========================================================
# Sidebar
# ==========================================================

class Sidebar:

    def __init__(

        self,

        rect=(1100, 40, 320, 820)

    ):

        self.rect = pygame.Rect(*rect)

        pygame.font.init()

        self.title_font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

        self.header_font = pygame.font.SysFont(
            "Arial",
            18,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            16
        )

    # ======================================================
    # Render
    # ======================================================

    def render(

        self,

        screen,

        snapshot,

        selected

    ):

        pygame.draw.rect(

            screen,

            (42, 42, 48),

            self.rect

        )

        pygame.draw.rect(

            screen,

            (90, 90, 90),

            self.rect,

            1

        )

        if selected is None:

            text = self.title_font.render(

                "Select a Cell",

                True,

                (220,220,220)

            )

            screen.blit(

                text,

                (

                    self.rect.left+20,

                    self.rect.top+20

                )

            )

            return

        y = self.rect.top + 20

        y = self.draw_title(

            screen,

            selected,

            y

        )

        y = self.draw_basic(

            screen,

            selected,

            y

        )

        y = self.draw_nodes(

            screen,

            selected,

            y

        )

        y = self.draw_behaviors(

            screen,

            selected,

            y

        )

        self.draw_labels(

            screen,

            selected,

            y

        )

    # ======================================================
    # Helpers
    # ======================================================

    def runtime(

        self,

        obj

    ):

        return obj.get(

            "runtime_state",

            {}

        )

    def header(

        self,

        screen,

        title,

        y

    ):

        surf = self.header_font.render(

            title,

            True,

            (120,210,255)

        )

        screen.blit(

            surf,

            (

                self.rect.left+18,

                y

            )

        )

        return y+28

    def text(

        self,

        screen,

        string,

        y,

        color=(220,220,220)

    ):

        surf = self.font.render(

            str(string),

            True,

            color

        )

        screen.blit(

            surf,

            (

                self.rect.left+20,

                y

            )

        )

    # ======================================================
    # Title
    # ======================================================

    def draw_title(

        self,

        screen,

        obj,

        y

    ):

        title = obj.get(

            "type",

            "Cell"

        )

        surf = self.title_font.render(

            title,

            True,

            (255,255,255)

        )

        screen.blit(

            surf,

            (

                self.rect.left+20,

                y

            )

        )

        return y+42

    # ======================================================
    # Basic
    # ======================================================

    def draw_basic(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Information",

            y

        )

        self.text(

            screen,

            f"ID : {obj.get('id')}",

            y

        )

        y += 22

        self.text(

            screen,

            f"Alive : {obj.get('alive')}",

            y

        )

        y += 22

        self.text(

            screen,

            f"Position : {obj.get('position')}",

            y

        )

        return y+34

    # ======================================================
    # Nodes
    # ======================================================

    def important_nodes(

        self,

        cell_type

    ):

        mapping = {

            "host_cell":[

                "ATP",

                "pMHC",

                "cell_membrane",

                "influenza",

                "pathogen_signal"

            ],

            "cd4_t_cell":[

                "ATP",

                "TCR",

                "IL2R",

                "IL2",

                "amino_acid"

            ],

            "cd8_t_cell":[

                "ATP",

                "TCR",

                "IL2R",

                "perforin",

                "amino_acid"

            ]

        }

        return mapping.get(

            cell_type,

            []

        )

    def draw_nodes(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Nodes",

            y

        )

        runtime = self.runtime(

            obj

        )

        nodes = runtime.get(

            "nodes",

            {}

        )

        wanted = self.important_nodes(

            obj.get(

                "type"

            )

        )

        if not wanted:

            self.text(

                screen,

                "(none)",

                y

            )

            return y+30

        for name in wanted:

            value = nodes.get(

                name,

                "-"

            )

            self.text(

                screen,

                f"{name:18} {value}",

                y

            )

            y += 20

        return y+18

    # ======================================================
    # Behaviors
    # ======================================================

    def draw_behaviors(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Behaviors",

            y

        )

        runtime = self.runtime(

            obj

        )

        behaviors = runtime.get(

            "behaviors",

            {}

        )

        if isinstance(

            behaviors,

            dict

        ):

            names = list(

                behaviors.keys()

            )

        else:

            names = behaviors

        if not names:

            self.text(

                screen,

                "(none)",

                y

            )

            return y+28

        for name in names:

            self.text(

                screen,

                name,

                y

            )

            y += 20

        return y+18

    # ======================================================
    # Labels
    # ======================================================

    def draw_labels(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Labels",

            y

        )

        runtime = self.runtime(

            obj

        )

        labels = runtime.get(

            "labels",

            []

        )

        if not labels:

            self.text(

                screen,

                "(none)",

                y

            )

            return

        for label in labels:

            surf = self.font.render(

                f"[ {label} ]",

                True,

                (255,220,120)

            )

            screen.blit(

                surf,

                (

                    self.rect.left+20,

                    y

                )

            )

            y += 22
