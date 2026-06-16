SELECT
    c.name,
    cs.set_code,
    r.rarity_name,
    r.rarity_code
FROM card_sets cs
JOIN cards c
    ON cs.card_id = c.card_id
JOIN rarities r
    ON cs.rarity_id = r.id;