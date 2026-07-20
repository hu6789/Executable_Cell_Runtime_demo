# visualization/event_panel.py

"""
Visualization Event Panel

Human-readable biological event timeline.
"""

import pygame


# ==========================================================
# Event Panel
# ==========================================================

class EventPanel:

    def __init__(
        self,
        rect=(20,220,290,640),
        max_events=24
    ):

        self.rect = pygame.Rect(*rect)

        self.max_events = max_events
        
        self.scroll_offset = 0
        
        self.scroll_pixels = 0
        
        self.auto_follow = True
        
        self.scroll_speed = 1

        pygame.font.init()

        self.title_font = pygame.font.SysFont(

            "Arial",

            22,

            bold=True

        )

        self.tick_font = pygame.font.SysFont(

            "Arial",

            16,

            bold=True

        )

        self.font = pygame.font.SysFont(

            "Arial",

            15

        )

    # ======================================================
    # Render
    # ======================================================

    def render(
        self,
        screen,
        snapshots
    ):

        pygame.draw.rect(

            screen,

            (40,40,45),

            self.rect

        )

        pygame.draw.rect(

            screen,

            (90,90,90),

            self.rect,

            1

        )

        title = self.title_font.render(

            "Events",

            True,

            (255,255,255)

        )

        screen.blit(

            title,

            (

                self.rect.left+15,

                self.rect.top+12

            )

        )

        history = self.build_event_history(
            snapshots
        )

        y = self.rect.top + 48 - self.scroll_pixels

        for block in history:


            tick = block["tick"]


            tick_surface = self.tick_font.render(

                f"Tick {tick}",

                True,

                (120,210,255)

            )


            screen.blit(

                tick_surface,

                (
                    self.rect.left+12,
                    y
                )

            )


            y += 22



            for text,color in block["events"]:


                surf = self.font.render(

                    text,

                    True,

                    color

                )


                screen.blit(

                    surf,

                    (
                        self.rect.left+18,
                        y
                    )

                )


                y += 18


                if y > self.rect.bottom:

                    break


            y += 8
    # ======================================================
    # Build Viewer Events
    # ======================================================

    def build_view_events(

        self,

        snapshot

    ):

        output = []

        #
        # runtime events
        #

        for event in snapshot.get(
            "events",
            []
        ):

            output.append(

                self.translate_visualization_event(
                    event
                )

            )

        #
        # behavior summary
        #

        for cell_id,behavior in snapshot.get(

            "behaviors",

            {}

        ).items():

            names = behavior.get(

                "behaviors",

                {}

            )

            if isinstance(names,dict):

                names = names.keys()

            for name in names:

                output.append(

                    (

                        f"{cell_id}: {name}",

                        (120,255,180)

                    )

                )

        return output

    # ======================================================
    # Translate Runtime Event
    # ======================================================
    def translate_visualization_event(
        self,
        event
    ):

        category = event.get(
            "category",
            "Event"
        )

        message = event.get(
            "message",
            ""
        )


        return (
            message,
            self.get_event_color(category)
        )
    
    def get_event_color(
        self,
        category
    ):

        if category == "Signal":

            return (
                255,
                220,
                120
            )


        if category == "Behavior":

            return (
                120,
                255,
                180
            )
 

        if category == "Substance":

            return (
                255,
                150,
                150
            )


        return (
            220,
            220,
            220
        )
        
    def build_event_history(
        self,
        snapshots
    ):

        history = []


        for snapshot in snapshots:


            tick = snapshot.get(
                "tick",
                0
            )


            events = self.build_view_events(
                snapshot
            )

            if events:
 
                history.append(
                    {
                        "tick": tick,
                        "events": events
                    }
                )

        return history
        
    def handle_event(
        self,
        event
    ):

        if event.type == pygame.MOUSEWHEEL:
        
            self.auto_follow = False

            self.scroll_pixels -= event.y * 30


        elif event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 4:

                self.scroll_offset += 1


            elif event.button == 5:
 
                self.scroll_offset -= 1


        if self.scroll_offset < 0:

            self.scroll_offset = 0
