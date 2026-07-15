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
# Capa clara derivada de Light Bronze para simular mayor translucidez sin
# reducir la legibilidad/opacidad de la consola.
PANEL_BG = "#f6ded1"
CONSOLE_BG = PALETTE["dusk_blue"]
TITLE_FONT = "Playfair Display"
UI_FONT = "Geomini"
TITLE_LETTER_COLORS = (
    PALETTE["dusk_blue"],
    PALETTE["dusty_lavender"],
    PALETTE["rosewood"],
    PALETTE["light_coral"],
    PALETTE["light_bronze"],
)


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
