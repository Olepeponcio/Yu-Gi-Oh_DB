from datetime import datetime

from src.api.ygoprodeck_client import fetch_cardinfo, load_raw_payload, save_raw_payload
from src.etl.load import load_all_tables
from src.etl.reporting import print_load_summary, print_run_summary, print_table_counts
from src.etl.transform import transform_cards


def run_pipeline(args):
    payload, raw_path = get_payload(args)
    raw_cards = payload["data"]
    metadata = payload.get("metadata", {})
    snapshot_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tables = transform_cards(raw_cards, snapshot_at=snapshot_at)

    print_run_summary(metadata, snapshot_at, raw_path)
    print_table_counts(tables)

    if args.dry_run:
        print("Dry-run completado sin cargar en MySQL.")
        return tables

    affected = load_all_tables(tables)
    print_load_summary(affected)
    return tables


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
