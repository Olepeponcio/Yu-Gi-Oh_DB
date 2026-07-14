from datetime import datetime
from decimal import Decimal
import unittest
from unittest.mock import Mock, patch

from src.etl.history_backup import (
    build_backup_filename,
    build_backup_sql,
    restore_card_price_history_backup,
    split_sql_statements,
)


class HistoryBackupTest(unittest.TestCase):
    def test_build_backup_filename_uses_sortable_timestamp(self):
        filename = build_backup_filename(datetime(2026, 7, 14, 16, 5, 2))

        self.assertEqual(filename, "card_price_history_20260714_160502.sql")

    def test_build_backup_sql_generates_restorable_inserts(self):
        rows = [
            {
                "card_id": 1,
                "snapshot_at": datetime(2026, 7, 14, 15, 4, 45),
                "cardmarket_price_eur": Decimal("1.10"),
                "cardmarket_usd": Decimal("1.26"),
                "tcgplayer_price": None,
                "ebay_price": Decimal("2.00"),
                "amazon_price": None,
                "coolstuffinc_price": None,
            }
        ]

        sql = build_backup_sql(rows)

        self.assertIn("INSERT INTO card_price_history", sql)
        self.assertIn("'2026-07-14 15:04:45'", sql)
        self.assertIn("ON DUPLICATE KEY UPDATE", sql)
        self.assertIn("cardmarket_price_eur = VALUES(cardmarket_price_eur)", sql)

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

        with patch("pathlib.Path.read_text", return_value="INSERT INTO card_price_history (card_id) VALUES (1);"):
            restore_card_price_history_backup("backup.sql")

        executed = [call.args[0] for call in cursor.execute.call_args_list]
        self.assertEqual(executed[0], "SET FOREIGN_KEY_CHECKS = 0")
        self.assertIn("INSERT INTO card_price_history (card_id) VALUES (1)", executed)
        self.assertIn("SET FOREIGN_KEY_CHECKS = 1", executed)
        connection.commit.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
