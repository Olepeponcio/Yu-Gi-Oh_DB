from argparse import Namespace
import unittest
from unittest.mock import patch

from src.etl.load import rarities_sql
from src.etl.pipeline import get_payload, run_pipeline


class GetPayloadTest(unittest.TestCase):
    def test_file_source_requires_raw_path(self):
        args = Namespace(source="file", raw_path=None, skip_save_raw=False)

        with self.assertRaisesRegex(ValueError, "--raw-path es obligatorio"):
            get_payload(args)

    @patch("src.etl.pipeline.load_raw_payload")
    def test_file_source_loads_local_payload(self, load_raw_payload):
        expected_payload = {"data": []}
        load_raw_payload.return_value = expected_payload
        args = Namespace(source="file", raw_path="data/raw/cardinfo_latest.json", skip_save_raw=False)

        payload, raw_path = get_payload(args)

        self.assertIs(payload, expected_payload)
        self.assertIsNone(raw_path)
        load_raw_payload.assert_called_once_with("data/raw/cardinfo_latest.json")

    @patch("src.etl.pipeline.save_raw_payload")
    @patch("src.etl.pipeline.fetch_cardinfo")
    def test_api_source_can_skip_raw_save(self, fetch_cardinfo, save_raw_payload):
        expected_payload = {"data": []}
        fetch_cardinfo.return_value = expected_payload
        args = Namespace(source="api", raw_path=None, skip_save_raw=True)

        payload, raw_path = get_payload(args)

        self.assertIs(payload, expected_payload)
        self.assertIsNone(raw_path)
        fetch_cardinfo.assert_called_once_with()
        save_raw_payload.assert_not_called()


class RunPipelineTest(unittest.TestCase):
    @patch("src.etl.pipeline.save_run_report")
    @patch("src.etl.pipeline.print_table_counts")
    @patch("src.etl.pipeline.print_run_summary")
    @patch("src.etl.pipeline.transform_cards")
    @patch("src.etl.pipeline.get_payload")
    @patch("src.etl.pipeline.load_all_tables")
    def test_dry_run_does_not_load_mysql(
        self,
        load_all_tables,
        get_payload_mock,
        transform_cards,
        print_run_summary,
        print_table_counts,
        save_run_report,
    ):
        payload = {"metadata": {"source": "test"}, "data": [{"id": "1"}]}
        tables = {"cards": [{"card_id": 1}]}
        args = Namespace(source="file", raw_path="raw.json", skip_save_raw=False, dry_run=True)
        get_payload_mock.return_value = (payload, None)
        transform_cards.return_value = tables

        with patch("builtins.print"):
            result = run_pipeline(args)

        self.assertIs(result, tables)
        transform_cards.assert_called_once()
        print_run_summary.assert_called_once()
        print_table_counts.assert_called_once_with(tables)
        save_run_report.assert_called_once()
        self.assertTrue(save_run_report.call_args.kwargs["dry_run"])
        load_all_tables.assert_not_called()

    @patch("src.etl.pipeline.save_run_report")
    @patch("src.etl.pipeline.print_load_summary")
    @patch("src.etl.pipeline.print_table_counts")
    @patch("src.etl.pipeline.print_run_summary")
    @patch("src.etl.pipeline.transform_cards")
    @patch("src.etl.pipeline.get_payload")
    @patch("src.etl.pipeline.load_all_tables")
    def test_full_run_loads_mysql(
        self,
        load_all_tables,
        get_payload_mock,
        transform_cards,
        print_run_summary,
        print_table_counts,
        print_load_summary,
        save_run_report,
    ):
        payload = {"metadata": {"source": "test"}, "data": [{"id": "1"}]}
        tables = {"cards": [{"card_id": 1}]}
        affected = {"cards": 1}
        args = Namespace(source="file", raw_path="raw.json", skip_save_raw=False, dry_run=False)
        get_payload_mock.return_value = (payload, None)
        transform_cards.return_value = tables
        load_all_tables.return_value = affected

        with patch("builtins.print"):
            result = run_pipeline(args)

        self.assertIs(result, tables)
        load_all_tables.assert_called_once_with(tables)
        print_load_summary.assert_called_once_with(affected)
        save_run_report.assert_called_once()
        self.assertFalse(save_run_report.call_args.kwargs["dry_run"])
        self.assertEqual(save_run_report.call_args.kwargs["affected"], affected)


class LoadSqlTest(unittest.TestCase):
    def test_rarities_sql_uses_set_code_not_card_id(self):
        sql = rarities_sql()

        self.assertIn("set_code", sql)
        self.assertIn("%(set_code)s", sql)
        self.assertNotIn("%(card_id)s", sql)


if __name__ == "__main__":
    unittest.main()
