-- entender distribucion general
-- validar si las cartas tienen o no apariciones
-- alimentar visuales descriptivos
CREATE OR REPLACE VIEW vw_fact_card_set_coverage_descriptive AS
SELECT
    c.card_id,
    c.name AS card_name,
    COUNT(cs.id) AS total_appearances,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    COUNT(DISTINCT cs.set_rarity) AS total_rarities
FROM cards c
LEFT JOIN card_sets cs
    ON c.card_id = cs.card_id
GROUP BY
    c.card_id,
    c.name
ORDER BY total_sets DESC, total_appearances DESC;
