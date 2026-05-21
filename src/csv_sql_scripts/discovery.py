from pathlib import Path


def find_csv_files(csv_dir: Path) -> list[Path]:
    if not csv_dir.exists():
        raise FileNotFoundError(f"No existe el directorio CSV: {csv_dir}")

    if not csv_dir.is_dir():
        raise NotADirectoryError(f"La ruta CSV no es un directorio: {csv_dir}")

    return sorted(path for path in csv_dir.glob("*.csv") if path.is_file())

