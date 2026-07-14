import argparse
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.database.connection import get_connection


BACKUP_DIR = Path("data/backups/card_price_history")
TABLE_NAME = "card_price_history"
BACKUP_COLUMNS = (
    "card_id",
    "snapshot_at",
    "cardmarket_price_eur",
    "cardmarket_usd",
    "tcgplayer_price",
    "ebay_price",
    "amazon_price",
    "coolstuffinc_price",
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
    sql = backup_path.read_text(encoding="utf-8")

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        statements = split_sql_statements(sql)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for statement in statements:
            cursor.execute(statement)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        return len(statements)
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


def fetch_card_price_history_rows(cursor):
    cursor.execute(
        f"""
        SELECT {", ".join(BACKUP_COLUMNS)}
        FROM {TABLE_NAME}
        ORDER BY snapshot_at, card_id
        """
    )
    return cursor.fetchall()


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
        if column not in {"card_id", "snapshot_at"}
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
