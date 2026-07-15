from collections import Counter

from src.etl.transform.sets import classify_rarity


def inspect_raw_cards(raw_cards):
    issues = Counter()
    seen_cards = set()
    seen_printings = set()

    for card in raw_cards:
        card_id = card.get("id")
        if card_id in (None, ""):
            issues["cards.missing_id"] += 1
        elif card_id in seen_cards:
            issues["cards.duplicate_id"] += 1
        seen_cards.add(card_id)

        if not card.get("name"):
            issues["cards.missing_name"] += 1
        if not card.get("type"):
            issues["cards.missing_type"] += 1

        for printing in card.get("card_sets", []):
            for field in ("set_name", "set_code", "set_rarity", "set_price"):
                if printing.get(field) in (None, ""):
                    issues[f"card_printings.missing_{field}"] += 1

            key = (
                card_id,
                printing.get("set_code"),
                printing.get("set_rarity"),
                printing.get("set_rarity_code") or "",
            )
            if key in seen_printings:
                issues["card_printings.duplicate_grain"] += 1
            seen_printings.add(key)

            _, quality = classify_rarity(printing.get("set_rarity"))
            if quality != "valid":
                issues[f"rarity.{quality}"] += 1

            try:
                if float(printing.get("set_price")) < 0:
                    issues["card_printings.negative_price"] += 1
            except (TypeError, ValueError):
                issues["card_printings.invalid_price"] += 1

    return dict(sorted(issues.items()))


def assert_no_blocking_issues(issues):
    blocking = {
        key: value for key, value in issues.items()
        if value and (
            key.startswith("cards.")
            or key.startswith("card_printings.missing_")
            or key in {"card_printings.duplicate_grain", "card_printings.negative_price", "card_printings.invalid_price"}
        )
    }
    if blocking:
        raise ValueError(f"Blocking data quality issues: {blocking}")
