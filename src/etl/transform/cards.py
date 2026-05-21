from src.etl.transform.common import to_int, validate_required


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
