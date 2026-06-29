-- detectar cartas muy reimpresas
-- interpretar disponibilidad
-- identificar cartas relevantes para revisar
-- Diagnóstico = explicar qué cartas destacan y por qué.
CREATE OR REPLACE VIEW vw_fact_card_set_coverage_diagnostic AS
SELECT
    c.card_id,
    c.name AS card_name,
    COUNT(cs.id) AS total_appearances,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    COUNT(DISTINCT cs.set_rarity) AS total_rarities
FROM cards c
JOIN card_sets cs
    ON c.card_id = cs.card_id
GROUP BY
    c.card_id,
    c.name
ORDER BY
    total_appearances DESC,
    total_sets DESC;
