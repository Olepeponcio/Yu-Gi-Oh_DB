-- Relacion entre rareza y precio de aparicion
-- analizar si ciertas rarezas aparecen asociadas a precios distintos.
-- No agrupar por cs.set_price si quieres calcular estadísticos.
CREATE OR REPLACE VIEW vw_fact_rarity_price_summary_diagnostic AS
SELECT
    COALESCE(r.rarity_name, cs.set_rarity) AS rarity_name,
    COUNT(*) AS total_appearances,
    COUNT(DISTINCT cs.card_id) AS total_cards,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    AVG(cs.set_price) AS avg_set_price,
    MIN(cs.set_price) AS min_set_price,
    MAX(cs.set_price) AS max_set_price
FROM card_sets cs
LEFT JOIN rarities r
    ON cs.rarity_id = r.id
WHERE cs.set_price IS NOT NULL
GROUP BY
    COALESCE(r.rarity_name, cs.set_rarity);
