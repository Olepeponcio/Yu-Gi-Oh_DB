from src.etl.transform.common import to_decimal, to_int, validate_required


def normalize_card_prices(raw_card):
    prices = raw_card.get("card_prices", [])

    if not prices:
        return None

    raw_prices = prices[0]
    card_prices = {
        "card_id": to_int(raw_card.get("id")),
        "cardmarket_price": to_decimal(raw_prices.get("cardmarket_price")),
        "tcgplayer_price": to_decimal(raw_prices.get("tcgplayer_price")),
        "ebay_price": to_decimal(raw_prices.get("ebay_price")),
        "amazon_price": to_decimal(raw_prices.get("amazon_price")),
        "coolstuffinc_price": to_decimal(raw_prices.get("coolstuffinc_price")),
    }
    validate_required(card_prices, ("card_id",), "Card prices")
    return card_prices
