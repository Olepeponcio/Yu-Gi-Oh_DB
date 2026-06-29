import os
from unittest.mock import patch
import unittest

from src.api.ygoprodeck_client import resolve_raw_path
from src.database.connection import get_db_port, get_required_env


class DatabaseEnvGuardTest(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_get_required_env_fails_when_missing(self):
        with self.assertRaisesRegex(RuntimeError, "DB_USER"):
            get_required_env("DB_USER")

    @patch.dict(os.environ, {"DB_PORT": "bad"}, clear=True)
    def test_get_db_port_requires_integer(self):
        with self.assertRaisesRegex(RuntimeError, "DB_PORT must be an integer"):
            get_db_port()

    @patch.dict(os.environ, {}, clear=True)
    def test_get_db_port_defaults_to_mysql_port(self):
        self.assertEqual(get_db_port(), 3306)


class RawPathGuardTest(unittest.TestCase):
    def test_resolve_raw_path_allows_data_raw(self):
        path = resolve_raw_path("data/raw/cardinfo_latest.json")

        self.assertEqual(path.name, "cardinfo_latest.json")

    def test_resolve_raw_path_rejects_external_path(self):
        with self.assertRaisesRegex(ValueError, "inside data/raw"):
            resolve_raw_path("../secrets.json")


if __name__ == "__main__":
    unittest.main()
