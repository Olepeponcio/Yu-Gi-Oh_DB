import json
from datetime import datetime, timezone
from pathlib import Path

import requests


API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
RAW_DATA_DIR = Path("data/raw")


def fetch_cardinfo():
    response = requests.get(API_URL, timeout=120)
    response.raise_for_status()
    payload = response.json()
    ingested_at = datetime.now(timezone.utc).isoformat()

    return {
        "metadata": {
            "source": "YGOPRODeck",
            "source_url": API_URL,
            "ingested_at": ingested_at,
            "source_last_updated": response.headers.get("Last-Modified"),
            "record_count": len(payload.get("data", [])),
        },
        "data": payload.get("data", []),
    }


def save_raw_payload(payload):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = RAW_DATA_DIR / f"cardinfo_{timestamp}.json"

    with raw_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    latest_path = RAW_DATA_DIR / "cardinfo_latest.json"
    with latest_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return raw_path


def load_raw_payload(raw_path):
    with Path(raw_path).open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if isinstance(payload, dict) and "data" in payload:
        return payload

    raise ValueError("Raw payload must be a JSON object with a 'data' key.")
