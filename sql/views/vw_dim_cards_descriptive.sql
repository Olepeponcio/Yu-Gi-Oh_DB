CREATE OR REPLACE VIEW vw_dim_cards_descriptive AS
SELECT c.card_id,
c.name,
c.card_type,
c.human_readable_card_type,
c.frame_type,
c.race,
COALESCE(c.archetype, 'Sin arquetipo') AS archetype,
COALESCE(c.atk, 'No aplica') AS atk,
COALESCE(c.def, 'No aplica') AS def,
COALESCE(c.attribute, 'No aplica') AS attribute,
COALESCE(c.level, 'No aplica') AS level,
COALESCE(c.scale, 'No aplica') AS scale,
COALESCE(c.link_value, 'No aplica') AS link_value

FROM cards c;
