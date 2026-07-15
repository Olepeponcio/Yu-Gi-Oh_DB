from src.etl.transform.common import to_decimal, to_int, validate_required

INTERNAL_API_RARITY_LABELS = {
    "new", "reprint", "new artwork", "european debut", "oceanian debut",
    "european & oceanian debut", "force-smw",
}

RARITY_TYPO_NORMALIZATION = {
    "PLatinum Secret Rare": "Platinum Secret Rare",
    "Cr": "Collector's Rare",
    "Extra Secret": "Extra Secret Rare",
    "Starfoil": "Starfoil Rare",
    "Duel Terminal Normal Rare Parallel Rare": "Duel Terminal Normal Parallel Rare",
}


def classify_rarity(raw_name):
    if raw_name is None or not str(raw_name).strip():
        return None, "missing"
    raw_name = str(raw_name).strip()
    if raw_name.isdigit():
        return None, "invalid_numeric_source"
    if raw_name.casefold() in INTERNAL_API_RARITY_LABELS:
        return None, "internal_api_label"
    if raw_name in RARITY_TYPO_NORMALIZATION:
        return RARITY_TYPO_NORMALIZATION[raw_name], "normalized_typo"
    return raw_name, "valid"


def normalize_card_printings(raw_card):
    card_id = to_int(raw_card.get("id"))
    rows = []
    for raw_set in raw_card.get("card_sets", []):
        rarity_name, quality = classify_rarity(raw_set.get("set_rarity"))
        row = {
            "card_id": card_id,
            "set_name": raw_set.get("set_name"),
            "set_code": raw_set.get("set_code"),
            "raw_rarity_name": str(raw_set.get("set_rarity") or ""),
            "raw_rarity_code": raw_set.get("set_rarity_code") or "",
            "rarity_name": rarity_name,
            "rarity_code": raw_set.get("set_rarity_code") or "",
            "rarity_source_quality": quality,
            "set_price_usd": to_decimal(raw_set.get("set_price")),
        }
        validate_required(row, ("card_id", "set_name", "set_code"), "Card printing")
        rows.append(row)
    return rows


def normalize_sets(raw_card):
    rows = []
    for raw_set in raw_card.get("card_sets", []):
        row = {"set_name": raw_set.get("set_name")}
        validate_required(row, ("set_name",), "Set")
        rows.append(row)
    return rows


def normalize_rarity_types(raw_card):
    rows = []
    for raw_set in raw_card.get("card_sets", []):
        rarity_name, quality = classify_rarity(raw_set.get("set_rarity"))
        if rarity_name is not None:
            rows.append({
                "rarity_name": rarity_name,
                "rarity_code": raw_set.get("set_rarity_code") or "",
                "rarity_source_quality": quality,
            })
    return rows


normalize_card_sets = normalize_card_printings
normalize_rarities = normalize_rarity_types
