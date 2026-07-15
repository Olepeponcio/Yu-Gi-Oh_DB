from decimal import Decimal, ROUND_HALF_UP

from src.etl.transform.common import to_decimal, to_int, validate_required

PRICE_FIELDS = (
    (1, "EUR", "cardmarket_price"),
    (2, "USD", "tcgplayer_price"),
    (3, "USD", "ebay_price"),
    (4, "USD", "amazon_price"),
    (5, "USD", "coolstuffinc_price"),
)


def normalize_card_prices(raw_card, snapshot_at=None, eur_usd_rate=None):
    prices = raw_card.get("card_prices", [])
    if not prices:
        return []
    card_id = to_int(raw_card.get("id"))
    validate_required({"card_id": card_id}, ("card_id",), "Card prices")
    raw_prices = prices[0]
    rows = []
    for marketplace_id, currency_code, field in PRICE_FIELDS:
        price = to_decimal(raw_prices.get(field))
        if price is not None:
            rows.append(_price_row(card_id, marketplace_id, currency_code, snapshot_at, price, "api"))

    converted = convert_eur_to_usd(to_decimal(raw_prices.get("cardmarket_price")), eur_usd_rate)
    if converted is not None:
        row = _price_row(card_id, 1, "USD", snapshot_at, converted, "currency_conversion")
        row["exchange_rate"] = Decimal(eur_usd_rate)
        rows.append(row)
    return rows


def _price_row(card_id, marketplace_id, currency_code, snapshot_at, price, origin):
    return {
        "card_id": card_id,
        "marketplace_id": marketplace_id,
        "currency_code": currency_code,
        "snapshot_at": snapshot_at,
        "price": price,
        "price_origin": origin,
        "exchange_rate": None,
    }


def convert_eur_to_usd(value, eur_usd_rate):
    if value is None or eur_usd_rate is None:
        return None
    return (value * Decimal(eur_usd_rate)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
