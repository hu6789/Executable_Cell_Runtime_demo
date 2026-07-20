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

from visualization.style import (
    get_cell_color,
    get_field_color
)

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
        
        self.selected_object = None

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


        if not values:

            return


        field_type = field.get(

            "type",

            ""

        )


        base_color = get_field_color(

            field_type

        )


        max_strength = max(

            values.values()

        )
 

        if max_strength <= 0:

            return


        overlay = pygame.Surface(

            screen.get_size(),

            pygame.SRCALPHA

        )


        for position, strength in values.items():


            ratio = strength / max_strength


            #
            # nonlinear amplification
            #
            # because concentration has long tail
            #

            visual = ratio ** 0.35

 
            center = self.world_to_screen(

                position

            )


            #
            # concentration -> radius
            #

            radius = int(

               12 + visual * 45

            )


            #
            # concentration -> alpha
            #

            alpha = int(
  
                20 + visual * 180

            )


            #
            # concentration -> brightness
            #

            color = (
 
                min(255, int(base_color[0] * (0.5 + visual*0.5))),

                min(255, int(base_color[1] * (0.5 + visual*0.5))),

                min(255, int(base_color[2] * (0.5 + visual*0.5)))

            )


            pygame.draw.circle(

                overlay,

                color + (alpha,),

                center,

                radius

            )


        screen.blit(

            overlay,

            (0,0)

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


        color = get_cell_color(

            cell.get("type")

            or

            cell.get("cell_type")

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

        if not self.selected_object:
            return


        objects = self.selected_object


        if not isinstance(objects, list):
            objects = [objects]


        for obj in objects:

            if obj["object_type"] != "cell":
                continue


            cell = obj["data"]


            position = self.world_to_screen(
                cell.get(
                    "position",
                    (0,0)
                )
            )


            pygame.draw.circle(

                screen,

                (255,255,255),

                position,

                self.cell_radius+4,

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

                return cell


        return None
        
    def pick_fields(
        self,
        position,
        snapshot=None
    ):

        result=[]

        if snapshot is None:
            return result

        fields = snapshot.get(
            "fields",
            []
        )

        for field in fields:

            values = field.get(
                "values",
                {}
            )

            for grid_position,strength in values.items():

                if strength <=0:
                    continue

                center=self.world_to_screen(
                    grid_position
                )


                distance=math.sqrt(
                    (center[0]-position[0])**2+
                    (center[1]-position[1])**2
                )


                radius=max(
                    15,
                    int(12+strength*0.5)
                )

 
                if distance<=radius:

                    result.append(
                        {
                            "object_type":"field",
                            "data":
                            {
                                "field_type":
                                    field.get("type"),

                                "position":
                                    grid_position,

                                "strength":
                                    strength
                            }
                        }
                    )

                    break


        return result
        
    def pick_object(
        self,
        position,
        snapshot=None
    ):

        if snapshot is None:
            return []


        if "world" in snapshot:
            snapshot = snapshot["world"]


        objects = []

        cell = self.pick_cell(
            position,
            snapshot
        )

        if cell is not None:

            objects.append(
                {
                    "object_type":"cell",
                    "data":cell
                }
            )

        fields = self.pick_fields(
            position,
            snapshot
        )

        objects.extend(fields)


        objects.sort(
            key=lambda x:
            0 if x["object_type"]=="cell" else 1
        )


        return objects
