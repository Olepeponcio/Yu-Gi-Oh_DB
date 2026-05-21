from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.etl.report_file import build_report_path, build_report_text, save_run_report


class ReportFileTest(unittest.TestCase):
    def test_build_report_path_uses_sortable_timestamp(self):
        created_at = datetime(2026, 5, 21, 8, 9, 10)

        report_path = build_report_path(created_at, report_dir="data/reporting")

        self.assertEqual(report_path, Path("data/reporting/etl_report_20260521_080910.txt"))

    def test_build_report_text_includes_date_parts_and_counts(self):
        created_at = datetime(2026, 5, 21, 8, 9, 10)
        text = build_report_text(
            metadata={"source": "test"},
            snapshot_at="2026-05-21 08:09:10",
            raw_path="data/raw/cardinfo_latest.json",
            tables={"cards": [{"id": 1}], "sets": []},
            dry_run=True,
            affected=None,
            created_at=created_at,
        )

        self.assertIn("year: 2026", text)
        self.assertIn("month: 05", text)
        self.assertIn("day: 21", text)
        self.assertIn("hour: 08", text)
        self.assertIn("mode: dry-run", text)
        self.assertIn("- cards: 1", text)
        self.assertIn("- sets: 0", text)

    def test_save_run_report_writes_txt_file(self):
        created_at = datetime(2026, 5, 21, 8, 9, 10)

        with TemporaryDirectory() as temp_dir:
            report_path = save_run_report(
                metadata={"source": "test"},
                snapshot_at="2026-05-21 08:09:10",
                raw_path=None,
                tables={"cards": []},
                dry_run=False,
                affected={"cards": 0},
                report_dir=temp_dir,
                created_at=created_at,
            )

            self.assertTrue(report_path.exists())
            self.assertEqual(report_path.name, "etl_report_20260521_080910.txt")
            self.assertIn("affected_rows:", report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
