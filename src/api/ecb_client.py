import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from io import StringIO

import requests


EUR_USD_API_URL = (
    "https://data-api.ecb.europa.eu/service/data/EXR/"
    "D.USD.EUR.SP00.A?lastNObservations=1&format=csvdata"
)


@dataclass(frozen=True)
class ExchangeRate:
    source: str
    source_url: str
    base_currency: str
    quote_currency: str
    rate: Decimal
    observed_at: str


def fetch_eur_usd_rate():
    response = requests.get(EUR_USD_API_URL, timeout=30)
    response.raise_for_status()
    return parse_eur_usd_csv(response.text, EUR_USD_API_URL)


def parse_eur_usd_csv(raw_csv, source_url=EUR_USD_API_URL):
    reader = csv.DictReader(StringIO(raw_csv))
    rows = list(reader)

    if len(rows) != 1:
        raise ValueError("ECB EUR/USD response must include exactly one observation.")

    row = rows[0]
    if row.get("CURRENCY") != "USD" or row.get("CURRENCY_DENOM") != "EUR":
        raise ValueError("ECB response is not the expected EUR/USD series.")

    try:
        rate = Decimal(row["OBS_VALUE"])
    except (KeyError, InvalidOperation) as error:
        raise ValueError("ECB EUR/USD observation value must be a valid decimal.") from error

    if rate <= 0:
        raise ValueError("ECB EUR/USD observation value must be greater than zero.")

    return ExchangeRate(
        source="ECB Data Portal",
        source_url=source_url,
        base_currency="EUR",
        quote_currency="USD",
        rate=rate,
        observed_at=row.get("TIME_PERIOD") or "no disponible",
    )
