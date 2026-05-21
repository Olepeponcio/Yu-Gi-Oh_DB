from pathlib import Path

from src.csv_sql_scripts.config import SQL_EXTENSION


def write_sql_script(
    output_dir: Path,
    view_name: str,
    sql: str,
    overwrite: bool = False,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{view_name}{SQL_EXTENSION}"

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Ya existe el script SQL: {output_path}. Usa --overwrite para regenerarlo."
        )

    output_path.write_text(sql, encoding="utf-8")
    return output_path
