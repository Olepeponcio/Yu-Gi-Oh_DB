-- Distribución por tipo de carta
-- entender como se reparte el catalogo por tipo
CREATE OR REPLACE VIEW vw_dim_cards_classification AS
SELECT
	c.card_id, c.card_type,
    c.human_readable_card_type,
    c.frame_type,
    c.race,
    COALESCE(c.archetype, 'Sin arquetipo') AS archetype,
    COALESCE(c.attribute, 'No aplica') AS attribute,
    COUNT(*) AS total_cards
FROM cards c
GROUP BY
    c.card_type,
    c.human_readable_card_type,
    c.frame_type,
    c.race,
    COALESCE(c.archetype, 'Sin arquetipo'),
    COALESCE(c.attribute, 'No aplica')
ORDER BY
    c.card_type,
    c.human_readable_card_type,
    c.frame_type,
    c.race,
    archetype,
    attribute;