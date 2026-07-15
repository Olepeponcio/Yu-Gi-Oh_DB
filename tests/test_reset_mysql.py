import unittest
from unittest.mock import patch

from src.etl.reset_mysql import (
    SQL_FILES,
    backup_history_if_available,
    consume_cursor_results,
    reset_mysql,
    split_sql_statements,
)


class ResetMysqlTest(unittest.TestCase):
    def test_reset_only_executes_drop_and_schema(self):
        self.assertEqual([path.name for path in SQL_FILES], ["drop_tables.sql", "schema.sql"])

    def test_reset_requires_yes(self):
        with self.assertRaisesRegex(RuntimeError, "--yes"):
            reset_mysql()

    def test_split_sql_statements_rejects_source(self):
        with self.assertRaisesRegex(RuntimeError, "SOURCE"):
            split_sql_statements("SOURCE sql/schema.sql;")

    def test_split_sql_statements_ignores_comments(self):
        statements = split_sql_statements(
            """
            -- comment
            USE `yugioh_db`;
            CREATE TABLE demo (id INT);
            """
        )

        self.assertEqual(
            statements,
            ["USE `yugioh_db`", "CREATE TABLE demo (id INT)"],
        )

    @patch("src.etl.reset_mysql.restore_backup_if_available")
    @patch("src.etl.reset_mysql.execute_sql_files")
    @patch("src.etl.reset_mysql.backup_history_if_available")
    @patch("src.etl.reset_mysql.create_database_if_missing")
    @patch("src.etl.reset_mysql.get_required_env")
    def test_reset_runs_database_backup_and_sql_steps(
        self,
        get_required_env,
        create_database_if_missing,
        backup_history_if_available,
        execute_sql_files,
        restore_backup_if_available,
    ):
        get_required_env.return_value = "yugioh_db"
        backup_history_if_available.return_value = ("backup.sql", 10)
        restore_backup_if_available.return_value = 10

        result = reset_mysql(yes=True)

        create_database_if_missing.assert_called_once_with("yugioh_db")
        backup_history_if_available.assert_called_once_with()
        execute_sql_files.assert_called_once()
        restore_backup_if_available.assert_called_once_with("backup.sql")
        self.assertEqual(result["backup_rows"], 10)
        self.assertEqual(result["restored_statements"], 10)

    def test_consume_cursor_results_fetches_result_sets(self):
        cursor = FakeCursor([True, False])

        consume_cursor_results(cursor)

        self.assertEqual(cursor.fetchall_calls, 1)
        self.assertEqual(cursor.nextset_calls, 2)

    @patch("src.etl.reset_mysql.find_latest_backup")
    @patch("src.etl.reset_mysql.count_table_rows")
    @patch("src.etl.reset_mysql.table_exists")
    def test_backup_history_uses_latest_backup_when_table_is_empty(
        self,
        table_exists,
        count_table_rows,
        find_latest_backup,
    ):
        table_exists.return_value = True
        count_table_rows.return_value = 0
        find_latest_backup.return_value = "latest.sql"

        backup_path, rows = backup_history_if_available()

        self.assertEqual(backup_path, "latest.sql")
        self.assertEqual(rows, 0)


class FakeCursor:
    def __init__(self, with_rows_values):
        self.with_rows_values = with_rows_values
        self.index = 0
        self.fetchall_calls = 0
        self.nextset_calls = 0

    @property
    def with_rows(self):
        return self.with_rows_values[self.index]

    def fetchall(self):
        self.fetchall_calls += 1
        return []

    def nextset(self):
        self.nextset_calls += 1
        if self.index + 1 >= len(self.with_rows_values):
            return None

        self.index += 1
        return True


if __name__ == "__main__":
    unittest.main()
