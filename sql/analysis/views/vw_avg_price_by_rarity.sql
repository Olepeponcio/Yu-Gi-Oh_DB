CREATE OR REPLACE VIEW vw_price_by_rarity AS
SELECT
    r.id AS rarity_id,
    r.rarity_name,
    r.rarity_code,

    COUNT(cs.id) AS total_printings,
    COUNT(DISTINCT cs.card_id) AS total_cards,

    ROUND(AVG(cs.set_price), 2) AS avg_set_price,
    ROUND(MIN(cs.set_price), 2) AS min_set_price,
    ROUND(MAX(cs.set_price), 2) AS max_set_price,
    ROUND(SUM(cs.set_price), 2) AS total_market_value

FROM card_sets cs
INNER JOIN rarities r
    ON cs.rarity_id = r.id
WHERE cs.set_price IS NOT NULL
  AND cs.set_price > 0
  AND cs.set_price < 10000
GROUP BY
    r.id,
    r.rarity_name,
    r.rarity_code
ORDER BY avg_set_price DESC;