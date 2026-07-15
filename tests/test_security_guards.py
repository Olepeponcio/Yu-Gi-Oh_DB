import os
from unittest.mock import patch
import unittest

from src.api.ygoprodeck_client import (
    get_max_raw_payload_bytes,
    parse_cardinfo_payload,
    read_limited_response_body,
    resolve_raw_path,
    validate_cardinfo_payload,
)
from src.database.connection import (
    get_db_host,
    get_db_port,
    get_db_user,
    get_required_env,
)
from src.etl import load


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

    @patch.dict(os.environ, {"DB_USER": "root"}, clear=True)
    def test_db_user_rejects_root(self):
        with self.assertRaisesRegex(RuntimeError, "must not be root"):
            get_db_user()

    @patch.dict(os.environ, {"DB_HOST": "localhost"}, clear=True)
    def test_db_host_allows_localhost(self):
        self.assertEqual(get_db_host(), "localhost")

    @patch.dict(os.environ, {"DB_HOST": "192.168.1.50"}, clear=True)
    def test_db_host_rejects_remote_by_default(self):
        with self.assertRaisesRegex(RuntimeError, "must be local"):
            get_db_host()

    @patch.dict(
        os.environ,
        {"DB_HOST": "192.168.1.50", "DB_ALLOW_REMOTE_DB": "true"},
        clear=True,
    )
    def test_db_host_allows_remote_when_explicit(self):
        self.assertEqual(get_db_host(), "192.168.1.50")


class RawPathGuardTest(unittest.TestCase):
    def test_resolve_raw_path_allows_data_raw(self):
        path = resolve_raw_path("data/raw/cardinfo_latest.json")

        self.assertEqual(path.name, "cardinfo_latest.json")

    def test_resolve_raw_path_rejects_external_path(self):
        with self.assertRaisesRegex(ValueError, "inside data/raw"):
            resolve_raw_path("../secrets.json")


class ApiPayloadGuardTest(unittest.TestCase):
    @patch.dict(os.environ, {"YGOPRODECK_MAX_RAW_BYTES": "bad"}, clear=True)
    def test_max_raw_payload_requires_integer(self):
        with self.assertRaisesRegex(RuntimeError, "must be an integer"):
            get_max_raw_payload_bytes()

    @patch.dict(os.environ, {"YGOPRODECK_MAX_RAW_BYTES": "0"}, clear=True)
    def test_max_raw_payload_requires_positive_value(self):
        with self.assertRaisesRegex(RuntimeError, "greater than zero"):
            get_max_raw_payload_bytes()

    def test_validate_cardinfo_payload_requires_object(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            validate_cardinfo_payload([])

    def test_validate_cardinfo_payload_requires_data_list(self):
        with self.assertRaisesRegex(ValueError, "'data' list"):
            validate_cardinfo_payload({"data": {}})

    def test_parse_cardinfo_payload_returns_valid_payload(self):
        payload = parse_cardinfo_payload(b'{"data": []}')

        self.assertEqual(payload, {"data": []})

    def test_read_limited_response_body_rejects_large_content_length(self):
        response = FakeResponse(headers={"Content-Length": "10"}, chunks=[b"{}"])

        with self.assertRaisesRegex(ValueError, "larger"):
            read_limited_response_body(response, max_bytes=5)

    def test_read_limited_response_body_rejects_bad_content_length(self):
        response = FakeResponse(headers={"Content-Length": "bad"}, chunks=[b"{}"])

        with self.assertRaisesRegex(ValueError, "Content-Length"):
            read_limited_response_body(response, max_bytes=5)

    def test_read_limited_response_body_rejects_large_stream(self):
        response = FakeResponse(headers={}, chunks=[b"123", b"456"])

        with self.assertRaisesRegex(ValueError, "exceeded"):
            read_limited_response_body(response, max_bytes=5)


class FakeResponse:
    def __init__(self, headers, chunks):
        self.headers = headers
        self.chunks = chunks

    def iter_content(self, chunk_size):
        return iter(self.chunks)


class SqlPlaceholderGuardTest(unittest.TestCase):
    def test_load_sql_uses_named_placeholders(self):
        sql_builders = (
            load.cards_sql,
            load.card_printings_sql,
            load.sets_sql,
            load.rarity_types_sql,
            load.card_images_sql,
            load.card_price_history_sql,
            load.card_banlist_sql,
            load.card_typelines_sql,
            load.card_linkmarkers_sql,
        )

        for sql_builder in sql_builders:
            with self.subTest(sql_builder=sql_builder.__name__):
                self.assertIn("%(", sql_builder())


if __name__ == "__main__":
    unittest.main()
