import ctypes
from pathlib import Path
import sys


PALETTE = {
    "dusk_blue": "#355070",
    "dusty_lavender": "#6d597a",
    "rosewood": "#b56576",
    "light_coral": "#e56b6f",
    "light_bronze": "#eaac8b",
}

BUTTON_COLORS = (
    PALETTE["dusk_blue"],
    PALETTE["dusty_lavender"],
    PALETTE["rosewood"],
    PALETTE["light_coral"],
    PALETTE["light_bronze"],
    PALETTE["dusk_blue"],
)

BLACK = "#000000"
WHITE = "#fffaf5"
DISABLED_BG = "#8f8a88"
TRANSPARENT_KEY = "#010203"
PANEL_BG = TRANSPARENT_KEY
CONSOLE_BG = PALETTE["dusk_blue"]
TITLE_FONT = "Playfair Display"
UI_FONT = "Geomini"
WINDOW_ALPHA = 1.0
WINDOW_TOPMOST = True
WINDOW_TRANSPARENT_COLOR = TRANSPARENT_KEY
BACKGROUND_ALPHA = 0.75
BACKGROUND_TRANSPARENCY = 1.0 - BACKGROUND_ALPHA
CONSOLE_WARNING = "#ff9f1c"
CONSOLE_ERROR = "#ff4d4f"
CONSOLE_SUCCESS = "#2ecc71"
TITLE_LETTER_COLORS = (
    PALETTE["dusk_blue"],
    PALETTE["rosewood"],
    PALETTE["light_coral"],
    PALETTE["light_bronze"],
)


def lighten_hex(color, amount=0.14):
    color = color.lstrip("#")
    channels = [int(color[index:index + 2], 16) for index in (0, 2, 4)]
    lightened = [round(channel + (255 - channel) * amount) for channel in channels]
    return "#" + "".join(f"{channel:02x}" for channel in lightened)


def register_private_fonts(project_root):
    """Registra las fuentes del proyecto solo para este proceso en Windows."""
    if sys.platform != "win32":
        return []
    fonts_root = Path(project_root) / "assets" / "fonts"
    font_paths = (
        fonts_root / "Geomini" / "static" / "Geomini-Regular.ttf",
        fonts_root / "Geomini" / "static" / "Geomini-SemiBold.ttf",
        fonts_root / "Playfair_Display" / "static" / "PlayfairDisplay-Regular.ttf",
        fonts_root / "Playfair_Display" / "static" / "PlayfairDisplay-Bold.ttf",
    )
    add_font = ctypes.windll.gdi32.AddFontResourceExW
    loaded = []
    for font_path in font_paths:
        if font_path.exists() and add_font(str(font_path), 0x10, 0):
            loaded.append(font_path)
    return loaded
