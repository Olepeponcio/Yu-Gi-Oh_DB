from datetime import datetime

from src.api.ecb_client import fetch_eur_usd_rate
from src.api.ygoprodeck_client import fetch_cardinfo, load_raw_payload, save_raw_payload
from src.etl.load import load_all_tables
from src.etl.report_file import save_run_report
from src.etl.reporting import print_load_summary, print_run_summary, print_table_counts
from src.etl.transform import transform_cards


def run_pipeline(args):
    payload, raw_path, extraction_events = get_payload(args)
    exchange_rate = get_exchange_rate(extraction_events)
    raw_cards = payload["data"]
    metadata = payload.get("metadata", {})
    snapshot_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    eur_usd_rate = exchange_rate.rate if exchange_rate is not None else None
    tables = transform_cards(raw_cards, snapshot_at=snapshot_at, eur_usd_rate=eur_usd_rate)

    print_run_summary(metadata, snapshot_at, raw_path)
    print_extraction_events(extraction_events)
    print_table_counts(tables)

    if metadata.get("extraction_status") == "failed":
        print("Carga MySQL omitida: no hay extraccion valida de YGOPRODeck.")
        report_path = save_run_report(
            metadata,
            snapshot_at,
            raw_path,
            tables,
            dry_run=True,
            extraction_events=extraction_events,
            exchange_rate=exchange_rate,
        )
        print(f"Reporte ETL guardado: {report_path}")
        return tables

    if args.dry_run:
        print("Dry-run completado sin cargar en MySQL.")
        report_path = save_run_report(
            metadata,
            snapshot_at,
            raw_path,
            tables,
            dry_run=True,
            extraction_events=extraction_events,
            exchange_rate=exchange_rate,
        )
        print(f"Reporte ETL guardado: {report_path}")
        return tables

    affected = load_all_tables(tables)
    print_load_summary(affected)
    report_path = save_run_report(
        metadata,
        snapshot_at,
        raw_path,
        tables,
        dry_run=False,
        affected=affected,
        extraction_events=extraction_events,
        exchange_rate=exchange_rate,
    )
    print(f"Reporte ETL guardado: {report_path}")
    return tables


def get_payload(args):
    if args.source == "file":
        if not args.raw_path:
            raise ValueError("--raw-path es obligatorio cuando --source=file.")
        return load_raw_payload(args.raw_path), None, [
            {"source": "YGOPRODeck", "status": "skipped", "detail": "Origen local --source=file."}
        ]

    try:
        payload = fetch_cardinfo()
    except Exception as error:
        print(f"Error extrayendo YGOPRODeck: {error}")
        return (
            {
                "metadata": {
                    "source": "YGOPRODeck",
                    "extraction_status": "failed",
                    "extraction_error": str(error),
                },
                "data": [],
            },
            None,
            [{"source": "YGOPRODeck", "status": "failed", "detail": str(error)}],
        )

    raw_path = None

    if not args.skip_save_raw:
        raw_path = save_raw_payload(payload)

    return payload, raw_path, [
        {"source": "YGOPRODeck", "status": "ok", "detail": f"{len(payload['data'])} registros."}
    ]


def get_exchange_rate(extraction_events):
    try:
        exchange_rate = fetch_eur_usd_rate()
    except Exception as error:
        print(f"Error extrayendo ECB EUR/USD: {error}")
        extraction_events.append({"source": "ECB Data Portal", "status": "failed", "detail": str(error)})
        return None

    extraction_events.append(
        {
            "source": "ECB Data Portal",
            "status": "ok",
            "detail": (
                f"1 {exchange_rate.base_currency} = {exchange_rate.rate} "
                f"{exchange_rate.quote_currency}; observacion {exchange_rate.observed_at}."
            ),
        }
    )
    return exchange_rate


def print_extraction_events(extraction_events):
    for event in extraction_events:
        print(f"Extraccion {event['source']}: {event['status']} - {event['detail']}")
