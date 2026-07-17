# visualization/renderer.py

"""
2D World Renderer

Position

    middle visualization panel

Purpose

    render simulation world

Responsibilities

    - draw cells

    - draw fields

    - draw selection

    - perform cell picking

Does NOT

    display events

    display inspector

    control playback
"""

import math
import pygame


# =========================================
# Renderer
# =========================================

class WorldRenderer:

    """
    render simulation world
    """

    def __init__(

        self,

        world_rect=(220,40,860,820)

    ):

        self.world_rect = pygame.Rect(*world_rect)

        self.cell_radius = 16

        self.selected_cell = None

        self.font = None
        
    # =====================================
    # Coordinate
    # =====================================

    def world_to_screen(
        self,
        position
    ):

        grid_x, grid_y = position

        cell_size = 40

        x = (
            self.world_rect.x
            + grid_x * cell_size
            + cell_size // 2
        )

        y = (
            self.world_rect.y
            + grid_y * cell_size
            + cell_size // 2
        )

        return (x, y)
    

    # =====================================
    # Render
    # =====================================

    def render(

        self,

        screen,

        snapshot
    ):  
        
        
        if self.font is None:

            self.font = pygame.font.SysFont(

                None,

                18

            )

        self.draw_background(screen)

        self.draw_grid(screen)

        if snapshot is None:

            return

        world_snapshot = snapshot.get(
            "world",
            {}
        )

        self.draw_fields(
            screen,
            world_snapshot
        )

        self.draw_cells(
            screen,
            world_snapshot
        )

        self.draw_selection(

            screen
        )

    # =====================================
    # Background
    # =====================================

    def draw_background(

        self,

        screen
    ):

        pygame.draw.rect(

            screen,

            (35, 35, 42),

            self.world_rect

        )

    # =====================================
    # Grid
    # =====================================

    def draw_grid(

        self,

        screen

    ):

        cell_size = 40

        left = self.world_rect.left
        right = self.world_rect.right

        top = self.world_rect.top
        bottom = self.world_rect.bottom

        #
        # vertical
        #

        x = left

        while x <= right:
 
            pygame.draw.line(

                screen,

                (60, 60, 70),

                (x, top),

                (x, bottom)

            )

            x += cell_size
  
        #
        # horizontal
        #

        y = top
 
        while y <= bottom:

            pygame.draw.line(

                screen,

                (60, 60, 70),

                (left, y),

                (right, y)

            )

            y += cell_size

    # =====================================
    # Fields
    # =====================================

    def draw_fields(

        self,

        screen,

        snapshot
    ):

        fields = snapshot.get(

            "fields",

            []

        )

        for field in fields:

            self.draw_single_field(

                screen,

                field
            )

    def draw_single_field(

        self,

        screen,

        field
    ):

        values = field.get(

            "values",

            {}

        )

        for position, strength in values.items():

            center = self.world_to_screen(

                position

            )

            radius = max(

                10,

                int(strength / 4)

            )

            pygame.draw.circle(

                screen,

                (255,255,0),

                center,

                radius,

                2

            )

    # =====================================
    # Cells
    # =====================================

    def draw_cells(

        self,

        screen,

        snapshot
    ):

        cells = snapshot.get(

            "cells",

            []
        )

        for cell in cells:

            self.draw_cell(

                screen,

                cell
            )

    def draw_cell(

        self,

        screen,

        cell

    ):

        world_position = cell.get(

            "position",

            (0, 0)

        )

        screen_position = self.world_to_screen(

            world_position

        )

        color = self.get_cell_color(

            cell

        )

        pygame.draw.circle(

            screen,

            color,

            screen_position,

            self.cell_radius

        )
        
        label = self.font.render(

            cell.get("id", ""),

            True,

            (255,255,255)

        )

        screen.blit(

            label,

            (

                screen_position[0]-15,

                screen_position[1]-28

            )

        )

    # =====================================
    # Selection
    # =====================================

    def draw_selection(

        self,

        screen
    ):

        if self.selected_cell is None:

            return

        world_position = self.selected_cell.get(

            "position",

            (0,0)

        )

        position = self.world_to_screen(

            world_position

        )

        pygame.draw.circle(

            screen,

            (255, 255, 255),

            position,

            self.cell_radius + 4,

            2
        )

    # =====================================
    # Picking
    # =====================================

    def pick_cell(

        self,

        position,

        snapshot=None
    ):

        if snapshot is None:

            return None

        for cell in snapshot.get(

            "cells",

            []

        ):

            x, y = self.world_to_screen(

                cell.get(

                    "position",

                    (0,0)

                )

            )
            
            distance = math.sqrt(

                (x-position[0])**2 +

                (y-position[1])**2

            )

            if distance <= self.cell_radius:

                self.selected_cell = cell

                return cell

        self.selected_cell = None

        return None

    # =====================================
    # Color
    # =====================================

    def get_cell_color(

        self,

        cell
    ):

        cell_type = (

            cell.get("type")

            or

            cell.get("cell_type")
 
            or

            ""

        )

        alive = cell.get(

            "alive",

            True
        )

        if not alive:

            return (

                90,

                90,

                90

            )

        colors = {

            "host_cell":
                (90, 170, 255),

            "cd4_t_cell":
                (90, 220, 90),

            "cd8_t_cell":
                (255, 120, 120),

            "virus":
                (255, 220, 80)
        }

        return colors.get(

            cell_type,

            (180, 180, 180)

        )
