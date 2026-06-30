-- Hecho BI: apariciones de cartas en sets.
-- 1 fila = 1 aparicion carta + set + rareza.

CREATE OR REPLACE VIEW vw_fact_card_set_appearances AS
SELECT
    cs.id AS card_set_appearance_id,
    cs.card_id,
    c.name AS card_name,
    cs.set_id,
    COALESCE(s.set_name, cs.set_name) AS set_name,
    cs.rarity_id,
    COALESCE(NULLIF(r.rarity_name, ''), cs.set_rarity) AS rarity_name,
    COALESCE(NULLIF(r.rarity_code, ''), cs.set_rarity_code) AS rarity_code,
    cs.set_code,
    cs.set_price,
    1 AS appearance_count
FROM card_sets cs
LEFT JOIN cards c
    ON cs.card_id = c.card_id
LEFT JOIN sets s
    ON cs.set_id = s.id
LEFT JOIN rarities r
    ON cs.rarity_id = r.id;
