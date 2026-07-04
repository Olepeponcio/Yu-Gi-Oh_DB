from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[3]
OUT_DIR = PROJECT_ROOT / "power_bi" / "informes"
OUT_PATH = OUT_DIR / "informe_analisis_resultados_powerbi_yugioh.docx"

PAGE_GENERAL = BASE_DIR / "01_vista_general"
PAGE_DESCRIPTIVE = BASE_DIR / "02_analisis_descriptivo"
PAGE_DIAGNOSTIC = BASE_DIR / "03_analisis_diagnostico"

BLUE = "2E74B5"
DARK_BLUE = "1F4D78"
LIGHT_GRAY = "F2F4F7"
LIGHT_BLUE = "E8EEF5"
BORDER = "D9E2EC"
MUTED = "666666"


def clean_number(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    text = text.replace("\xa0", " ")
    text = re.sub(r"[^0-9,.\-]", "", text)
    if not text:
        return None
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def fmt_number(value, decimals=0):
    if value is None or pd.isna(value):
        return "n/d"
    return f"{float(value):,.{decimals}f}"


def fmt_money(value, decimals=2, symbol="$"):
    if value is None or pd.isna(value):
        return "n/d"
    return f"{symbol}{float(value):,.{decimals}f}"


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = cell._tc.get_or_add_tcPr().find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_borders(cell, color: str = BORDER, size: str = "6") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        tag = f"w:{edge}"
        node = borders.find(qn(tag))
        if node is None:
            node = OxmlElement(tag)
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, value in {"top": top, "start": start, "bottom": bottom, "end": end}.items():
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_width(table, width_dxa: int = 9360, indent_dxa: int = 120) -> None:
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(width_dxa))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent_dxa))
    tbl_ind.set(qn("w:type"), "dxa")


def style_table(table, widths: list[int] | None = None, header_fill=LIGHT_GRAY) -> None:
    set_table_width(table)
    table.autofit = False
    for row_idx, row in enumerate(table.rows):
        if row_idx == 0:
            tr_pr = row._tr.get_or_add_trPr()
            tbl_header = tr_pr.find(qn("w:tblHeader"))
            if tbl_header is None:
                tbl_header = OxmlElement("w:tblHeader")
                tr_pr.append(tbl_header)
            tbl_header.set(qn("w:val"), "true")
        for cell_idx, cell in enumerate(row.cells):
            if widths:
                cell.width = Inches(widths[cell_idx] / 1440)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_borders(cell)
            set_cell_margins(cell)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.05
                for run in paragraph.runs:
                    run.font.size = Pt(9)
            if row_idx == 0:
                set_cell_shading(cell, header_fill)
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
                        run.font.color.rgb = RGBColor.from_string(DARK_BLUE)


def add_matrix(doc: Document, headers: list[str], rows: Iterable[Iterable[str]], widths: list[int]) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    for idx, header in enumerate(headers):
        table.cell(0, idx).text = header
    for row in rows:
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            cells[idx].text = str(value)
    style_table(table, widths)


def add_callout(doc: Document, text: str, fill: str = "F8FAFC") -> None:
    table = doc.add_table(rows=1, cols=1)
    table.cell(0, 0).text = text
    style_table(table, [9360], header_fill=fill)
    set_cell_shading(table.cell(0, 0), fill)


def configure_doc(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10

    for name, size, color, before, after in [
        ("Title", 24, DARK_BLUE, 0, 6),
        ("Heading 1", 16, BLUE, 16, 8),
        ("Heading 2", 13, BLUE, 12, 6),
        ("Heading 3", 12, DARK_BLUE, 8, 4),
    ]:
        style = styles[name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def add_footer(doc: Document) -> None:
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run("Informe de resultados Power BI - Yu-Gi-Oh!")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor.from_string(MUTED)


def add_image_if_exists(doc: Document, image_path: Path, caption: str) -> None:
    if not image_path.exists():
        return
    doc.add_picture(str(image_path), width=Inches(6.3))
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor.from_string(MUTED)


def get_scalar(df: pd.DataFrame, column: str):
    return df.iloc[0][column]


def load_data() -> dict[str, pd.DataFrame]:
    return {
        "vol_cards": read_csv(PAGE_GENERAL / "Volumen de Cartas.csv"),
        "vol_sets": read_csv(PAGE_GENERAL / "Volumen de Sets.csv"),
        "rarities": read_csv(PAGE_GENERAL / "Rarezas.csv"),
        "snapshots": read_csv(PAGE_GENERAL / "Total Snapshots.csv"),
        "last_snapshot": read_csv(PAGE_GENERAL / "Ultimo Snapshot.csv"),
        "marketplaces": read_csv(PAGE_GENERAL / "Marketplaces.csv"),
        "market_avg": read_csv(PAGE_DESCRIPTIVE / "Precio medio global por Marketplace USD.csv"),
        "card_prices": read_csv(PAGE_DESCRIPTIVE / "Precio medio de mercado USD.csv"),
        "card_market_rank": read_csv(PAGE_DESCRIPTIVE / "cartas mayor precio medio marketplace.csv"),
        "set_values": read_csv(PAGE_DESCRIPTIVE / "Valor Mercado Set por set_name.csv"),
        "rarity_median": read_csv(PAGE_DIAGNOSTIC / "Precio Mediana por rareza.csv"),
        "card_sets": read_csv(PAGE_DIAGNOSTIC / "Sets Distintos por Carta y Apariciones en Sets por card_name.csv"),
        "diagnostic_marketplaces": read_csv(PAGE_DIAGNOSTIC / "marketplace.csv"),
    }


def prepare_data(data: dict[str, pd.DataFrame]) -> None:
    data["market_avg"]["Promedio de price_num"] = data["market_avg"]["Promedio de price"].map(clean_number)
    data["card_prices"]["Precio medio_num"] = data["card_prices"]["Precio medio"].map(clean_number)
    for col in ["Precio Amazon", "Precio CoolStuffInc", "Precio eBay", "Precio TCGplayer"]:
        if col in data["card_prices"].columns:
            data["card_prices"][col + "_num"] = data["card_prices"][col].map(clean_number)
    data["card_market_rank"]["Precio medio marketplace USD_num"] = data["card_market_rank"][
        "Precio medio marketplace USD"
    ].map(clean_number)
    data["set_values"]["Valor Mercado Set_num"] = data["set_values"]["Valor Mercado Set"].map(clean_number)
    data["rarity_median"]["Precio Mediano por Rareza_num"] = data["rarity_median"][
        "Precio Mediano por Rareza"
    ].map(clean_number)


def add_cover(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("Informe de resultados del analisis Power BI")
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Proyecto SQL DB Yu-Gi-Oh | Resultados exportados de visuales")
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.add_paragraph()
    add_matrix(
        doc,
        ["Elemento", "Valor"],
        [
            ["Documento", "Informe de analisis y resultados"],
            ["Fuente", "CSV exportados desde paginas 01, 02 y 03 del PBIX"],
            ["Salida", str(OUT_PATH.relative_to(PROJECT_ROOT))],
            ["Fecha de generacion", datetime.now().strftime("%Y-%m-%d %H:%M")],
            ["Ultimo snapshot", str(get_scalar(data["last_snapshot"], "Ultimo snapshot"))],
        ],
        [2600, 6760],
    )


def add_executive_summary(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    cards = int(get_scalar(data["vol_cards"], "Volumen de cartas"))
    sets = int(get_scalar(data["vol_sets"], "Volumen de sets"))
    rarity_rows = int(get_scalar(data["rarities"], "Volumen de rarezas"))
    rarity_names = int(get_scalar(data["rarities"], "Nombres de rareza"))
    snapshots = int(get_scalar(data["snapshots"], "Total snapshots"))
    top_market = data["market_avg"].sort_values("Promedio de price_num", ascending=False).iloc[0]
    top_card = data["card_prices"].sort_values("Precio medio_num", ascending=False).iloc[0]
    top_rarity = data["rarity_median"].sort_values("Precio Mediano por Rareza_num", ascending=False).iloc[0]
    top_presence = data["card_sets"].sort_values("Sets Distintos por Carta", ascending=False).iloc[0]

    doc.add_heading("1. Resumen ejecutivo", level=1)
    add_callout(
        doc,
        "Hallazgo central: el modelo ya permite separar tres lecturas: cobertura general del catalogo, "
        "valor descriptivo por carta/marketplace/set y diagnostico por rareza o presencia en sets.",
        "EAF3FF",
    )
    add_matrix(
        doc,
        ["Indicador", "Resultado", "Lectura"],
        [
            ["Cartas", fmt_number(cards), "Catalogo amplio; suficiente para rankings y segmentaciones."],
            ["Sets", fmt_number(sets), "Base amplia para analizar reimpresiones y valor por set."],
            ["Rarezas tecnicas", fmt_number(rarity_rows), f"Agrupadas en {rarity_names} nombres de rareza."],
            ["Snapshots", fmt_number(snapshots), "Hay base inicial para historico, aunque debe validarse granularidad temporal."],
            [
                "Marketplace con mayor precio medio",
                f"{top_market['marketplace_name']} ({fmt_money(top_market['Promedio de price_num'])})",
                "Senal descriptiva; no implica mejor oportunidad.",
            ],
            [
                "Carta con mayor precio medio",
                f"{top_card['name']} ({fmt_money(top_card['Precio medio_num'])})",
                "Candidata a revision por posible outlier o carta premio.",
            ],
            [
                "Rareza con mayor mediana",
                f"{top_rarity['rarity_name']} ({fmt_money(top_rarity['Precio Mediano por Rareza_num'])})",
                "Senal diagnostica de rarezas asociadas a precios superiores.",
            ],
            [
                "Carta con mas sets",
                f"{top_presence['card_name']} ({int(top_presence['Sets Distintos por Carta'])} sets)",
                "Presencia alta: reimpresion, popularidad o disponibilidad historica.",
            ],
        ],
        [2300, 2600, 4460],
    )


def add_methodology(doc: Document) -> None:
    doc.add_heading("2. Fuente y metodologia", level=1)
    doc.add_paragraph(
        "Este informe usa los CSV exportados desde los visuales de Power BI. Por tanto, analiza el resultado "
        "observado en el dashboard, no reconstruye el modelo completo desde MySQL. La lectura mantiene la "
        "secuencia: visual, dato observado, interpretacion, decision o cautela."
    )
    add_matrix(
        doc,
        ["Pagina", "Recursos usados", "Finalidad"],
        [
            ["01_vista_general", "CSV de tarjetas, marketplaces, rarezas y captura PNG", "Describir cobertura del modelo."],
            ["02_analisis_descriptivo", "CSV de precios, rankings y valor por set; captura PNG", "Identificar concentraciones de valor."],
            ["03_analisis_diagnostico", "CSV de rarezas, sets por carta y marketplace; captura PNG", "Explicar posibles causas o patrones."],
        ],
        [1900, 3960, 3500],
    )


def add_general_view(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("3. Vista general", level=1)
    add_image_if_exists(doc, PAGE_GENERAL / "01_vista_general.png", "Captura de la pagina 01_vista_general.")
    cards = int(get_scalar(data["vol_cards"], "Volumen de cartas"))
    sets = int(get_scalar(data["vol_sets"], "Volumen de sets"))
    rarity_rows = int(get_scalar(data["rarities"], "Volumen de rarezas"))
    rarity_names = int(get_scalar(data["rarities"], "Nombres de rareza"))
    snapshots = int(get_scalar(data["snapshots"], "Total snapshots"))
    latest = str(get_scalar(data["last_snapshot"], "Ultimo snapshot"))
    doc.add_heading("3.1 Datos observados", level=2)
    add_matrix(
        doc,
        ["Metrica", "Valor"],
        [
            ["Volumen de cartas", fmt_number(cards)],
            ["Volumen de sets", fmt_number(sets)],
            ["Filas tecnicas de rareza", fmt_number(rarity_rows)],
            ["Nombres de rareza", fmt_number(rarity_names)],
            ["Total snapshots", fmt_number(snapshots)],
            ["Ultimo snapshot", latest],
        ],
        [3600, 5760],
    )
    doc.add_heading("3.2 Interpretacion", level=2)
    doc.add_paragraph(
        f"El modelo contiene {fmt_number(cards)} cartas y {fmt_number(sets)} sets, volumen suficiente para "
        "analisis de catalogo, precios y reimpresiones. La diferencia entre filas tecnicas de rareza "
        f"({fmt_number(rarity_rows)}) y nombres de rareza ({fmt_number(rarity_names)}) indica que la rareza "
        "debe tratarse con grano controlado: una etiqueta puede repetirse por set, codigo o aparicion."
    )
    doc.add_paragraph(
        f"El historico muestra {fmt_number(snapshots)} snapshots y ultimo corte {latest}. Esto permite iniciar "
        "lecturas temporales, pero todavia exige cautela antes de hablar de tendencia robusta."
    )
    doc.add_heading("3.3 Marketplaces", level=2)
    add_matrix(
        doc,
        ["Marketplace", "Region", "Moneda"],
        data["marketplaces"].astype(str).values.tolist(),
        [2800, 3280, 3280],
    )
    add_callout(
        doc,
        "Decision de lectura: no mezclar Cardmarket con fuentes USD sin conversion. El informe de resultados "
        "de precios descriptivos se centra en USD cuando el visual asi lo exporta.",
        "FFF6E5",
    )


def add_descriptive_analysis(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("4. Analisis descriptivo", level=1)
    add_image_if_exists(doc, PAGE_DESCRIPTIVE / "02_analisis_descriptivo.png", "Captura de la pagina 02_Analisis_descriptivo.")

    doc.add_heading("4.1 Precio medio global por marketplace", level=2)
    market_rows = []
    for _, row in data["market_avg"].sort_values("Promedio de price_num", ascending=False).iterrows():
        market_rows.append([row["marketplace_name"], fmt_money(row["Promedio de price_num"])])
    add_matrix(doc, ["Marketplace", "Precio medio USD"], market_rows, [4200, 5160])
    leader = data["market_avg"].sort_values("Promedio de price_num", ascending=False).iloc[0]
    doc.add_paragraph(
        f"{leader['marketplace_name']} lidera el precio medio global exportado con "
        f"{fmt_money(leader['Promedio de price_num'])}. La lectura es descriptiva: indica mayor precio medio "
        "en el conjunto filtrado, no una decision de compra."
    )

    doc.add_heading("4.2 Cartas con mayor precio medio", level=2)
    top_cards = data["card_prices"].sort_values("Precio medio_num", ascending=False).head(10)
    rows = [
        [r["name"], fmt_money(r["Precio medio_num"]), fmt_money(clean_number(r.get("Precio eBay"))), fmt_money(clean_number(r.get("Precio TCGplayer")))]
        for _, r in top_cards.iterrows()
    ]
    add_matrix(doc, ["Carta", "Precio medio", "eBay", "TCGplayer"], rows, [3400, 1900, 1900, 2160])
    top = top_cards.iloc[0]
    doc.add_paragraph(
        f"La carta con mayor precio medio es {top['name']} ({fmt_money(top['Precio medio_num'])}). "
        "El ranking concentra cartas con precios extremos, por lo que debe usarse como lista de revision y no "
        "como recomendacion automatica."
    )

    doc.add_heading("4.3 Ranking carta-marketplace", level=2)
    top_market_cards = data["card_market_rank"].sort_values("Precio medio marketplace USD_num", ascending=False).head(8)
    add_matrix(
        doc,
        ["Carta", "Marketplace", "Precio medio USD"],
        [
            [r["card_name"], r["marketplace"], fmt_money(r["Precio medio marketplace USD_num"])]
            for _, r in top_market_cards.iterrows()
        ],
        [4300, 2300, 2760],
    )
    doc.add_paragraph(
        "El ranking por carta-marketplace muestra que un mismo nombre puede destacar en fuentes distintas. "
        "Esto refuerza la necesidad de revisar fuente, cobertura y posibles outliers antes de comparar cartas."
    )

    doc.add_heading("4.4 Valor de mercado por set", level=2)
    top_sets = data["set_values"].sort_values("Valor Mercado Set_num", ascending=False).head(8)
    add_matrix(
        doc,
        ["Set", "Valor mercado"],
        [[r["set_name"], fmt_money(r["Valor Mercado Set_num"])] for _, r in top_sets.iterrows()],
        [6200, 3160],
    )
    top_set = top_sets.iloc[0]
    doc.add_paragraph(
        f"El set con mayor valor exportado es {top_set['set_name']} "
        f"({fmt_money(top_set['Valor Mercado Set_num'])}). La concentracion en sets premio sugiere que "
        "rareza competitiva, escasez y coleccionismo condicionan fuertemente el valor agregado."
    )


def add_diagnostic_analysis(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("5. Analisis diagnostico", level=1)
    add_image_if_exists(doc, PAGE_DIAGNOSTIC / "03_analisis_diagnostico.png", "Captura de la pagina 03_Analisis_diagnostico.")

    doc.add_heading("5.1 Precio mediano por rareza", level=2)
    top_rarities = data["rarity_median"].sort_values("Precio Mediano por Rareza_num", ascending=False).head(10)
    add_matrix(
        doc,
        ["Rareza", "Precio mediano"],
        [[r["rarity_name"], fmt_money(r["Precio Mediano por Rareza_num"])] for _, r in top_rarities.iterrows()],
        [6100, 3260],
    )
    first = top_rarities.iloc[0]
    doc.add_paragraph(
        f"{first['rarity_name']} aparece como rareza con mayor mediana "
        f"({fmt_money(first['Precio Mediano por Rareza_num'])}). La mediana reduce el efecto de precios extremos, "
        "por lo que esta lectura es mas estable que un promedio simple para diagnosticar rarezas."
    )
    doc.add_paragraph(
        "La interpretacion prudente es que estas rarezas se asocian con precios superiores en el contexto exportado. "
        "No prueba causalidad: puede intervenir escasez, antiguedad, fuente de precio, carta concreta o baja cobertura."
    )

    doc.add_heading("5.2 Sets distintos y apariciones por carta", level=2)
    top_presence = data["card_sets"].sort_values("Sets Distintos por Carta", ascending=False).head(10)
    add_matrix(
        doc,
        ["Carta", "Sets distintos", "Apariciones"],
        [
            [r["card_name"], str(int(r["Sets Distintos por Carta"])), str(int(r["Apariciones en Sets"]))]
            for _, r in top_presence.iterrows()
        ],
        [5100, 2100, 2160],
    )
    leader = top_presence.iloc[0]
    doc.add_paragraph(
        f"{leader['card_name']} lidera presencia con {int(leader['Sets Distintos por Carta'])} sets distintos "
        f"y {int(leader['Apariciones en Sets'])} apariciones. Esta senal explica disponibilidad historica, "
        "reimpresion o popularidad; no mide valor por si sola."
    )

    doc.add_heading("5.3 Preguntas respondidas", level=2)
    add_matrix(
        doc,
        ["Pregunta", "Respuesta basada en CSV", "Decision / cautela"],
        [
            [
                "Que rarezas se asocian con precios mas altos?",
                f"Lidera {first['rarity_name']} con mediana {fmt_money(first['Precio Mediano por Rareza_num'])}.",
                "Usar como hipotesis diagnostica; validar cobertura por rareza.",
            ],
            [
                "Que cartas aparecen en mas sets?",
                f"Lidera {leader['card_name']} con {int(leader['Sets Distintos por Carta'])} sets.",
                "Interpretar como presencia/reimpresion, no como recomendacion.",
            ],
            [
                "Como afecta marketplace?",
                "El visual incluye slicer con amazon, cardmarket, coolstuffinc, ebay y tcgplayer.",
                "Mantener fuente y moneda antes de comparar precios.",
            ],
        ],
        [2600, 3860, 2900],
    )


def add_decisions(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("6. Decisiones, hipotesis y siguientes validaciones", level=1)
    top_card = data["card_prices"].sort_values("Precio medio_num", ascending=False).iloc[0]
    top_set = data["set_values"].sort_values("Valor Mercado Set_num", ascending=False).iloc[0]
    add_matrix(
        doc,
        ["Linea de accion", "Base observada", "Siguiente validacion"],
        [
            [
                "Revisar outliers de precio",
                f"{top_card['name']} encabeza precio medio con {fmt_money(top_card['Precio medio_num'])}.",
                "Contrastar precio por marketplace, moneda y cobertura.",
            ],
            [
                "Profundizar en sets premio",
                f"{top_set['set_name']} lidera valor agregado.",
                "Separar precio de carta, precio de set y numero de apariciones.",
            ],
            [
                "Validar rarezas caras",
                "Las primeras rarezas por mediana muestran precios superiores.",
                "Medir numero de cartas por rareza antes de concluir.",
            ],
            [
                "Usar presencia como contexto",
                "Blue-Eyes White Dragon y otras cartas clasicas lideran sets distintos.",
                "Cruzar presencia con precio y tipo de carta.",
            ],
        ],
        [2600, 3900, 2860],
    )
    add_callout(
        doc,
        "Conclusion: el informe identifica senales de valor y presencia, pero las decisiones prescriptivas deben "
        "esperar a validar outliers, moneda, fuente y cobertura de cada visual.",
        "EAF8EE",
    )


def build_doc() -> None:
    data = load_data()
    prepare_data(data)

    doc = Document()
    configure_doc(doc)
    add_footer(doc)

    add_cover(doc, data)
    add_executive_summary(doc, data)
    add_methodology(doc)
    add_general_view(doc, data)
    add_descriptive_analysis(doc, data)
    add_diagnostic_analysis(doc, data)
    add_decisions(doc, data)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_PATH)
    print(OUT_PATH)


if __name__ == "__main__":
    build_doc()
