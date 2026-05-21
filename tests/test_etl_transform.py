from decimal import Decimal
import unittest

from src.etl.transform import normalize_card, to_decimal, to_int, transform_cards


class TransformHelpersTest(unittest.TestCase):
    def test_to_int_converts_valid_values(self):
        self.assertEqual(to_int("12"), 12)
        self.assertEqual(to_int(7), 7)

    def test_to_int_returns_none_for_empty_or_invalid_values(self):
        self.assertIsNone(to_int(None))
        self.assertIsNone(to_int(""))
        self.assertIsNone(to_int("not-a-number"))

    def test_to_decimal_converts_valid_values(self):
        self.assertEqual(to_decimal("1.25"), Decimal("1.25"))
        self.assertEqual(to_decimal(3), Decimal("3"))

    def test_to_decimal_returns_none_for_empty_or_invalid_values(self):
        self.assertIsNone(to_decimal(None))
        self.assertIsNone(to_decimal(""))
        self.assertIsNone(to_decimal("bad-price"))


class NormalizeCardTest(unittest.TestCase):
    def test_normalize_card_maps_core_fields(self):
        raw_card = {
            "id": "123",
            "name": "Dark Magician",
            "type": "Normal Monster",
            "humanReadableCardType": "Normal Monster",
            "frameType": "normal",
            "desc": "The ultimate wizard.",
            "race": "Spellcaster",
            "archetype": "Dark Magician",
            "ygoprodeck_url": "https://example.test/card",
            "atk": "2500",
            "def": "2100",
            "attribute": "DARK",
            "level": "7",
        }

        card = normalize_card(raw_card)

        self.assertEqual(card["card_id"], 123)
        self.assertEqual(card["name"], "Dark Magician")
        self.assertEqual(card["card_type"], "Normal Monster")
        self.assertEqual(card["atk"], 2500)
        self.assertEqual(card["def"], 2100)
        self.assertEqual(card["level"], 7)

    def test_normalize_card_requires_id_name_and_type(self):
        with self.assertRaisesRegex(ValueError, "Card missing required fields"):
            normalize_card({"id": "123", "name": "Incomplete"})


class TransformCardsTest(unittest.TestCase):
    def test_transform_cards_builds_tables_and_deduplicates_dimensions(self):
        raw_cards = [
            build_raw_card(
                card_id=1,
                name="Card One",
                set_name="Starter Deck",
                rarity_name="Common",
                rarity_code="C",
            ),
            build_raw_card(
                card_id=2,
                name="Card Two",
                set_name="Starter Deck",
                rarity_name="Common",
                rarity_code="C",
            ),
        ]

        tables = transform_cards(raw_cards, snapshot_at="2026-05-21 07:30:00")

        self.assertEqual(len(tables["cards"]), 2)
        self.assertEqual(len(tables["sets"]), 1)
        self.assertEqual(len(tables["rarities"]), 1)
        self.assertEqual(len(tables["card_sets"]), 2)
        self.assertEqual(len(tables["card_images"]), 2)
        self.assertEqual(len(tables["card_prices"]), 2)
        self.assertEqual(len(tables["card_price_history"]), 2)
        self.assertEqual(tables["card_price_history"][0]["snapshot_at"], "2026-05-21 07:30:00")

    def test_transform_cards_includes_optional_child_tables(self):
        raw_card = build_raw_card(
            card_id=3,
            name="Link Card",
            typeline=["Cyberse", "Effect"],
            linkmarkers=["Top", "Bottom-Left"],
            banlist_info={"ban_tcg": "Limited", "ban_ocg": None, "ban_goat": None},
        )

        tables = transform_cards([raw_card], snapshot_at="2026-05-21 07:30:00")

        self.assertEqual(len(tables["card_banlist"]), 1)
        self.assertEqual(len(tables["card_typelines"]), 2)
        self.assertEqual(len(tables["card_linkmarkers"]), 2)
        self.assertEqual(tables["card_typelines"][0]["position"], 1)
        self.assertEqual(tables["card_linkmarkers"][1]["position"], 2)


def build_raw_card(
    card_id,
    name,
    set_name="Demo Set",
    rarity_name="Ultra Rare",
    rarity_code="UR",
    typeline=None,
    linkmarkers=None,
    banlist_info=None,
):
    return {
        "id": str(card_id),
        "name": name,
        "type": "Effect Monster",
        "card_sets": [
            {
                "set_name": set_name,
                "set_code": f"SET-{card_id}",
                "set_rarity": rarity_name,
                "set_rarity_code": rarity_code,
                "set_price": "0.25",
            }
        ],
        "card_images": [
            {
                "id": str(card_id * 10),
                "image_url": "https://example.test/image.jpg",
                "image_url_small": "https://example.test/image-small.jpg",
                "image_url_cropped": "https://example.test/image-cropped.jpg",
            }
        ],
        "card_prices": [
            {
                "cardmarket_price": "1.10",
                "tcgplayer_price": "1.20",
                "ebay_price": "1.30",
                "amazon_price": "1.40",
                "coolstuffinc_price": "1.50",
            }
        ],
        "typeline": typeline or [],
        "linkmarkers": linkmarkers or [],
        "banlist_info": banlist_info,
    }


if __name__ == "__main__":
    unittest.main()
