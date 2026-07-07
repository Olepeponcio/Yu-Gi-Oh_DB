import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests


API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
RAW_DATA_DIR = Path("data/raw")
DEFAULT_MAX_RAW_PAYLOAD_BYTES = 75 * 1024 * 1024
DOWNLOAD_CHUNK_SIZE = 1024 * 1024


def fetch_cardinfo():
    response = requests.get(API_URL, timeout=120, stream=True)
    try:
        response.raise_for_status()
        raw_body = read_limited_response_body(response, get_max_raw_payload_bytes())
    finally:
        response.close()

    payload = parse_cardinfo_payload(raw_body)
    ingested_at = datetime.now(timezone.utc).isoformat()
    data = payload["data"]

    return {
        "metadata": {
            "source": "YGOPRODeck",
            "source_url": API_URL,
            "ingested_at": ingested_at,
            "source_last_updated": response.headers.get("Last-Modified"),
            "record_count": len(data),
        },
        "data": data,
    }


def get_max_raw_payload_bytes():
    raw_value = os.getenv("YGOPRODECK_MAX_RAW_BYTES")

    if raw_value is None or raw_value == "":
        return DEFAULT_MAX_RAW_PAYLOAD_BYTES

    try:
        value = int(raw_value)
    except ValueError as error:
        raise RuntimeError("YGOPRODECK_MAX_RAW_BYTES must be an integer.") from error

    if value <= 0:
        raise RuntimeError("YGOPRODECK_MAX_RAW_BYTES must be greater than zero.")

    return value


def read_limited_response_body(response, max_bytes):
    content_length = response.headers.get("Content-Length")

    if content_length is not None:
        try:
            content_length_bytes = int(content_length)
        except ValueError as error:
            raise ValueError("API response Content-Length must be an integer.") from error

        if content_length_bytes > max_bytes:
            raise ValueError("API response is larger than the configured limit.")

    chunks = []
    total_bytes = 0

    for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
        if not chunk:
            continue

        total_bytes += len(chunk)
        if total_bytes > max_bytes:
            raise ValueError("API response exceeded the configured limit.")

        chunks.append(chunk)

    return b"".join(chunks)


def parse_cardinfo_payload(raw_body):
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("API response must be valid UTF-8 JSON.") from error

    return validate_cardinfo_payload(payload)


def validate_cardinfo_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Raw payload must be a JSON object.")

    if not isinstance(payload.get("data"), list):
        raise ValueError("Raw payload must include a 'data' list.")

    return payload


def save_raw_payload(payload):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    latest_path = RAW_DATA_DIR / "cardinfo_latest.json"

    with latest_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return latest_path


def load_raw_payload(raw_path):
    path = resolve_raw_path(raw_path)

    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    return validate_cardinfo_payload(payload)


def resolve_raw_path(raw_path):
    raw_dir = RAW_DATA_DIR.resolve()
    path = Path(raw_path).resolve()

    try:
        path.relative_to(raw_dir)
    except ValueError as error:
        raise ValueError("Raw payload path must be inside data/raw.") from error

    return path
