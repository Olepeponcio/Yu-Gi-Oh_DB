import argparse
from pathlib import Path

import mysql.connector

from src.database.connection import (
    get_db_host,
    get_db_port,
    get_db_user,
    get_required_env,
)
from src.etl.history_backup import create_card_price_history_backup
from src.etl.history_backup import restore_card_price_history_backup


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_FILES = (
    PROJECT_ROOT / "sql" / "drop_tables.sql",
    PROJECT_ROOT / "sql" / "schema.sql",
    PROJECT_ROOT / "sql" / "template_create_views.sql",
)


def reset_mysql(yes=False):
    if not yes:
        raise RuntimeError("Reset MySQL requiere confirmacion explicita con --yes.")

    db_name = get_required_env("DB_NAME")

    create_database_if_missing(db_name)
    backup_path, backup_rows = backup_history_if_available()
    execute_sql_files(SQL_FILES)
    restored_statements = restore_backup_if_available(backup_path)

    return {
        "database": db_name,
        "backup_path": str(backup_path) if backup_path is not None else None,
        "backup_rows": backup_rows,
        "restored_statements": restored_statements,
        "sql_files": [str(path) for path in SQL_FILES],
    }


def create_database_if_missing(db_name):
    connection = get_server_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def backup_history_if_available():
    if not table_exists("card_price_history"):
        return find_latest_backup(), 0

    row_count = count_table_rows("card_price_history")
    if row_count == 0:
        return find_latest_backup(), 0

    return create_card_price_history_backup()


def restore_backup_if_available(backup_path):
    if backup_path is None:
        return 0

    return restore_card_price_history_backup(backup_path)


def find_latest_backup():
    backup_dir = PROJECT_ROOT / "data" / "backups" / "card_price_history"
    backups = sorted(backup_dir.glob("card_price_history_*.sql"))
    if not backups:
        return None
    return backups[-1]


def table_exists(table_name):
    db_name = get_required_env("DB_NAME")
    connection = get_server_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s
                AND table_name = %s
            """,
            (db_name, table_name),
        )
        return cursor.fetchone()[0] > 0
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def count_table_rows(table_name):
    connection = get_database_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        return cursor.fetchone()[0]
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def execute_sql_files(paths):
    connection = get_database_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        for path in paths:
            for statement in read_sql_statements(path):
                cursor.execute(statement)
                consume_cursor_results(cursor)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def read_sql_statements(path):
    sql = path.read_text(encoding="utf-8")
    return split_sql_statements(sql)


def consume_cursor_results(cursor):
    while True:
        if cursor.with_rows:
            cursor.fetchall()

        if not cursor.nextset():
            break


def split_sql_statements(sql):
    statements = []
    current = []

    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        if stripped.upper().startswith("SOURCE "):
            raise RuntimeError("SOURCE no esta soportado dentro del reset Python.")

        current.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(current).strip().rstrip(";")
            if statement:
                statements.append(statement)
            current = []

    if current:
        statement = "\n".join(current).strip().rstrip(";")
        if statement:
            statements.append(statement)

    return statements


def get_server_connection():
    return mysql.connector.connect(
        host=get_db_host(),
        port=get_db_port(),
        user=get_db_user(),
        password=get_required_env("DB_PASSWORD"),
    )


def get_database_connection():
    return mysql.connector.connect(
        host=get_db_host(),
        port=get_db_port(),
        database=get_required_env("DB_NAME"),
        user=get_db_user(),
        password=get_required_env("DB_PASSWORD"),
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Reset seguro de MySQL con backup previo de card_price_history."
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma el backup/drop/recreacion de tablas.",
    )
    return parser


def main():
    args = build_parser().parse_args()
    result = reset_mysql(yes=args.yes)

    print(f"Base preparada: {result['database']}")
    if result["backup_path"] is None:
        print("Backup card_price_history omitido: la tabla no existia.")
    else:
        print(f"Backup card_price_history: {result['backup_path']}")
        print(f"Filas exportadas: {result['backup_rows']}")
        print(f"Sentencias restauradas: {result['restored_statements']}")

    print("SQL ejecutados:")
    for path in result["sql_files"]:
        print(f"- {path}")


if __name__ == "__main__":
    main()
