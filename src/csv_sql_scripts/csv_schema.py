import csv
from pathlib import Path


def read_csv_headers(csv_path: Path) -> list[str]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        try:
            headers = next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV vacio: {csv_path}") from exc

    if not headers:
        raise ValueError(f"CSV sin cabecera: {csv_path}")

    return headers

