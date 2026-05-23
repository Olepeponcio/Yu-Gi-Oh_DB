-- Precio por rareza y codigo de impresion.

CREATE OR REPLACE VIEW vw_diag_price_by_rarity AS
SELECT
    r.id AS rarity_id,
    r.set_code,
    r.rarity_name,
    r.rarity_code,
    COUNT(cs.id) AS total_printings,
    COUNT(DISTINCT cs.card_id) AS total_cards,
    ROUND(AVG(cs.set_price), 2) AS avg_set_price,
    ROUND(MIN(cs.set_price), 2) AS min_set_price,
    ROUND(MAX(cs.set_price), 2) AS max_set_price,
    ROUND(SUM(cs.set_price), 2) AS total_market_value
FROM rarities r
INNER JOIN card_sets cs
    ON r.id = cs.rarity_id
WHERE cs.set_price IS NOT NULL
  AND cs.set_price > 0
GROUP BY
    r.id,
    r.set_code,
    r.rarity_name,
    r.rarity_code
ORDER BY
    avg_set_price DESC;
