from dataclasses import dataclass
from pathlib import Path

from src.csv_sql_scripts.csv_schema import read_csv_headers
from src.csv_sql_scripts.discovery import find_csv_files
from src.csv_sql_scripts.naming import (
    staging_name_from_view,
    unique_identifiers,
    view_name_from_csv,
)
from src.csv_sql_scripts.sql_builder import build_script
from src.csv_sql_scripts.writer import write_sql_script


@dataclass(frozen=True)
class GeneratedScript:
    csv_path: Path
    output_path: Path | None
    staging_table: str
    view_name: str
    columns: list[str]


def generate_scripts_from_csv_dir(
    csv_dir: Path,
    output_dir: Path,
    overwrite: bool = False,
    dry_run: bool = False,
) -> list[GeneratedScript]:
    csv_files = find_csv_files(csv_dir)
    generated: list[GeneratedScript] = []

    for csv_path in csv_files:
        raw_headers = read_csv_headers(csv_path)
        columns = unique_identifiers(raw_headers)
        view_name = view_name_from_csv(csv_path)
        staging_table = staging_name_from_view(view_name)
        sql = build_script(csv_path, staging_table, view_name, columns)
        output_path = None

        if not dry_run:
            output_path = write_sql_script(
                output_dir=output_dir,
                view_name=view_name,
                sql=sql,
                overwrite=overwrite,
            )

        generated.append(
            GeneratedScript(
                csv_path=csv_path,
                output_path=output_path,
                staging_table=staging_table,
                view_name=view_name,
                columns=columns,
            )
        )

    return generated
