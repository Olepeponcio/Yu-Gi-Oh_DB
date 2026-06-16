CREATE OR REPLACE VIEW vw_dim_card AS
SELECT
    c.card_id,
    c.name,
    c.card_type,
    c.human_readable_card_type,
    c.frame_type,
    c.race,
    c.archetype,
    c.attribute,
    c.level,
    c.atk,
    c.def,
    c.link_value
FROM cards c;
