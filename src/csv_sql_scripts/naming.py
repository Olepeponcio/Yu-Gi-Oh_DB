import re
from pathlib import Path

from src.csv_sql_scripts.config import STAGING_PREFIX


VALID_IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def sanitize_identifier(raw_name: str, fallback: str) -> str:
    value = raw_name.strip().lower()
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")

    if not value:
        value = fallback

    if value[0].isdigit():
        value = f"{fallback}_{value}"

    if not VALID_IDENTIFIER.match(value):
        raise ValueError(f"Identificador SQL no valido: {raw_name!r}")

    return value


def unique_identifiers(raw_names: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    identifiers: list[str] = []

    for index, raw_name in enumerate(raw_names, start=1):
        identifier = sanitize_identifier(raw_name, fallback=f"column_{index}")
        count = seen.get(identifier, 0)
        seen[identifier] = count + 1

        if count:
            identifier = f"{identifier}_{count + 1}"

        identifiers.append(identifier)

    return identifiers


def view_name_from_csv(csv_path: Path) -> str:
    name = sanitize_identifier(csv_path.stem, fallback="view")
    if not name.startswith("vw_"):
        name = f"vw_{name}"

    return name


def staging_name_from_view(view_name: str) -> str:
    return f"{STAGING_PREFIX}{view_name}"
