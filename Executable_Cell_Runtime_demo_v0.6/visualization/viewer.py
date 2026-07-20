# visualization/viewer.py

"""
Visualization Viewer

Top-level pygame window.

Responsibilities

    - own visualization modules

    - playback timeline

    - dispatch mouse / keyboard

    - render every frame

Does NOT

    - execute simulation

    - modify runtime
"""

import pygame

from visualization.renderer import WorldRenderer
from visualization.sidebar import Sidebar
from visualization.event_panel import EventPanel
from visualization.control_panel import ControlPanel
from visualization.legend import VisualizationLegend

# ==========================================================
# Viewer
# ==========================================================

class Viewer:

    def __init__(

        self,

        snapshots,

        scenario_name="Executable_Cell_Runtime"

    ):

        self.snapshots = snapshots

        self.scenario_name = scenario_name

        #
        # playback
        #

        self.current_tick = 0

        self.playing = True

        self.play_speed = 1.0

        self.running = False

        #
        # selection
        #

        self.selected_cell = None
        
        self.selected_object = None

        #
        # pygame
        #

        self.screen = None

        self.clock = None

        #
        # components
        #

        self.renderer = WorldRenderer()
        
        self.legend = VisualizationLegend()

        self.sidebar = Sidebar()

        self.event_panel = EventPanel()

        self.controls = ControlPanel(

            viewer=self,

            x=220,

            y=830,

            width=800,

            height=70

        )

    # ======================================================
    # Initialize
    # ======================================================

    def initialize(

        self,

        title=None

    ):

        pygame.init()

        self.screen = pygame.display.set_mode(

            (1420, 920)

        )

        pygame.display.set_caption(

            title or self.scenario_name

        )

        self.clock = pygame.time.Clock()

    # ======================================================
    # Snapshot
    # ======================================================

    def current_snapshot(self):

        if not self.snapshots:

            return None

        return self.snapshots[self.current_tick]

    # ======================================================
    # Playback
    # ======================================================

    def play(self):

        self.playing = True

    def pause(self):

        self.playing = False

    def toggle(self):

        self.playing = not self.playing

    def reset(self):

        self.current_tick = 0

    def advance(self):

        if self.current_tick < len(self.snapshots) - 1:

            self.current_tick += 1

        else:

            #
            # stop at end
            #

            self.playing = False

    def step_forward(self):

        if self.current_tick < len(self.snapshots) - 1:

            self.current_tick += 1

    def step_backward(self):

        if self.current_tick > 0:

            self.current_tick -= 1

    # ======================================================
    # Rendering
    # ======================================================

    def render(self):

        self.screen.fill(

            (24, 24, 28)

        )

        snapshot = self.current_snapshot()

        if snapshot is None:

            return

        self.renderer.render(

            self.screen,

            snapshot

        )
        
        self.legend.render(

            self.screen

        )

        self.sidebar.render(
            self.screen,
            snapshot,
            self.selected_object
        )

        self.event_panel.render(
            self.screen,
            self.snapshots[:self.current_tick+1]
        )

        self.controls.draw(

            self.screen

        )

        #
        # Tick title
        #

        pygame.display.set_caption(

            f"{self.scenario_name}    Tick {self.current_tick}"

        )

    # ======================================================
    # Events
    # ======================================================

    def handle_events(self):

        snapshot = self.current_snapshot()

        for event in pygame.event.get():
        
            self.event_panel.handle_event(
                event
            )

            self.controls.handle_event(

                event

            )

            #
            # quit
            #

            if event.type == pygame.QUIT:

                self.running = False

            #
            # keyboard
            #

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    self.toggle()

                elif event.key == pygame.K_RIGHT:

                    self.step_forward()

                elif event.key == pygame.K_LEFT:

                    self.step_backward()

                elif event.key == pygame.K_HOME:

                    self.current_tick = 0

                elif event.key == pygame.K_END:

                    self.current_tick = max(

                        0,

                        len(self.snapshots) - 1

                    )

            #
            # mouse
            #

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if snapshot is None:

                    continue

                selected = self.renderer.pick_object(

                    event.pos,

                    snapshot

                )
                
                self.selected_object = selected

    # ======================================================
    # Main Loop
    # ======================================================

    def run(

        self,

        fps=30

    ):

        self.initialize(

            title=f"MacroImmunet Viewer - {self.scenario_name}"

        )

        self.running = True

        playback_counter = 0

        while self.running:

            self.handle_events()

            #
            # playback
            #

            if self.playing:

                playback_counter += 1

                if playback_counter >= max(

                    1,

                    int(30 / self.play_speed)

                ):

                    self.advance()

                    playback_counter = 0

            self.render()

            pygame.display.flip()

            self.clock.tick(fps)

        pygame.quit()
