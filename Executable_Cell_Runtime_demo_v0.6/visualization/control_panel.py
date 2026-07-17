# visualization/control_panel.py

"""
Viewer Control Panel

Responsibilities

    - playback buttons

    - tick information

    - speed information

    - shortcut hint

Does NOT

    - execute simulation

    - modify snapshots
"""

import pygame


# ==========================================================
# Control Panel
# ==========================================================

class ControlPanel:

    def __init__(

        self,

        viewer,

        x,

        y,

        width,

        height

    ):

        self.viewer = viewer

        self.rect = pygame.Rect(

            x,

            y,

            width,

            height

        )

        self.font = pygame.font.SysFont(

            None,

            20

        )

        self.small_font = pygame.font.SysFont(

            None,

            16

        )

        self.buttons = {}

        self.button_width = 88
        self.button_height = 34
        self.margin = 10

        self.build_buttons()

    # =====================================================
    # Layout
    # =====================================================

    def build_buttons(self):

        names = [

            "Play",

            "Pause",

            "Prev",

            "Next",

            "Reset"

        ]

        x = self.rect.left + self.margin

        y = self.rect.top + 8

        for name in names:

            self.buttons[name] = pygame.Rect(

                x,

                y,

                self.button_width,

                self.button_height

            )

            x += self.button_width + 8

    # =====================================================
    # Draw
    # =====================================================

    def draw(

        self,

        screen

    ):

        pygame.draw.rect(

            screen,

            (45,45,45),

            self.rect

        )

        pygame.draw.rect(

            screen,

            (120,120,120),

            self.rect,

            1

        )

        #
        # buttons
        #

        for name, rect in self.buttons.items():

            pygame.draw.rect(

                screen,

                (75,75,75),

                rect,

                border_radius=6

            )

            pygame.draw.rect(

                screen,

                (180,180,180),

                rect,

                1,

                border_radius=6

            )

            label = self.font.render(

                name,

                True,

                (255,255,255)

            )

            screen.blit(

                label,

                label.get_rect(center=rect.center)

            )

        #
        # information
        #

        total = len(self.viewer.snapshots)

        info = [

            f"Tick : {self.viewer.current_tick}/{max(total-1,0)}",

            f"Speed : {self.viewer.play_speed:.1f}x",

            f"Scenario : {self.viewer.scenario_name}"

        ]

        x = self.rect.left + 520

        y = self.rect.top + 10

        for line in info:

            text = self.font.render(

                line,

                True,

                (220,220,220)

            )

            screen.blit(

                text,

                (x,y)

            )

            y += 22

        #
        # shortcuts
        #

        hint = (

            "Space Play/Pause   "

            "← Prev   "

            "→ Next   "

            "Home First   "

            "End Last"

        )

        text = self.small_font.render(

            hint,

            True,

            (170,170,170)

        )

        screen.blit(

            text,

            (

                self.rect.left + 12,

                self.rect.bottom - 22

            )

        )

    # =====================================================
    # Mouse
    # =====================================================

    def handle_event(

        self,

        event

    ):

        if event.type != pygame.MOUSEBUTTONDOWN:

            return

        for name, rect in self.buttons.items():

            if rect.collidepoint(event.pos):

                self.click(name)

                break

    # =====================================================
    # Button Actions
    # =====================================================

    def click(

        self,

        name

    ):

        if name == "Play":

            self.viewer.play()

        elif name == "Pause":

            self.viewer.pause()

        elif name == "Prev":

            self.viewer.step_backward()

        elif name == "Next":

            self.viewer.step_forward()

        elif name == "Reset":

            self.viewer.reset()
