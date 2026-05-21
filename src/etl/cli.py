import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="Ingesta completa de cartas desde YGOPRODeck hacia MySQL."
    )
    parser.add_argument(
        "--source",
        choices=("api", "file"),
        default="api",
        help="Origen de datos: API remota o JSON raw local.",
    )
    parser.add_argument(
        "--raw-path",
        help="Ruta al JSON raw si --source=file.",
    )
    parser.add_argument(
        "--skip-save-raw",
        action="store_true",
        help="No guarda copia raw cuando el origen es la API.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extrae y transforma, pero no carga en MySQL.",
    )
    return parser
