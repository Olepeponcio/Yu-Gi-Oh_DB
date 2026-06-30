CREATE OR REPLACE VIEW vw_dim_cards_descriptive AS
SELECT c.card_id,
c.name,
c.card_type,
c.human_readable_card_type,
c.frame_type,
c.race,
COALESCE(c.archetype, 'Sin arquetipo') AS archetype,
CAST(c.atk AS SIGNED) AS atk,
CAST(c.def AS SIGNED) AS def,
COALESCE(c.attribute, 'No aplica') AS attribute,
CAST(c.level AS SIGNED) AS level,
CAST(c.scale AS SIGNED) AS scale,
CAST(c.link_value AS SIGNED) AS link_value

FROM cards c;
