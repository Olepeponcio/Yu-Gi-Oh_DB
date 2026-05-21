from src.etl.transform.common import to_decimal, to_int, validate_required


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
