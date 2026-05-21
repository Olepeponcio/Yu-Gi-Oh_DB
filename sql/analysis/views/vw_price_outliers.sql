CREATE OR REPLACE VIEW vw_price_outliers AS
SELECT
    c.id AS card_id,
    c.name,
    cs.set_name,
    r.rarity_name,
    cs.set_price
FROM card_sets cs
INNER JOIN cards c
    ON cs.card_id = c.id
INNER JOIN rarities r
    ON cs.rarity_id = r.id
WHERE cs.set_price >= 10000
ORDER BY cs.set_price DESC;