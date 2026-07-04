from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "video_proceso_analaisis" / "analisis_diagnostico"
MP4_PATH = OUT_DIR / "video_medidas_03_analisis_diagnostico.mp4"
SCREENSHOT = Path(
    r"C:\Users\PEPIN\AppData\Local\Temp\codex-clipboard-9e5c50c3-7e9a-456b-8dfe-b77f84df32f6.png"
)

W, H = 1280, 720
INK = "#17212F"
MUTED = "#5D6876"
WHITE = "#FFFFFF"
BG = "#F5F7FA"
BLUE = "#174A7C"
NAVY = "#123F68"
TEAL = "#0F766E"
AMBER = "#D9941E"
PURPLE = "#7446A8"
RED = "#B63B3B"
GRID = "#D7DEE8"


def font(size: int, bold: bool = False):
    files = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for file in files:
        try:
            return ImageFont.truetype(file, size)
        except OSError:
            pass
    return ImageFont.load_default()


TITLE = font(34, True)
H2 = font(25, True)
H3 = font(21, True)
BODY = font(18)
SMALL = font(15)
TINY = font(13)
MONO = font(15)


def wrap_px(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        words = raw.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and draw.textlength(candidate, font=fnt) > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    return lines


def write_text(draw, xy, text, max_width, fill=INK, fnt=BODY, gap=5) -> int:
    x, y = xy
    for line in wrap_px(draw, text, max_width, fnt):
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + gap
    return y


def panel(draw, box, fill=WHITE, outline=GRID, width=2):
    draw.rounded_rectangle(box, radius=8, fill=fill, outline=outline, width=width)


def header(draw, title: str, subtitle: str = ""):
    draw.rectangle((0, 0, W, 78), fill=WHITE)
    draw.text((34, 20), title, fill=INK, font=TITLE)
    if subtitle:
        draw.text((620, 30), subtitle, fill=MUTED, font=SMALL)


def base(title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    header(draw, title, subtitle)
    return img, draw


def load_screenshot() -> Image.Image:
    if not SCREENSHOT.exists():
        raise FileNotFoundError(f"No existe la captura: {SCREENSHOT}")
    return Image.open(SCREENSHOT).convert("RGB")


def slide_cover() -> Image.Image:
    img, draw = base("Como elegir medidas para la pagina 03", "Power BI - Analisis diagnostico")
    panel(draw, (54, 112, 1226, 620), fill="#102A43", outline="#102A43")
    draw.text((92, 155), "De tabla a visual", fill=WHITE, font=TITLE)
    write_text(
        draw,
        (95, 220),
        "Objetivo: entender que tabla usar, que columnas tratar, como relacionarlas y que medida DAX construir para cada visual.",
        850,
        fill=WHITE,
        fnt=H2,
        gap=10,
    )
    steps = ["1. Pregunta", "2. Grano", "3. Columnas", "4. Relaciones", "5. Medida", "6. Visual"]
    x = 100
    for step in steps:
        draw.rounded_rectangle((x, 475, x + 165, 535), radius=8, fill="#EAF4FF")
        draw.text((x + 18, 495), step, fill=INK, font=SMALL)
        x += 178
    return img


def slide_real_page() -> Image.Image:
    img, draw = base("La pagina real: 03_Analisis_diagnostico")
    shot = load_screenshot()
    shot.thumbnail((880, 570), Image.Resampling.LANCZOS)
    img.paste(shot, (40, 112))
    draw.rectangle((40, 112, 40 + shot.width, 112 + shot.height), outline="#B8C4D2", width=2)
    panel(draw, (950, 112, 1238, 650))
    draw.text((980, 145), "Que se ve", fill=BLUE, font=H2)
    write_text(
        draw,
        (980, 190),
        "Izquierda: precio mediano por rareza.\nDerecha: cartas con mas sets.\nAbajo: marketplace como filtro.\n\nLa pagina no empieza por DAX: empieza por una pregunta.",
        220,
    )
    return img


def slide_question_to_visual() -> Image.Image:
    img, draw = base("Inicio: pregunta -> visual -> medida")
    cards = [
        ("Pregunta 1", "Que rarezas se asocian con precios mas altos?", BLUE),
        ("Visual", "Grafico de barras: rarity_name en eje, precio mediano en valores.", TEAL),
        ("Medida", "Precio Mediano por Rareza: mediana de price filtrada por rareza y marketplace.", AMBER),
    ]
    x = 70
    for title, body, color in cards:
        panel(draw, (x, 145, x + 350, 505), fill=WHITE, outline=color, width=3)
        draw.text((x + 25, 180), title, fill=color, font=H2)
        write_text(draw, (x + 25, 240), body, 285, fnt=BODY)
        x += 410
    draw.line((255, 325, 480, 325), fill=MUTED, width=4)
    draw.polygon([(480, 325), (462, 315), (462, 335)], fill=MUTED)
    draw.line((665, 325, 890, 325), fill=MUTED, width=4)
    draw.polygon([(890, 325), (872, 315), (872, 335)], fill=MUTED)
    write_text(
        draw,
        (85, 575),
        "Regla: el visual decide el contexto; la medida decide el calculo dentro de ese contexto.",
        1050,
        fnt=H2,
        fill=INK,
    )
    return img


def table_card(draw, box, name, grain, columns, color):
    x1, y1, x2, y2 = box
    panel(draw, box, fill=WHITE, outline=color, width=3)
    draw.rectangle((x1, y1, x2, y1 + 48), fill=color)
    draw.text((x1 + 16, y1 + 13), name, fill=WHITE, font=H3)
    draw.text((x1 + 16, y1 + 62), f"Grano: {grain}", fill=INK, font=SMALL)
    y = y1 + 95
    for col, note in columns:
        draw.text((x1 + 18, y), col, fill=BLUE, font=SMALL)
        write_text(draw, (x1 + 170, y), note, x2 - x1 - 195, fill=MUTED, fnt=TINY, gap=3)
        y += 43


def slide_prices_table() -> Image.Image:
    img, draw = base("Tabla 1: precios actuales")
    table_card(
        draw,
        (55, 125, 630, 620),
        "vw_fact_card_prices_descriptive",
        "1 carta + 1 marketplace + 1 moneda",
        [
            ("card_id", "clave para conectar con cartas"),
            ("card_name", "etiqueta legible"),
            ("marketplace", "campo del slicer"),
            ("currency", "control para no mezclar EUR y USD"),
            ("price", "valor numerico de la medida"),
        ],
        BLUE,
    )
    panel(draw, (690, 150, 1215, 570), fill="#EFF6FF")
    draw.text((720, 185), "Tratamiento", fill=BLUE, font=H2)
    write_text(
        draw,
        (720, 235),
        "La vista convierte columnas de precio en filas con UNION ALL. Asi Power BI filtra por marketplace y mantiene la moneda declarada.",
        430,
    )
    draw.text((720, 365), "Medidas naturales", fill=BLUE, font=H3)
    write_text(draw, (720, 405), "MEDIAN(price)\nAVERAGE(price)\nCOUNTROWS(precios validos)", 430, fnt=MONO)
    return img


def slide_appearances_table() -> Image.Image:
    img, draw = base("Tabla 2: apariciones carta-set-rareza")
    table_card(
        draw,
        (55, 125, 665, 640),
        "vw_fact_card_set_appearances",
        "1 aparicion de carta en set con rareza",
        [
            ("card_id", "puente hacia precios por carta"),
            ("set_id", "set donde aparece"),
            ("rarity_id", "puente hacia dimension de rarezas"),
            ("rarity_name", "etiqueta de rareza"),
            ("set_price", "precio del set, no de la rareza"),
            ("appearance_count", "vale 1 para contar apariciones"),
        ],
        TEAL,
    )
    panel(draw, (720, 150, 1215, 570), fill="#ECFDF5")
    draw.text((750, 185), "Tratamiento", fill=TEAL, font=H2)
    write_text(
        draw,
        (750, 235),
        "Esta tabla explica presencia: reimpresiones, disponibilidad y combinacion carta-set-rareza. No debe usarse set_price como precio directo de la rareza.",
        400,
    )
    draw.text((750, 395), "Medidas naturales", fill=TEAL, font=H3)
    write_text(draw, (750, 435), "SUM(appearance_count)\nDISTINCTCOUNT(set_id)", 400, fnt=MONO)
    return img


def slide_dimensions() -> Image.Image:
    img, draw = base("Dimensiones: lo que agrupa y filtra")
    table_card(
        draw,
        (60, 130, 600, 585),
        "vw_dim_rarities_descriptive",
        "1 rareza por codigo de impresion",
        [
            ("rarity_id", "clave de relacion"),
            ("rarity_name", "eje del grafico de rarezas"),
            ("rarity_code", "detalle tecnico"),
            ("business_key", "control de unicidad"),
        ],
        PURPLE,
    )
    table_card(
        draw,
        (680, 130, 1220, 585),
        "vw_dim_cards_descriptive",
        "1 carta",
        [
            ("card_id", "clave comun a hechos"),
            ("name", "nombre de carta"),
            ("card_type", "segmentacion"),
            ("atk/def/level", "atributos descriptivos"),
        ],
        BLUE,
    )
    draw.text((80, 635), "Las dimensiones no calculan: dan contexto para que la medida calcule.", fill=INK, font=H2)
    return img


def slide_relationships() -> Image.Image:
    img, draw = base("Relaciones: antes de escribir la medida")
    boxes = {
        "cards": (80, 170, 340, 260, "dim_cards\ncard_id"),
        "prices": (500, 120, 820, 230, "fact_prices\ncard_id, marketplace, price"),
        "appear": (500, 330, 820, 450, "fact_appearances\ncard_id, set_id, rarity_id"),
        "rarity": (930, 330, 1190, 450, "dim_rarities\nrarity_id"),
        "market": (930, 120, 1190, 230, "marketplace\nslicer"),
    }
    for key, (x1, y1, x2, y2, label) in boxes.items():
        color = TEAL if key == "appear" else BLUE
        if key == "rarity":
            color = PURPLE
        if key == "market":
            color = AMBER
        panel(draw, (x1, y1, x2, y2), fill=WHITE, outline=color, width=3)
        write_text(draw, (x1 + 18, y1 + 25), label, x2 - x1 - 35, fnt=H3 if key in ("cards", "rarity") else BODY)
    def arrow(a, b, color=MUTED):
        draw.line((a[0], a[1], b[0], b[1]), fill=color, width=4)
        draw.polygon([(b[0], b[1]), (b[0] - 14, b[1] - 8), (b[0] - 14, b[1] + 8)], fill=color)
    arrow((340, 215), (500, 175), BLUE)
    arrow((340, 215), (500, 390), BLUE)
    arrow((930, 390), (820, 390), PURPLE)
    arrow((930, 175), (820, 175), AMBER)
    panel(draw, (85, 520, 1195, 645), fill="#FFF7E8", outline=AMBER)
    write_text(
        draw,
        (115, 545),
        "Alerta: rarity filtra appearances. Para calcular precios por rareza, la medida debe llevar las cartas de appearances hacia prices. No conviene conectar hechos entre si sin control.",
        1010,
        fnt=H2,
        fill=INK,
    )
    return img


def slide_measure_rarity() -> Image.Image:
    img, draw = base("Medida 1: Precio Mediano por Rareza")
    panel(draw, (55, 120, 620, 635), fill=WHITE, outline=BLUE, width=3)
    draw.text((85, 155), "Intencion", fill=BLUE, font=H2)
    write_text(
        draw,
        (85, 205),
        "Para cada rareza del eje, buscar las cartas que tienen esa rareza en apariciones y calcular la mediana de sus precios en el marketplace filtrado.",
        470,
    )
    draw.text((85, 360), "Por que mediana", fill=BLUE, font=H3)
    write_text(draw, (85, 400), "Reduce el efecto de precios extremos. Es mejor para diagnostico que promedio cuando hay outliers.", 470)

    panel(draw, (680, 120, 1225, 635), fill="#F8FAFC", outline=GRID)
    draw.text((710, 155), "DAX recomendado", fill=BLUE, font=H2)
    dax = (
        "Precio Mediano por Rareza =\n"
        "VAR CartasRareza =\n"
        "    VALUES(vw_fact_card_set_appearances[card_id])\n"
        "RETURN\n"
        "    CALCULATE(\n"
        "        MEDIAN(vw_fact_card_prices_descriptive[price]),\n"
        "        TREATAS(CartasRareza,\n"
        "            vw_fact_card_prices_descriptive[card_id])\n"
        "    )"
    )
    y = 210
    for line in dax.splitlines():
        draw.text((710, y), line, fill=INK, font=MONO)
        y += 25
    write_text(draw, (710, 555), "El slicer marketplace sigue filtrando la tabla de precios.", 455, fnt=SMALL, fill=MUTED)
    return img


def slide_measure_sets() -> Image.Image:
    img, draw = base("Medidas 2 y 3: presencia en sets")
    panel(draw, (60, 130, 575, 610), fill=WHITE, outline=TEAL, width=3)
    draw.text((90, 165), "Sets Distintos por Carta", fill=TEAL, font=H2)
    write_text(draw, (90, 220), "Cuenta cuantos sets diferentes tiene cada carta. Sirve para detectar reimpresion o presencia historica.", 420)
    draw.text((90, 365), "DAX", fill=TEAL, font=H3)
    write_text(
        draw,
        (90, 405),
        "Sets Distintos por Carta =\nDISTINCTCOUNT(vw_fact_card_set_appearances[set_id])",
        420,
        fnt=MONO,
    )
    panel(draw, (705, 130, 1220, 610), fill=WHITE, outline=AMBER, width=3)
    draw.text((735, 165), "Apariciones en Sets", fill=AMBER, font=H2)
    write_text(draw, (735, 220), "Cuenta filas de aparicion. Puede ser mayor que sets distintos si hay codigos, variantes o rarezas repetidas.", 420)
    draw.text((735, 365), "DAX", fill=AMBER, font=H3)
    write_text(
        draw,
        (735, 405),
        "Apariciones en Sets =\nSUM(vw_fact_card_set_appearances[appearance_count])",
        420,
        fnt=MONO,
    )
    return img


def slide_visual_build() -> Image.Image:
    img, draw = base("Como montar los visuales")
    rows = [
        ("Precio por rareza", "Eje", "rarity_name", "dim_rarities"),
        ("Precio por rareza", "Valores", "Precio Mediano por Rareza", "_Medidas_analisis_diagnostico"),
        ("Presencia por carta", "Eje", "card_name", "fact_card_set_appearances"),
        ("Presencia por carta", "Valores", "Sets Distintos por Carta", "_Medidas_analisis_diagnostico"),
        ("Presencia por carta", "Tooltip", "Apariciones en Sets", "_Medidas_analisis_diagnostico"),
        ("Filtro", "Slicer", "marketplace", "fact_card_prices_descriptive"),
    ]
    x0, y0 = 70, 130
    colw = [250, 150, 330, 380]
    headers = ["Visual", "Zona", "Campo / medida", "Tabla"]
    x = x0
    for i, h in enumerate(headers):
        draw.rectangle((x, y0, x + colw[i], y0 + 46), fill=BLUE)
        draw.text((x + 12, y0 + 13), h, fill=WHITE, font=SMALL)
        x += colw[i]
    y = y0 + 46
    for idx, row in enumerate(rows):
        x = x0
        fill = WHITE if idx % 2 == 0 else "#EEF3F8"
        for i, cell in enumerate(row):
            draw.rectangle((x, y, x + colw[i], y + 58), fill=fill, outline=GRID)
            write_text(draw, (x + 12, y + 14), cell, colw[i] - 24, fnt=SMALL, fill=INK)
            x += colw[i]
        y += 58
    panel(draw, (80, 575, 1200, 650), fill="#ECFDF5", outline=TEAL)
    draw.text((110, 598), "La tabla de medidas centraliza el calculo; las tablas de datos aportan contexto y grano.", fill=INK, font=H3)
    return img


def slide_decision_rules() -> Image.Image:
    img, draw = base("Reglas para saber que medida usar")
    rules = [
        ("Si preguntas por valor", "usa price y una agregacion: mediana, promedio, maximo."),
        ("Si preguntas por presencia", "usa appearance_count o DISTINCTCOUNT(set_id)."),
        ("Si cruzas rareza con precio", "necesitas puente por card_id; TREATAS evita un cruce ambiguo."),
        ("Si hay marketplace", "filtra siempre la fuente y conserva currency."),
        ("Si hay ranking", "tratalo como diagnostico, no como recomendacion final."),
    ]
    y = 120
    for title, body in rules:
        panel(draw, (70, y, 1210, y + 85), fill=WHITE, outline=GRID)
        draw.rectangle((70, y, 88, y + 85), fill=TEAL)
        draw.text((115, y + 17), title, fill=BLUE, font=H3)
        draw.text((115, y + 48), body, fill=INK, font=BODY)
        y += 103
    return img


def slide_close() -> Image.Image:
    img = Image.new("RGB", (W, H), "#102A43")
    draw = ImageDraw.Draw(img)
    draw.text((58, 70), "Marco reusable", fill=WHITE, font=TITLE)
    write_text(
        draw,
        (70, 160),
        "Para cualquier pagina Power BI: define la pregunta, identifica el grano de la tabla, elige columnas de contexto, confirma relaciones y solo entonces escribe la medida.",
        1050,
        fill=WHITE,
        fnt=H2,
        gap=10,
    )
    panel(draw, (80, 500, 1200, 610), fill="#EAF4FF", outline="#EAF4FF")
    write_text(
        draw,
        (110, 530),
        "Pagina 03: rareza explica categoria, appearances explica presencia, prices calcula valor y marketplace limita el contexto.",
        1000,
        fnt=H3,
        fill=INK,
    )
    return img


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "video_proceso_analaisis" / "analsis_descriptivo").mkdir(
        parents=True,
        exist_ok=True,
    )
    slides = [
        slide_cover(),
        slide_real_page(),
        slide_question_to_visual(),
        slide_prices_table(),
        slide_appearances_table(),
        slide_dimensions(),
        slide_relationships(),
        slide_measure_rarity(),
        slide_measure_sets(),
        slide_visual_build(),
        slide_decision_rules(),
        slide_close(),
    ]
    durations = [2600, 3200, 3200, 5200, 5200, 4200, 5600, 7200, 5200, 6200, 5200, 4200]
    from moviepy import ImageSequenceClip

    with TemporaryDirectory(prefix="video_frames_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        frame_files = []
        for idx, slide in enumerate(slides, 1):
            frame_path = tmp_path / f"frame_{idx:02d}.png"
            slide.save(frame_path)
            frame_files.append(str(frame_path))
        clip = ImageSequenceClip(
            frame_files,
            durations=[duration / 1000 for duration in durations],
        )
        clip.write_videofile(
            str(MP4_PATH),
            fps=24,
            codec="libx264",
            audio=False,
            logger=None,
        )
        clip.close()
    print(MP4_PATH)


if __name__ == "__main__":
    build()
