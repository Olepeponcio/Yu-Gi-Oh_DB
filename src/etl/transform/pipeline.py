from datetime import datetime

from src.etl.transform.cards import normalize_card, normalize_card_banlist, normalize_card_images
from src.etl.transform.common import deduplicate_rows
from src.etl.transform.prices import normalize_card_prices
from src.etl.transform.relations import normalize_card_linkmarkers, normalize_card_typelines
from src.etl.transform.sets import normalize_card_printings, normalize_rarity_types, normalize_sets


def transform_cards(raw_cards, snapshot_at=None, eur_usd_rate=None):
    if snapshot_at is None:
        snapshot_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tables = {
        "cards": [],
        "sets": [],
        "rarity_types": [],
        "card_printings": [],
        "card_images": [],
        "card_price_history": [],
        "card_banlist": [],
        "card_typelines": [],
        "card_linkmarkers": [],
    }

    for raw_card in raw_cards:
        tables["cards"].append(normalize_card(raw_card))
        tables["sets"].extend(normalize_sets(raw_card))
        tables["rarity_types"].extend(normalize_rarity_types(raw_card))
        tables["card_printings"].extend(normalize_card_printings(raw_card))
        tables["card_images"].extend(normalize_card_images(raw_card))

        tables["card_price_history"].extend(
            normalize_card_prices(raw_card, snapshot_at=snapshot_at, eur_usd_rate=eur_usd_rate)
        )

        banlist = normalize_card_banlist(raw_card)
        if banlist is not None:
            tables["card_banlist"].append(banlist)

        tables["card_typelines"].extend(normalize_card_typelines(raw_card))
        tables["card_linkmarkers"].extend(normalize_card_linkmarkers(raw_card))

    tables["sets"] = deduplicate_rows(tables["sets"], ("set_name",))
    tables["rarity_types"] = deduplicate_rows(tables["rarity_types"], ("rarity_name", "rarity_code"))

    return tables
