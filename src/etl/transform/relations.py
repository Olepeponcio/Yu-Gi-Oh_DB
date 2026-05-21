from src.etl.transform.common import to_int, validate_required


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
