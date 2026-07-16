CREATE OR REPLACE VIEW vw_fact_card_printings AS
SELECT 
cp.printing_id,
cp.card_id,
cp.set_id,
cp.rarity_id,
cp.raw_rarity_name AS rarity_name,
cp.raw_rarity_code AS rarity_code,
cp.set_code,
cp.set_price_usd AS set_price
FROM card_printings cp
WHERE cp.rarity_source_quality IN ("valid")
ORDER BY rarity_name, cp.set_price_usd DESC;