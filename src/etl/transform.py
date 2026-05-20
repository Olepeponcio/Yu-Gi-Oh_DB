from decimal import Decimal, InvalidOperation
from datetime import datetime


def to_int(value):
    if value is None or value == "":
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_decimal(value):
    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def normalize_card(raw_card):
    card = {
        "id": to_int(raw_card.get("id")),
        "name": raw_card.get("name"),
        "card_type": raw_card.get("type"),
        "human_readable_card_type": raw_card.get("humanReadableCardType"),
        "frame_type": raw_card.get("frameType"),
        "description": raw_card.get("desc"),
        "race": raw_card.get("race"),
        "archetype": raw_card.get("archetype"),
        "ygoprodeck_url": raw_card.get("ygoprodeck_url"),
        "atk": to_int(raw_card.get("atk")),
        "def": to_int(raw_card.get("def")),
        "attribute": raw_card.get("attribute"),
        "level": to_int(raw_card.get("level")),
        "scale": to_int(raw_card.get("scale")),
        "pendulum_description": raw_card.get("pend_desc"),
        "monster_description": raw_card.get("monster_desc"),
        "link_value": to_int(raw_card.get("linkval")),
    }
    validate_required(card, ("id", "name", "card_type"), "Card")
    return card


def normalize_card_sets(raw_card):
    card_id = to_int(raw_card.get("id"))
    sets = []

    for raw_set in raw_card.get("card_sets", []):
        card_set = {
            "card_id": card_id,
            "set_name": raw_set.get("set_name"),
            "set_code": raw_set.get("set_code"),
            "set_rarity": raw_set.get("set_rarity"),
            "set_rarity_code": raw_set.get("set_rarity_code"),
            "set_price": to_decimal(raw_set.get("set_price")),
        }
        validate_required(card_set, ("card_id", "set_name"), "Card set")
        sets.append(card_set)

    return sets


def normalize_sets(raw_card):
    sets = []

    for raw_set in raw_card.get("card_sets", []):
        card_set = {
            "set_name": raw_set.get("set_name"),
        }
        validate_required(card_set, ("set_name",), "Set")
        sets.append(card_set)

    return sets


def normalize_rarities(raw_card):
    rarities = []

    for raw_set in raw_card.get("card_sets", []):
        if raw_set.get("set_rarity") is None:
            continue

        rarity = {
            "rarity_name": raw_set.get("set_rarity"),
            "rarity_code": raw_set.get("set_rarity_code") or "",
        }
        validate_required(rarity, ("rarity_name",), "Rarity")
        rarities.append(rarity)

    return rarities


def normalize_card_images(raw_card):
    card_id = to_int(raw_card.get("id"))
    images = []

    for raw_image in raw_card.get("card_images", []):
        image = {
            "image_id": to_int(raw_image.get("id")),
            "card_id": card_id,
            "image_url": raw_image.get("image_url"),
            "image_url_small": raw_image.get("image_url_small"),
            "image_url_cropped": raw_image.get("image_url_cropped"),
        }
        validate_required(image, ("image_id", "card_id"), "Card image")
        images.append(image)

    return images


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


def normalize_card_banlist(raw_card):
    banlist = raw_card.get("banlist_info")

    if not banlist:
        return None

    card_banlist = {
        "card_id": to_int(raw_card.get("id")),
        "ban_tcg": banlist.get("ban_tcg"),
        "ban_ocg": banlist.get("ban_ocg"),
        "ban_goat": banlist.get("ban_goat"),
    }
    validate_required(card_banlist, ("card_id",), "Card banlist")
    return card_banlist


def normalize_card_typelines(raw_card):
    card_id = to_int(raw_card.get("id"))
    typelines = []

    for position, typeline in enumerate(raw_card.get("typeline", []), start=1):
        item = {
            "card_id": card_id,
            "typeline": typeline,
            "position": position,
        }
        validate_required(item, ("card_id", "typeline", "position"), "Card typeline")
        typelines.append(item)

    return typelines


def normalize_card_linkmarkers(raw_card):
    card_id = to_int(raw_card.get("id"))
    linkmarkers = []

    for position, linkmarker in enumerate(raw_card.get("linkmarkers", []), start=1):
        item = {
            "card_id": card_id,
            "linkmarker": linkmarker,
            "position": position,
        }
        validate_required(item, ("card_id", "linkmarker", "position"), "Card linkmarker")
        linkmarkers.append(item)

    return linkmarkers


def deduplicate_rows(rows, key_fields):
    deduplicated = {}

    for row in rows:
        key = tuple(row.get(field) for field in key_fields)
        deduplicated[key] = row

    return list(deduplicated.values())


def transform_cards(raw_cards, snapshot_at=None):
    if snapshot_at is None:
        snapshot_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tables = {
        "cards": [],
        "sets": [],
        "rarities": [],
        "card_sets": [],
        "card_images": [],
        "card_prices": [],
        "card_price_history": [],
        "card_banlist": [],
        "card_typelines": [],
        "card_linkmarkers": [],
    }

    for raw_card in raw_cards:
        tables["cards"].append(normalize_card(raw_card))
        tables["sets"].extend(normalize_sets(raw_card))
        tables["rarities"].extend(normalize_rarities(raw_card))
        tables["card_sets"].extend(normalize_card_sets(raw_card))
        tables["card_images"].extend(normalize_card_images(raw_card))

        prices = normalize_card_prices(raw_card)
        if prices is not None:
            tables["card_prices"].append(prices)
            tables["card_price_history"].append({**prices, "snapshot_at": snapshot_at})

        banlist = normalize_card_banlist(raw_card)
        if banlist is not None:
            tables["card_banlist"].append(banlist)

        tables["card_typelines"].extend(normalize_card_typelines(raw_card))
        tables["card_linkmarkers"].extend(normalize_card_linkmarkers(raw_card))

    tables["sets"] = deduplicate_rows(tables["sets"], ("set_name",))
    tables["rarities"] = deduplicate_rows(tables["rarities"], ("rarity_name", "rarity_code"))

    return tables


def validate_required(row, required_fields, label):
    missing_fields = [field for field in required_fields if row.get(field) is None]

    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise ValueError(f"{label} missing required fields: {joined_fields}")
