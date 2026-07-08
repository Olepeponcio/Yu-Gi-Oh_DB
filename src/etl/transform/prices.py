from decimal import Decimal, ROUND_HALF_UP

from src.etl.transform.common import to_decimal, to_int, validate_required


def normalize_card_prices(raw_card, eur_usd_rate=None):
    prices = raw_card.get("card_prices", [])

    if not prices:
        return None

    raw_prices = prices[0]
    cardmarket_price_eur = to_decimal(raw_prices.get("cardmarket_price"))
    cardmarket_price_usd = convert_eur_to_usd(cardmarket_price_eur, eur_usd_rate)
    card_prices = {
        "card_id": to_int(raw_card.get("id")),
        "cardmarket_price_eur": cardmarket_price_eur,
        "cardmarket_price_usd": cardmarket_price_usd,
        "tcgplayer_price": to_decimal(raw_prices.get("tcgplayer_price")),
        "ebay_price": to_decimal(raw_prices.get("ebay_price")),
        "amazon_price": to_decimal(raw_prices.get("amazon_price")),
        "coolstuffinc_price": to_decimal(raw_prices.get("coolstuffinc_price")),
    }
    validate_required(card_prices, ("card_id",), "Card prices")
    return card_prices


def convert_eur_to_usd(value, eur_usd_rate):
    if value is None or eur_usd_rate is None:
        return None

    return (value * Decimal(eur_usd_rate)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
