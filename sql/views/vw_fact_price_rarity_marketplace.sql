CREATE OR REPLACE VIEW vw_fact_price_rarity_marketplace AS
SELECT
    p.card_id,
    a.rarity_id,
    p.marketplace,
    p.currency,
    AVG(p.price) AS avg_price,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price,
    COUNT(*) AS rows_count
FROM vw_fact_card_prices_descriptive p
INNER JOIN vw_fact_card_set_appearances a
    ON p.card_id = a.card_id
WHERE
    a.rarity_id IS NOT NULL
    AND p.price IS NOT NULL
    AND p.price > 0
GROUP BY
    p.card_id,
    a.rarity_id,
    p.marketplace,
    p.currency;