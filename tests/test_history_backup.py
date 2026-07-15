from datetime import datetime
from decimal import Decimal
import unittest
from unittest.mock import Mock, mock_open, patch

from src.etl.history_backup import (
    build_backup_filename,
    build_backup_sql,
    restore_card_price_history_backup,
    parse_long_insert_row,
    split_sql_statements,
    expand_legacy_history_rows,
)


class HistoryBackupTest(unittest.TestCase):
    def test_parse_long_backup_insert_for_batched_restore(self):
        sql = build_backup_sql([{
            "card_id": 1,
            "marketplace_id": 1,
            "currency_code": "EUR",
            "snapshot_at": datetime(2026, 7, 14, 15, 4, 45),
            "price": Decimal("1.10"),
            "price_origin": "api",
            "exchange_rate": None,
        }])
        insert = next(line for line in sql.splitlines() if line.startswith("INSERT"))
        row = parse_long_insert_row(insert)
        self.assertEqual(row[0:3], ("1", "1", "EUR"))
        self.assertEqual(row[4], "1.10")
        self.assertIsNone(row[6])

    def test_legacy_wide_history_is_expanded_without_losing_snapshot(self):
        rows = [{
            "card_id": 1,
            "snapshot_at": datetime(2026, 7, 14, 15, 4, 45),
            "cardmarket_price_eur": Decimal("1.10"),
            "cardmarket_usd": Decimal("1.26"),
            "tcgplayer_price": None,
            "ebay_price": Decimal("2.00"),
            "amazon_price": None,
            "coolstuffinc_price": None,
        }]
        expanded = expand_legacy_history_rows(rows)
        self.assertEqual(len(expanded), 3)
        self.assertTrue(all(row["snapshot_at"] == rows[0]["snapshot_at"] for row in expanded))
        self.assertEqual({row["marketplace_id"] for row in expanded}, {1, 3})

    def test_build_backup_filename_uses_sortable_timestamp(self):
        filename = build_backup_filename(datetime(2026, 7, 14, 16, 5, 2))

        self.assertEqual(filename, "card_price_history_20260714_160502.sql")

    def test_build_backup_sql_generates_restorable_inserts(self):
        rows = [
            {
                "card_id": 1,
                "marketplace_id": 1,
                "currency_code": "EUR",
                "snapshot_at": datetime(2026, 7, 14, 15, 4, 45),
                "price": Decimal("1.10"),
                "price_origin": "api",
                "exchange_rate": None,
            }
        ]

        sql = build_backup_sql(rows)

        self.assertIn("INSERT INTO card_price_history", sql)
        self.assertIn("'2026-07-14 15:04:45'", sql)
        self.assertIn("ON DUPLICATE KEY UPDATE", sql)
        self.assertIn("price = VALUES(price)", sql)

    def test_split_sql_statements_ignores_comments_set_and_use(self):
        sql = """
        -- comment
        SET NAMES utf8mb4;
        USE `yugioh_db`;
        INSERT INTO card_price_history (card_id) VALUES (1);
        """

        statements = split_sql_statements(sql)

        self.assertEqual(statements, ["INSERT INTO card_price_history (card_id) VALUES (1)"])

    @patch("src.etl.history_backup.get_connection")
    def test_restore_disables_foreign_key_checks_temporarily(self, get_connection):
        connection = Mock()
        cursor = Mock()
        connection.cursor.return_value = cursor
        get_connection.return_value = connection

        with patch(
            "pathlib.Path.open",
            mock_open(read_data="INSERT INTO card_price_history (card_id) VALUES (1);\n"),
        ):
            restore_card_price_history_backup("backup.sql")

        executed = [call.args[0] for call in cursor.execute.call_args_list]
        self.assertEqual(executed[0], "SET FOREIGN_KEY_CHECKS = 0")
        self.assertIn("INSERT INTO card_price_history (card_id) VALUES (1)", executed)
        self.assertIn("SET FOREIGN_KEY_CHECKS = 1", executed)
        connection.commit.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
