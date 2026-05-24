from pathlib import Path
import re


VALID_IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def quote_identifier(identifier: str) -> str:
    if not VALID_IDENTIFIER.match(identifier):
        raise ValueError(f"Identificador SQL no valido: {identifier!r}")

    return f"`{identifier}`"


def build_create_staging_table_sql(table_name: str, columns: list[str]) -> str:
    column_lines = ",\n".join(
        f"    {quote_identifier(column)} TEXT" for column in columns
    )

    return (
        f"CREATE TABLE IF NOT EXISTS {quote_identifier(table_name)} (\n"
        f"{column_lines}\n"
        ");"
    )


def build_create_view_sql(view_name: str, staging_table: str, columns: list[str]) -> str:
    select_lines = ",\n".join(
        f"    {quote_identifier(column)}" for column in columns
    )

    return (
        f"CREATE OR REPLACE VIEW {quote_identifier(view_name)} AS\n"
        "SELECT\n"
        f"{select_lines}\n"
        f"FROM {quote_identifier(staging_table)};"
    )


def build_script(
    csv_path: Path,
    staging_table: str,
    view_name: str,
    columns: list[str],
) -> str:
    return "\n\n".join(
        [
            "-- Generated from exported analytical CSV.",
            f"-- Source CSV: {csv_path.name}",
            build_create_staging_table_sql(staging_table, columns),
            build_create_view_sql(view_name, staging_table, columns),
        ]
    ) + "\n"
