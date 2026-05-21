-- 3. Arquetipos con alta demanda
-- Proxy: arquetipos con muchas cartas, muchas impresiones y precio medio alto

CREATE OR REPLACE VIEW vw_high_demand_archetypes AS
SELECT
    c.archetype,
    COUNT(DISTINCT c.id) AS total_cards,
    COUNT(cs.id) AS total_printings,
    ROUND(AVG(cs.set_price), 2) AS avg_set_price,
    ROUND(MAX(cs.set_price), 2) AS max_set_price,
    ROUND(SUM(cs.set_price), 2) AS estimated_market_weight
FROM cards c
INNER JOIN card_sets cs
    ON c.id = cs.card_id
WHERE c.archetype IS NOT NULL
  AND c.archetype <> ''
  AND cs.set_price IS NOT NULL
GROUP BY c.archetype
HAVING
    total_cards >= 3
    AND total_printings >= 5
ORDER BY
    estimated_market_weight DESC,
    avg_set_price DESC;