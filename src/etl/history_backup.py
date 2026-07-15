import argparse
import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.database.connection import get_connection


BACKUP_DIR = Path("data/backups/card_price_history")
TABLE_NAME = "card_price_history"
BACKUP_COLUMNS = (
    "card_id",
    "marketplace_id",
    "currency_code",
    "snapshot_at",
    "price",
    "price_origin",
    "exchange_rate",
)
RESTORE_BATCH_SIZE = 2000
LONG_INSERT_PREFIX = f"INSERT INTO {TABLE_NAME} ({', '.join(BACKUP_COLUMNS)}) VALUES ("
LONG_INSERT_SUFFIX = ") ON DUPLICATE KEY UPDATE"

LEGACY_PRICE_COLUMNS = (
    ("cardmarket_price_eur", 1, "EUR", "api"),
    ("cardmarket_usd", 1, "USD", "currency_conversion"),
    ("tcgplayer_price", 2, "USD", "api"),
    ("ebay_price", 3, "USD", "api"),
    ("amazon_price", 4, "USD", "api"),
    ("coolstuffinc_price", 5, "USD", "api"),
)


def create_card_price_history_backup(backup_dir=BACKUP_DIR, created_at=None):
    if created_at is None:
        created_at = datetime.now()

    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / build_backup_filename(created_at)

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        rows = fetch_card_price_history_rows(cursor)
        backup_path.write_text(build_backup_sql(rows), encoding="utf-8")
        return backup_path, len(rows)
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def restore_card_price_history_backup(backup_path):
    backup_path = Path(backup_path)
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        restored = restore_backup_stream(cursor, backup_path)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        return restored
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            except Exception:
                pass
            cursor.close()
        connection.close()


def restore_backup_stream(cursor, backup_path, batch_size=RESTORE_BATCH_SIZE):
    batch = []
    restored = 0
    with Path(backup_path).open("r", encoding="utf-8") as backup_file:
        for line in backup_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("--") or stripped.upper().startswith(("SET ", "USE ")):
                continue
            row = parse_long_insert_row(stripped)
            if row is None:
                cursor.execute(stripped.rstrip(";"))
                restored += 1
                continue
            batch.append(row)
            if len(batch) >= batch_size:
                restored += insert_history_batch(cursor, batch)
                batch = []
    if batch:
        restored += insert_history_batch(cursor, batch)
    return restored


def parse_long_insert_row(statement):
    if not statement.startswith(LONG_INSERT_PREFIX):
        return None
    suffix_index = statement.find(LONG_INSERT_SUFFIX, len(LONG_INSERT_PREFIX))
    if suffix_index == -1:
        return None
    values_text = statement[len(LONG_INSERT_PREFIX):suffix_index]
    values = next(csv.reader([values_text], delimiter=",", quotechar="'", escapechar="\\", skipinitialspace=True))
    if len(values) != len(BACKUP_COLUMNS):
        raise ValueError("Backup histórico largo con número de columnas inválido.")
    return tuple(None if value.strip().upper() == "NULL" else value for value in values)


def insert_history_batch(cursor, rows):
    placeholders = ", ".join(["%s"] * len(BACKUP_COLUMNS))
    updates = ", ".join(
        f"{column} = VALUES({column})"
        for column in BACKUP_COLUMNS
        if column not in {"card_id", "marketplace_id", "currency_code", "snapshot_at"}
    )
    cursor.executemany(
        f"INSERT INTO {TABLE_NAME} ({', '.join(BACKUP_COLUMNS)}) "
        f"VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}",
        rows,
    )
    return len(rows)


def fetch_card_price_history_rows(cursor):
    try:
        cursor.execute(
            f"SELECT {', '.join(BACKUP_COLUMNS)} FROM {TABLE_NAME} "
            "ORDER BY snapshot_at, card_id, marketplace_id, currency_code"
        )
        return cursor.fetchall()
    except Exception as error:
        if getattr(error, "errno", None) != 1054:
            raise

    legacy_columns = ("card_id", "snapshot_at") + tuple(row[0] for row in LEGACY_PRICE_COLUMNS)
    cursor.execute(
        f"SELECT {', '.join(legacy_columns)} FROM {TABLE_NAME} ORDER BY snapshot_at, card_id"
    )
    return expand_legacy_history_rows(cursor.fetchall())


def expand_legacy_history_rows(rows):
    expanded = []
    for row in rows:
        for column, marketplace_id, currency_code, origin in LEGACY_PRICE_COLUMNS:
            if row[column] is None:
                continue
            expanded.append({
                "card_id": row["card_id"],
                "marketplace_id": marketplace_id,
                "currency_code": currency_code,
                "snapshot_at": row["snapshot_at"],
                "price": row[column],
                "price_origin": origin,
                "exchange_rate": None,
            })
    return expanded


def build_backup_filename(created_at):
    return f"card_price_history_{created_at.strftime('%Y%m%d_%H%M%S')}.sql"


def build_backup_sql(rows):
    lines = [
        "-- Backup de card_price_history.",
        "-- Restaurar despues de recrear schema.sql y antes de ejecutar un nuevo ETL.",
        "SET NAMES utf8mb4;",
        "USE `yugioh_db`;",
        "",
    ]

    if not rows:
        lines.append("-- Sin filas para restaurar.")
        return "\n".join(lines) + "\n"

    for row in rows:
        lines.append(build_insert_statement(row))

    return "\n".join(lines) + "\n"


def build_insert_statement(row):
    columns = ", ".join(BACKUP_COLUMNS)
    values = ", ".join(sql_literal(row[column]) for column in BACKUP_COLUMNS)
    updates = ", ".join(
        f"{column} = VALUES({column})"
        for column in BACKUP_COLUMNS
        if column not in {"card_id", "marketplace_id", "currency_code", "snapshot_at"}
    )
    return (
        f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({values}) "
        f"ON DUPLICATE KEY UPDATE {updates};"
    )


def sql_literal(value):
    if value is None:
        return "NULL"
    if isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def split_sql_statements(sql):
    statements = []
    current = []

    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        current.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(current).strip().rstrip(";")
            if not statement.upper().startswith(("SET ", "USE ")):
                statements.append(statement)
            current = []

    if current:
        statement = "\n".join(current).strip().rstrip(";")
        if statement:
            statements.append(statement)

    return statements


def build_parser():
    parser = argparse.ArgumentParser(
        description="Backup y restauracion de card_price_history."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument("--backup-dir", default=str(BACKUP_DIR))

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("backup_path")

    return parser


def main():
    args = build_parser().parse_args()

    if args.command == "backup":
        backup_path, row_count = create_card_price_history_backup(args.backup_dir)
        print(f"Backup card_price_history guardado: {backup_path}")
        print(f"Filas exportadas: {row_count}")
        return

    restored = restore_card_price_history_backup(args.backup_path)
    print(f"Backup card_price_history restaurado: {args.backup_path}")
    print(f"Sentencias ejecutadas: {restored}")


if __name__ == "__main__":
    main()
