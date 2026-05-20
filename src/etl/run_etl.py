import argparse
from datetime import datetime

from src.api.ygoprodeck_client import fetch_cardinfo, load_raw_payload, save_raw_payload
from src.etl.load import load_all_tables
from src.etl.transform import transform_cards


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


def get_payload(args):
    if args.source == "file":
        if not args.raw_path:
            raise ValueError("--raw-path es obligatorio cuando --source=file.")
        return load_raw_payload(args.raw_path), None

    payload = fetch_cardinfo()
    raw_path = None

    if not args.skip_save_raw:
        raw_path = save_raw_payload(payload)

    return payload, raw_path


def print_table_counts(tables):
    print(f"cards: {len(tables['cards'])}")
    print(f"sets: {len(tables['sets'])}")
    print(f"rarities: {len(tables['rarities'])}")
    print(f"card_sets: {len(tables['card_sets'])}")
    print(f"card_images: {len(tables['card_images'])}")
    print(f"card_prices: {len(tables['card_prices'])}")
    print(f"card_price_history: {len(tables['card_price_history'])}")
    print(f"card_banlist: {len(tables['card_banlist'])}")
    print(f"card_typelines: {len(tables['card_typelines'])}")
    print(f"card_linkmarkers: {len(tables['card_linkmarkers'])}")


def main():
    args = build_parser().parse_args()
    payload, raw_path = get_payload(args)
    raw_cards = payload["data"]
    metadata = payload.get("metadata", {})
    snapshot_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tables = transform_cards(raw_cards, snapshot_at=snapshot_at)

    print(f"Fuente: {metadata.get('source', 'raw file')}")
    print(f"Fecha de ingesta raw: {metadata.get('ingested_at', 'no disponible')}")
    print(f"Ultima actualizacion fuente: {metadata.get('source_last_updated') or 'no disponible'}")
    print(f"Snapshot de precios: {snapshot_at}")
    if raw_path is not None:
        print(f"JSON raw guardado: {raw_path}")

    print_table_counts(tables)

    if args.dry_run:
        print("Dry-run completado sin cargar en MySQL.")
        return

    affected = load_all_tables(tables)
    print("Carga MySQL completada.")
    for table, rowcount in affected.items():
        print(f"{table}: {rowcount}")


if __name__ == "__main__":
    main()
