import unittest

from src.csv_sql_scripts.sql_builder import (
    build_create_staging_table_sql,
    quote_identifier,
)


class SqlBuilderSecurityTest(unittest.TestCase):
    def test_quote_identifier_accepts_safe_identifier(self):
        self.assertEqual(quote_identifier("vw_cards_2026"), "`vw_cards_2026`")

    def test_quote_identifier_rejects_unsafe_identifier(self):
        with self.assertRaisesRegex(ValueError, "Identificador SQL no valido"):
            quote_identifier("cards`; DROP TABLE cards; --")

    def test_build_create_staging_table_rejects_unsafe_columns(self):
        with self.assertRaisesRegex(ValueError, "Identificador SQL no valido"):
            build_create_staging_table_sql(
                "staging_cards",
                ["safe_column", "bad`; DROP TABLE cards; --"],
            )


if __name__ == "__main__":
    unittest.main()
