import unittest

from src.etl.data_quality import assert_no_blocking_issues, inspect_raw_cards
from src.etl.transform import classify_rarity


class RarityQualityTest(unittest.TestCase):
    def test_numeric_api_codes_are_not_loaded_as_rarities(self):
        self.assertEqual(classify_rarity("2"), (None, "invalid_numeric_source"))
        self.assertEqual(classify_rarity("3"), (None, "invalid_numeric_source"))

    def test_internal_api_labels_are_preserved_but_not_dimensional(self):
        self.assertEqual(classify_rarity("New artwork"), (None, "internal_api_label"))
        self.assertEqual(classify_rarity("Reprint"), (None, "internal_api_label"))

    def test_known_typo_is_normalized(self):
        self.assertEqual(
            classify_rarity("PLatinum Secret Rare"),
            ("Platinum Secret Rare", "normalized_typo"),
        )


class RawQualityTest(unittest.TestCase):
    def test_detects_nulls_duplicates_internal_codes_and_bad_prices(self):
        cards = [{
            "id": "1", "name": "Demo", "type": "Monster",
            "card_sets": [
                {"set_name": "Set", "set_code": "S-1", "set_rarity": "2", "set_price": "1"},
                {"set_name": "Set", "set_code": "S-1", "set_rarity": "2", "set_price": "bad"},
            ],
        }]
        issues = inspect_raw_cards(cards)
        self.assertEqual(issues["rarity.invalid_numeric_source"], 2)
        self.assertEqual(issues["card_printings.duplicate_grain"], 1)
        self.assertEqual(issues["card_printings.invalid_price"], 1)

    def test_blocking_issues_fail_validation(self):
        with self.assertRaisesRegex(ValueError, "duplicate_grain"):
            assert_no_blocking_issues({"card_printings.duplicate_grain": 1})
