from __future__ import annotations

import re
import unicodedata
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
EXPORT_DIR = PROJECT_ROOT / "power_bi" / "informes" / "exports"
OUT_DIR = PROJECT_ROOT / "power_bi" / "informes"
OUT_PATH = OUT_DIR / "informe_analisis_resultados_powerbi_yugioh.docx"

PAGE_DESCRIPTIVE = EXPORT_DIR / "descriptive"
PAGE_DIAGNOSTIC = EXPORT_DIR / "diagnostic"

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
    text = str(value).strip().replace("\xa0", " ")
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


def fmt_ratio(value):
    if value is None or pd.isna(value):
        return "n/d"
    return f"{float(value):,.2f}x"


def normalize_label(value):
    return str(value).strip().replace("\ufeff", "").replace("ï»¿", "")


def text_key(value):
    text = normalize_label(value).lower()
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [normalize_label(col) for col in df.columns]
    for col in df.columns:
        if not (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])):
            continue
        df[col] = df[col].map(normalize_label)
    return df


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
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


def load_data() -> dict[str, pd.DataFrame]:
    return {
        "top_cards": read_csv(PAGE_DESCRIPTIVE / "data.csv"),
        "market_avg": read_csv(PAGE_DESCRIPTIVE / "Precio medio global por Marketplace USD.csv"),
        "set_values": read_csv(PAGE_DESCRIPTIVE / "Precios por set.csv"),
        "rarity_counts": read_csv(PAGE_DIAGNOSTIC / "Cartas distintas por rareza por rarity_name.csv"),
        "quality_counts": read_csv(PAGE_DIAGNOSTIC / "Cartas distintas por rareza por revision rarity name.csv"),
        "outlier_table": read_csv(PAGE_DIAGNOSTIC / "data.csv"),
        "rarity_table": read_csv(PAGE_DIAGNOSTIC / "tabla_rarezas.csv"),
    }


def prepare_data(data: dict[str, pd.DataFrame]) -> None:
    data["market_avg"]["Promedio de price_num"] = data["market_avg"]["Promedio de price"].map(clean_number)
    data["set_values"]["Suma de set_price_num"] = data["set_values"]["Suma de set_price"].map(clean_number)
    data["top_cards"]["avg_price_USD_num"] = data["top_cards"]["avg_price_USD"].map(clean_number)
    for col in ["cardmarket_usd", "tcgplayer", "ebay", "amazon", "coolstuffinc"]:
        data["top_cards"][col + "_num"] = data["top_cards"][col].map(clean_number)

    data["quality_counts"]["Cartas distintas por rareza_num"] = data["quality_counts"][
        "Cartas distintas por rareza"
    ].map(clean_number)
    data["outlier_table"]["precio max_num"] = data["outlier_table"]["precio max"].map(clean_number)
    data["outlier_table"]["Ratio outlier_num"] = data["outlier_table"]["Ratio outlier"].map(clean_number)

    max_col = [col for col in data["rarity_table"].columns if col.startswith("Precio")][0]
    ratio_col = [col for col in data["rarity_table"].columns if col.startswith("Ratio")][0]
    data["rarity_table"]["precio_max_num"] = data["rarity_table"][max_col].map(clean_number)
    data["rarity_table"]["ratio_num"] = data["rarity_table"][ratio_col].map(clean_number)


def rows_count(df: pd.DataFrame, col: str, value: str) -> float:
    match = df[df[col].map(text_key) == text_key(value)]
    if match.empty:
        return 0
    return float(match.iloc[0]["Cartas distintas por rareza_num"])


def add_cover(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("Informe de resultados del analisis Power BI")
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Proyecto SQL DB Yu-Gi-Oh | Exports descriptivo y diagnostico")
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor.from_string(MUTED)
    doc.add_paragraph()
    add_matrix(
        doc,
        ["Elemento", "Valor"],
        [
            ["Documento", "Informe de analisis y resultados"],
            ["Fuente", str(EXPORT_DIR.relative_to(PROJECT_ROOT))],
            ["Paginas analizadas", "02_analisis_descriptivo y 03_analisis_diagnostico"],
            ["Salida", str(OUT_PATH.relative_to(PROJECT_ROOT))],
            ["Fecha de generacion", datetime.now().strftime("%Y-%m-%d %H:%M")],
        ],
        [2600, 6760],
    )


def add_executive_summary(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    top_market = data["market_avg"].sort_values("Promedio de price_num", ascending=False).iloc[0]
    top_card = data["top_cards"].sort_values("avg_price_USD_num", ascending=False).iloc[0]
    top_set = data["set_values"].sort_values("Suma de set_price_num", ascending=False).iloc[0]
    valid_count = rows_count(data["quality_counts"], "revision rarity name", "Rareza válida")
    suspect_count = data["quality_counts"]["Cartas distintas por rareza_num"].sum() - valid_count
    outliers = data["outlier_table"][data["outlier_table"]["Flag Outlier"].map(text_key) == "si"]
    valid_outliers = outliers[outliers["revision rarity name"].map(text_key) == "rareza valida"]
    critical = data["outlier_table"][data["outlier_table"]["Nivel outlier"].map(text_key) == "critico"]

    doc.add_heading("1. Resumen ejecutivo", level=1)
    add_callout(
        doc,
        "Hallazgo central: los visuales actuales ya separan valor descriptivo, control de categorias de rareza "
        "y deteccion explicita de outliers. La decision de lectura debe partir de rarezas validas y tratar los "
        "precios extremos como candidatos a revision.",
        "EAF3FF",
    )
    add_matrix(
        doc,
        ["Indicador", "Resultado", "Lectura"],
        [
            [
                "Marketplace con mayor precio medio",
                f"{top_market['marketplace_name']} ({fmt_money(top_market['Promedio de price_num'])})",
                "eBay lidera el promedio exportado; puede contener listados altos.",
            ],
            [
                "Carta con mayor precio medio",
                f"{top_card['name']} ({fmt_money(top_card['avg_price_USD_num'])})",
                "Ranking util para revision, no para recomendacion directa.",
            ],
            [
                "Set con mayor valor agregado",
                f"{top_set['set_name']} ({fmt_money(top_set['Suma de set_price_num'], symbol='EUR ')})",
                "El valor se concentra en prize cards y sets promocionales.",
            ],
            [
                "Categorias validas",
                fmt_number(valid_count),
                "Base recomendada para visuales principales.",
            ],
            [
                "Categorias sospechosas",
                fmt_number(suspect_count),
                "Deben quedar en visual de calidad, no en rankings principales.",
            ],
            [
                "Outliers validos",
                fmt_number(len(valid_outliers)),
                "Rarezas validas con precio maximo muy superior a la referencia.",
            ],
            [
                "Outliers criticos",
                fmt_number(len(critical)),
                "Prioridad de auditoria de fuente, moneda y cobertura.",
            ],
        ],
        [2500, 2600, 4260],
    )


def add_methodology(doc: Document) -> None:
    doc.add_heading("2. Fuente y metodologia", level=1)
    doc.add_paragraph(
        "Este informe usa exclusivamente los CSV exportados desde Power BI en la carpeta de exports. No reconstruye "
        "el modelo desde MySQL: interpreta lo que muestran los visuales actuales y documenta las cautelas necesarias."
    )
    add_matrix(
        doc,
        ["Bloque", "CSV usados", "Finalidad"],
        [
            [
                "Analisis descriptivo",
                "data.csv, Precio medio global por Marketplace USD.csv, Precios por set.csv",
                "Identificar cartas, marketplaces y sets con mayor valor observado.",
            ],
            [
                "Analisis diagnostico",
                "data.csv, tabla_rarezas.csv, Cartas distintas por rareza por *.csv",
                "Separar categorias validas, categorias sospechosas y outliers.",
            ],
        ],
        [2100, 4200, 3060],
    )


def add_descriptive_analysis(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("3. Analisis descriptivo", level=1)

    doc.add_heading("3.1 Precio medio global por marketplace", level=2)
    market_rows = [
        [row["marketplace_name"], fmt_money(row["Promedio de price_num"])]
        for _, row in data["market_avg"].sort_values("Promedio de price_num", ascending=False).iterrows()
    ]
    add_matrix(doc, ["Marketplace", "Precio medio USD"], market_rows, [4200, 5160])
    market = data["market_avg"].set_index("marketplace_name")["Promedio de price_num"]
    if "eBay" in market.index and "Cardmarket" in market.index:
        doc.add_paragraph(
            f"eBay promedia {fmt_money(market['eBay'])}, frente a {fmt_money(market['Cardmarket'])} en Cardmarket. "
            f"La relacion es aproximadamente {fmt_number(market['eBay'] / market['Cardmarket'], 2)}x, por lo que "
            "la fuente de precio debe mantenerse visible en cualquier conclusion."
        )

    doc.add_heading("3.2 Cartas con mayor precio medio", level=2)
    top_cards = data["top_cards"].sort_values("avg_price_USD_num", ascending=False).head(10)
    add_matrix(
        doc,
        ["Carta", "Media USD", "eBay", "TCGplayer", "Amazon"],
        [
            [
                r["name"],
                fmt_money(r["avg_price_USD_num"]),
                fmt_money(r["ebay_num"]),
                fmt_money(r["tcgplayer_num"]),
                fmt_money(r["amazon_num"]),
            ]
            for _, r in top_cards.iterrows()
        ],
        [3300, 1500, 1500, 1500, 1560],
    )
    first = top_cards.iloc[0]
    doc.add_paragraph(
        f"{first['name']} encabeza el ranking con {fmt_money(first['avg_price_USD_num'])}. "
        "La tabla muestra que la media puede quedar dominada por un marketplace concreto; por eso debe cruzarse "
        "con el visual diagnostico de outliers antes de interpretar valor real."
    )

    doc.add_heading("3.3 Valor por set", level=2)
    sets = data["set_values"].sort_values("Suma de set_price_num", ascending=False)
    total_top20 = sets["Suma de set_price_num"].sum()
    top1_share = sets.iloc[0]["Suma de set_price_num"] / total_top20
    top2_share = sets.head(2)["Suma de set_price_num"].sum() / total_top20
    top6_share = sets.head(6)["Suma de set_price_num"].sum() / total_top20
    add_matrix(
        doc,
        ["Set", "Valor exportado"],
        [[r["set_name"], fmt_money(r["Suma de set_price_num"], symbol="EUR ")] for _, r in sets.head(8).iterrows()],
        [6500, 2860],
    )
    doc.add_paragraph(
        f"El top 20 de sets suma {fmt_money(total_top20, symbol='EUR ')}. El primer set concentra "
        f"{fmt_number(top1_share * 100, 1)}%, los dos primeros {fmt_number(top2_share * 100, 1)}% y los seis "
        f"primeros {fmt_number(top6_share * 100, 1)}%. La concentracion confirma que los prize cards condicionan "
        "el valor agregado."
    )


def add_diagnostic_analysis(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("4. Analisis diagnostico", level=1)

    doc.add_heading("4.1 Calidad de categorias de rareza", level=2)
    quality = data["quality_counts"].sort_values("Cartas distintas por rareza_num", ascending=False)
    total_quality = quality["Cartas distintas por rareza_num"].sum()
    add_matrix(
        doc,
        ["Revision rarity name", "Cartas distintas", "% del total"],
        [
            [
                r["revision rarity name"],
                fmt_number(r["Cartas distintas por rareza_num"]),
                f"{fmt_number(r['Cartas distintas por rareza_num'] / total_quality * 100, 2)}%",
            ]
            for _, r in quality.iterrows()
        ],
        [4100, 2600, 2660],
    )
    add_callout(
        doc,
        "Decision aplicada: los visuales principales deben filtrar revision rarity name = Rareza valida. Las "
        "categorias Atributo no rareza, Codigo interno / revisar y Error parseo se mantienen como control de calidad.",
        "FFF6E5",
    )

    doc.add_heading("4.2 Outliers por rareza", level=2)
    outliers = data["outlier_table"].sort_values("Ratio outlier_num", ascending=False)
    valid_outliers = outliers[outliers["revision rarity name"].map(text_key) == "rareza valida"].head(12)
    add_matrix(
        doc,
        ["Rareza", "Revision", "Rarezas", "Precio max", "Ratio", "Nivel"],
        [
            [
                r["name"],
                r["revision rarity name"],
                fmt_number(r["rarezas"]),
                fmt_money(r["precio max_num"]),
                fmt_ratio(r["Ratio outlier_num"]),
                r["Nivel outlier"],
            ]
            for _, r in valid_outliers.iterrows()
        ],
        [2300, 1900, 1200, 1400, 1400, 1160],
    )
    lead = valid_outliers.iloc[0]
    doc.add_paragraph(
        f"Entre rarezas validas, {lead['name']} presenta el mayor ratio de outlier "
        f"({fmt_ratio(lead['Ratio outlier_num'])}) con precio maximo {fmt_money(lead['precio max_num'])}. "
        "Esto identifica una anomalia relativa: el precio maximo supera de forma extrema al precio tipico del grupo."
    )

    doc.add_heading("4.3 Rarezas por volumen", level=2)
    rarity_counts = data["rarity_counts"].sort_values("Cartas distintas por rareza", ascending=False)
    total_rarities = rarity_counts["Cartas distintas por rareza"].sum()
    add_matrix(
        doc,
        ["Rareza", "Cartas distintas", "% acumulable"],
        [
            [
                r["rarity_name"],
                fmt_number(r["Cartas distintas por rareza"]),
                f"{fmt_number(r['Cartas distintas por rareza'] / total_rarities * 100, 2)}%",
            ]
            for _, r in rarity_counts.head(10).iterrows()
        ],
        [5200, 2100, 2060],
    )
    top5_share = rarity_counts.head(5)["Cartas distintas por rareza"].sum() / total_rarities
    doc.add_paragraph(
        f"Las cinco rarezas con mas cartas concentran {fmt_number(top5_share * 100, 1)}% del total exportado. "
        "Esto explica que Common, Super Rare y Ultra Rare puedan aparecer con outliers: tienen volumen alto y mas "
        "probabilidad de contener precios extremos."
    )


def add_decisions(doc: Document, data: dict[str, pd.DataFrame]) -> None:
    doc.add_heading("5. Decisiones y siguientes validaciones", level=1)
    top_card = data["top_cards"].sort_values("avg_price_USD_num", ascending=False).iloc[0]
    top_set = data["set_values"].sort_values("Suma de set_price_num", ascending=False).iloc[0]
    top_outlier = data["outlier_table"][
        data["outlier_table"]["revision rarity name"].map(text_key) == "rareza valida"
    ].sort_values("Ratio outlier_num", ascending=False).iloc[0]
    add_matrix(
        doc,
        ["Linea de accion", "Base observada", "Siguiente validacion"],
        [
            [
                "Auditar outliers criticos",
                f"{top_outlier['name']} alcanza {fmt_ratio(top_outlier['Ratio outlier_num'])}.",
                "Revisar carta concreta, marketplace, moneda y si el precio representa venta real o listado.",
            ],
            [
                "Separar categorias sospechosas",
                "La columna revision rarity name ya identifica errores, codigos internos y atributos no rareza.",
                "Mantenerlas fuera de visuales principales y dentro de control de calidad.",
            ],
            [
                "Contrastar rankings descriptivos",
                f"{top_card['name']} lidera precio medio con {fmt_money(top_card['avg_price_USD_num'])}.",
                "Comparar contra mediana, precio maximo y fuente antes de extraer conclusion economica.",
            ],
            [
                "Profundizar en sets premio",
                f"{top_set['set_name']} lidera valor exportado.",
                "Separar valor por carta, numero de apariciones y tipo de set.",
            ],
        ],
        [2500, 3900, 2960],
    )
    add_callout(
        doc,
        "Conclusion: el dashboard ya tiene una rama diagnostica util. El siguiente avance debe ser convertir los "
        "outliers criticos en una tabla de auditoria por carta y marketplace para decidir si se excluyen, se corrigen "
        "o se documentan como casos excepcionales.",
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
    add_descriptive_analysis(doc, data)
    add_diagnostic_analysis(doc, data)
    add_decisions(doc, data)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_PATH)
    print(OUT_PATH)


if __name__ == "__main__":
    build_doc()
