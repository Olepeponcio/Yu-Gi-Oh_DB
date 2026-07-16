CREATE OR REPLACE VIEW vw_dim_cards AS
SELECT 
c.card_id,
c.name AS card_name,
c.human_readable_card_type AS card_type,
c.frame_type,
c.race,
c.archetype,
c.attribute,
c.atk,
c.def,
c.level AS card_level,
c.scale AS card_scale,
c.link_value

FROM cards c;