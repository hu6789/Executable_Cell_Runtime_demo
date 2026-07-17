# visualization/legend.py

"""
Visualization Legend

Position

    upper-left panel

Purpose

    explain visualization symbols

Responsibilities

    - display entity colors

    - display entity shapes

    - explain brightness

Does NOT

    render simulation

    modify snapshot

    process events
"""

import pygame


# =========================================
# Legend Panel
# =========================================

class VisualizationLegend:

    def __init__(

        self,

        rect=(20, 20, 260, 80)

    ):

        self.rect = pygame.Rect(*rect)

        pygame.font.init()

        self.title_font = pygame.font.SysFont(
            "Arial",
            20,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            15
        )

        self.entries = [

            (
                "circle",
                (80, 180, 255),
                "Host Cell"
            ),

            (
                "circle",
                (120, 255, 120),
                "CD4 T Cell"
            ),

            (
                "circle",
                (255, 120, 120),
                "CD8 T Cell"
            ),

            (
                "triangle",
                (255, 200, 80),
                "Virus"
            ),

            (
                "square",
                (180, 180, 255),
                "Field"
            )
        ]

    # =====================================
    # Render
    # =====================================

    def render(

        self,

        screen

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

        title = self.title_font.render(

            "Legend",

            True,

            (255, 255, 255)

        )

        screen.blit(

            title,

            (

                self.rect.left + 12,

                self.rect.top + 8

            )

        )

        x = self.rect.left + 14
        y = self.rect.top + 38

        for shape, color, label in self.entries:

            self.draw_symbol(

                screen,

                shape,

                color,

                x,

                y + 7

            )

            text = self.font.render(

                label,

                True,

                (230, 230, 230)

            )

            screen.blit(

                text,

                (

                    x + 18,

                    y

                )

            )

            x += 118

            if x > self.rect.right - 110:

                x = self.rect.left + 14
                y += 22

        y += 26

        info = self.font.render(

            "Brightness: Active → Bright",

            True,

            (170, 170, 170)

        )

        screen.blit(

            info,

            (

                self.rect.left + 12,

                y

            )

        )

    # =====================================
    # Draw Symbol
    # =====================================

    def draw_symbol(

        self,

        screen,

        shape,

        color,

        x,

        y

    ):

        if shape == "circle":

            pygame.draw.circle(

                screen,

                color,

                (x, y),

                5

            )

            return

        if shape == "square":

            pygame.draw.rect(

                screen,

                color,

                pygame.Rect(

                    x - 5,
                    y - 5,
                    10,
                    10

                )

            )

            return

        if shape == "triangle":

            pygame.draw.polygon(

                screen,

                color,

                [

                    (x, y - 6),

                    (x - 6, y + 5),

                    (x + 6, y + 5)

                ]

            )
