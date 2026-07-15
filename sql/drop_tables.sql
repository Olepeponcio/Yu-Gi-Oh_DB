SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS card_banlist;
DROP TABLE IF EXISTS card_images;
DROP TABLE IF EXISTS card_linkmarkers;
DROP TABLE IF EXISTS card_printings;
DROP TABLE IF EXISTS card_typelines;
DROP TABLE IF EXISTS card_price_history;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS rarity_types;
DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS marketplaces;
DROP TABLE IF EXISTS currencies;
-- Compatibilidad de limpieza con el esquema anterior.
DROP TABLE IF EXISTS card_prices;
DROP TABLE IF EXISTS card_sets;
DROP TABLE IF EXISTS rarities;
SET FOREIGN_KEY_CHECKS = 1;
