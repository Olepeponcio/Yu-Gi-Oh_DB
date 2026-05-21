from datetime import datetime
from pathlib import Path


REPORTING_DIR = Path("data/reporting")
REPORT_FILENAME_PREFIX = "etl_report"


def save_run_report(
    metadata,
    snapshot_at,
    raw_path,
    tables,
    dry_run,
    affected=None,
    report_dir=REPORTING_DIR,
    created_at=None,
):
    if created_at is None:
        created_at = datetime.now()

    report_path = build_report_path(created_at, report_dir)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report_text(metadata, snapshot_at, raw_path, tables, dry_run, affected, created_at),
        encoding="utf-8",
    )
    return report_path


def build_report_path(created_at, report_dir=REPORTING_DIR):
    timestamp = created_at.strftime("%Y%m%d_%H%M%S")
    return Path(report_dir) / f"{REPORT_FILENAME_PREFIX}_{timestamp}.txt"


def build_report_text(metadata, snapshot_at, raw_path, tables, dry_run, affected, created_at):
    lines = [
        "ETL YGOPRODeck report",
        f"generated_at: {created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"year: {created_at.strftime('%Y')}",
        f"month: {created_at.strftime('%m')}",
        f"day: {created_at.strftime('%d')}",
        f"hour: {created_at.strftime('%H')}",
        f"mode: {'dry-run' if dry_run else 'load'}",
        f"source: {metadata.get('source', 'raw file')}",
        f"raw_ingested_at: {metadata.get('ingested_at', 'no disponible')}",
        f"source_last_updated: {metadata.get('source_last_updated') or 'no disponible'}",
        f"price_snapshot_at: {snapshot_at}",
        f"raw_path: {raw_path or 'no guardado'}",
        "",
        "table_counts:",
    ]

    for table_name, rows in tables.items():
        lines.append(f"- {table_name}: {len(rows)}")

    if affected is not None:
        lines.extend(["", "affected_rows:"])
        for table_name, rowcount in affected.items():
            lines.append(f"- {table_name}: {rowcount}")

    return "\n".join(lines) + "\n"
