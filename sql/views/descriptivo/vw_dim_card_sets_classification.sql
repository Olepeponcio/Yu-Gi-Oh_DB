CREATE OR REPLACE VIEW vw_dim_card_sets_classification AS
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