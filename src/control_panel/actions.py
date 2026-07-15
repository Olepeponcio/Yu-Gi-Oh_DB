from dataclasses import dataclass
from pathlib import Path
import sys

from src.control_panel.theme import BUTTON_COLORS


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_LATEST = PROJECT_ROOT / "data" / "raw" / "cardinfo_latest.json"


@dataclass(frozen=True)
class PanelAction:
    key: str
    label: str
    description: str
    command: tuple[str, ...]
    color: str
    destructive: bool = False
    stores_snapshot: bool = False
    primary: bool = False


def python_module(*arguments):
    return (sys.executable, "-m", *arguments)


def build_actions():
    return (
        PanelAction(
            key="reset_schema",
            label="1. Preparar DB + schema",
            description="Backup histórico, reset de tablas, schema y restauración.",
            command=python_module("src.etl.reset_mysql", "--yes"),
            color=BUTTON_COLORS[0],
            destructive=True,
        ),
        PanelAction(
            key="validate_api",
            label="2. Validar API (dry-run)",
            description="Descarga y transforma sin escribir en MySQL.",
            command=python_module("src.etl", "--dry-run"),
            color=BUTTON_COLORS[1],
        ),
        PanelAction(
            key="etl_api_snapshot",
            label="3. CARGAR API + GUARDAR SNAPSHOT",
            description="Carga tablas madre, inserta snapshot y crea backup histórico.",
            command=python_module("src.etl"),
            color=BUTTON_COLORS[2],
            stores_snapshot=True,
            primary=True,
        ),
        PanelAction(
            key="etl_raw_snapshot",
            label="4. ETL raw + snapshot",
            description="Reprocesa el raw local e inserta un snapshot nuevo.",
            command=python_module(
                "src.etl", "--source", "file", "--raw-path", str(RAW_LATEST)
            ),
            color=BUTTON_COLORS[3],
            stores_snapshot=True,
        ),
        PanelAction(
            key="backup_history",
            label="5. Backup de snapshots",
            description="Exporta card_price_history sin modificar la base.",
            command=python_module("src.etl.history_backup", "backup"),
            color=BUTTON_COLORS[4],
        ),
        PanelAction(
            key="tests",
            label="6. Ejecutar tests",
            description="Valida ETL, claves, calidad, reset y compatibilidad histórica.",
            command=python_module("unittest", "discover", "-v"),
            color=BUTTON_COLORS[5],
        ),
    )
