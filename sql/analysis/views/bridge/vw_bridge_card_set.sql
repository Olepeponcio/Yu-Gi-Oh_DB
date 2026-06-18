CREATE OR REPLACE VIEW vw_bridge_card_set AS
SELECT
    cs.id AS card_set_id,
    cs.card_id,
    cs.set_id,
    cs.rarity_id,
    cs.set_code,
    cs.set_name,
    cs.set_rarity,
    cs.set_rarity_code
FROM card_sets cs;