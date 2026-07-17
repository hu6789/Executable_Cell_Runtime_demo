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

        rect=(20,40,180,820),

        max_events=32

    ):

        self.rect = pygame.Rect(*rect)

        self.max_events = max_events

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

        snapshot

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

        y = self.rect.top + 48

        tick = snapshot.get(

            "tick",

            0

        )

        tick_label = self.tick_font.render(

            f"Tick {tick}",

            True,

            (120,210,255)

        )

        screen.blit(

            tick_label,

            (

                self.rect.left+12,

                y

            )

        )

        y += 26

        events = self.build_view_events(

            snapshot

        )

        if len(events) > self.max_events:

            events = events[-self.max_events:]

        for text,color in events:

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

            y += 20

            if y > self.rect.bottom-20:

                break

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

                self.translate_runtime_event(

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

    def translate_runtime_event(

        self,

        event

    ):

        event_type = event.get(

            "title",

            ""

        )

        payload = event.get(

            "payload",

            {}

        )

        if event_type == "field_exposure_event":

            target = payload.get(

                "target_id",

                "cell"

            )

            field = (

                payload

                .get(

                    "payload",

                    {}

                )

                .get(

                    "field_type",

                    "field"

                )

            )

            return (

                f"{target} senses {field}",

                (255,220,120)

            )

        if "virus" in event_type:

            return (

                event_type,

                (255,180,120)

            )

        if "kill" in event_type:

            return (

                event_type,

                (255,120,120)

            )

        return (

            event_type,

            (220,220,220)

        )
