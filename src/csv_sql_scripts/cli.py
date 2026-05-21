import argparse
from pathlib import Path

from src.csv_sql_scripts.config import DEFAULT_CSV_DIR, DEFAULT_OUTPUT_DIR
from src.csv_sql_scripts.main import generate_scripts_from_csv_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera scripts SQL de staging/views desde CSV analiticos exportados."
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DEFAULT_CSV_DIR,
        help=f"Directorio origen de CSV. Por defecto: {DEFAULT_CSV_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directorio destino de scripts SQL. Por defecto: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribe scripts SQL existentes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida y muestra lo que se generaria sin escribir archivos.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    generated = generate_scripts_from_csv_dir(
        csv_dir=args.csv_dir,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )

    if not generated:
        print(f"No se encontraron CSV en: {args.csv_dir}")
        return

    action = "Validado" if args.dry_run else "Generado"
    for item in generated:
        target = item.output_path if item.output_path is not None else args.output_dir / f"{item.view_name}.sql"
        print(
            f"{action}: {item.csv_path.name} -> {target} "
            f"({item.staging_table}, {item.view_name}, {len(item.columns)} columnas)"
        )


if __name__ == "__main__":
    main()
