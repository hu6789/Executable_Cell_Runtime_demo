# visualization/style.py

"""
Visualization Style

Single Source of Truth (SSOT)
for all visualization appearance.

Responsibilities

    - colors

    - fonts

    - spacing

    - panel sizes

    - renderer constants

Does NOT

    - render UI

    - modify simulation

    - process events
"""

from pathlib import Path

import pygame

pygame.font.init()


# ==========================================================
# Asset Path
# ==========================================================

STYLE_DIR = Path(__file__).parent

FONT_DIR = STYLE_DIR / "assets" / "fonts"


# ==========================================================
# Font Loader
# ==========================================================

def load_font(
    filename,
    size,
    bold=False
):
    """
    Try project font first.

    Fallback to system serif.
    """

    path = FONT_DIR / filename

    if path.exists():

        return pygame.font.Font(
            str(path),
            size
        )

    return pygame.font.SysFont(
        "serif",
        size,
        bold=bold
    )


# ==========================================================
# Fonts
# ==========================================================

TITLE_FONT = load_font(
    "LibertinusSerif-Regular.ttf",
    28
)

HEADER_FONT = load_font(
    "LibertinusSerif-Regular.ttf",
    22
)

BODY_FONT = load_font(
    "LibertinusSerif-Regular.ttf",
    18
)

SMALL_FONT = load_font(
    "LibertinusSerif-Regular.ttf",
    15
)

MONO_FONT = pygame.font.SysFont(
    "monospace",
    16
)


# ==========================================================
# Window
# ==========================================================

WINDOW_WIDTH = 1440

WINDOW_HEIGHT = 900

FPS = 60


# ==========================================================
# Layout
# ==========================================================

LEFT_PANEL_WIDTH = 280

RIGHT_PANEL_WIDTH = 320

BOTTOM_PANEL_HEIGHT = 100

TOP_MARGIN = 10

PANEL_PADDING = 12

CELL_RADIUS = 14

VIRUS_RADIUS = 7


# ==========================================================
# Background
# ==========================================================

BACKGROUND = (26, 27, 30)

PANEL = (40, 42, 47)

PANEL_BORDER = (90, 90, 96)

GRID = (60, 60, 65)


# ==========================================================
# Text
# ==========================================================

TEXT = (235, 235, 235)

TEXT_SECONDARY = (180, 180, 180)

TEXT_DISABLED = (120, 120, 120)

TITLE = (255, 255, 255)

ACCENT = (120, 210, 255)


# ==========================================================
# Cell Colors
# ==========================================================

HOST_CELL = (220, 80, 80)

CD4_CELL = (255, 220, 80)

CD8_CELL = (80, 150, 255)

DEAD_CELL = (100, 100, 100)

UNKNOWN_CELL = (180,180,180)


# ==========================================================
# Substance Colors
# ==========================================================

INFLUENZA = (120, 20, 20)

PMHC = (255, 150, 150)

IL2 = (255, 240, 120)

PERFORIN = (120, 200, 255)

# ==========================================================
# Status
# ==========================================================

ACTIVE = (120, 255, 120)

WARNING = (255, 210, 90)

DANGER = (255, 120, 120)

DEAD = (90, 90, 90)


# ==========================================================
# Animation
# ==========================================================

DEFAULT_ALPHA = 255

INACTIVE_ALPHA = 90

FIELD_ALPHA = 100

EVENT_FLASH_TIME = 0.5


# ==========================================================
# UI
# ==========================================================

BUTTON = (70, 70, 74)

BUTTON_HOVER = (95, 95, 105)

BUTTON_BORDER = (180, 180, 180)

BUTTON_TEXT = TEXT


# ==========================================================
# Brightness
# ==========================================================

MIN_BRIGHTNESS = 0.30

MAX_BRIGHTNESS = 1.00


# ==========================================================
# Renderer Lookup
# ==========================================================

CELL_COLOR_MAP = {

    "host":
        HOST_CELL,

    "cd4":
        CD4_CELL,

    "cd8":
        CD8_CELL,

    "dead":
        DEAD_CELL

}


FIELD_COLOR_MAP = {

    "IL2":
        IL2,

    "il2":
        IL2,


    "influenza":
        INFLUENZA,


    "pMHC":
        PMHC,

    "pmhc":
        PMHC,


    "perforin":
        PERFORIN,

    "Perforin":
        PERFORIN

}


# ==========================================================
# Utility
# ==========================================================

def get_cell_color(cell_type):

    if cell_type is None:
        return UNKNOWN_CELL


    name=str(cell_type).lower()


    if name.startswith("host"):
        return HOST_CELL


    if name.startswith("cd4"):
        return CD4_CELL


    if name.startswith("cd8"):
        return CD8_CELL


    if "dead" in name:
        return DEAD_CELL


    return UNKNOWN_CELL


def get_field_color(field_type):

    return FIELD_COLOR_MAP.get(
        str(field_type).lower(),
        UNKNOWN_CELL
    )
