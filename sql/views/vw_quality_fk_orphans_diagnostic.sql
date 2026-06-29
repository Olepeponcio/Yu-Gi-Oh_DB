-- Calidad FK: filas hijas que apuntan a claves padre inexistentes.
-- Resultado esperado: issue_count = 0 en todas las relaciones.

CREATE OR REPLACE VIEW vw_quality_fk_orphans_diagnostic AS
SELECT
    'card_sets.card_id -> cards.card_id' AS relationship_name,
    COUNT(*) AS issue_count
FROM card_sets cs
LEFT JOIN cards c
    ON cs.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_images.card_id -> cards.card_id',
    COUNT(*)
FROM card_images ci
LEFT JOIN cards c
    ON ci.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_prices.card_id -> cards.card_id',
    COUNT(*)
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_price_history.card_id -> cards.card_id',
    COUNT(*)
FROM card_price_history cph
LEFT JOIN cards c
    ON cph.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_banlist.card_id -> cards.card_id',
    COUNT(*)
FROM card_banlist cb
LEFT JOIN cards c
    ON cb.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_typelines.card_id -> cards.card_id',
    COUNT(*)
FROM card_typelines ct
LEFT JOIN cards c
    ON ct.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_linkmarkers.card_id -> cards.card_id',
    COUNT(*)
FROM card_linkmarkers cl
LEFT JOIN cards c
    ON cl.card_id = c.card_id
WHERE c.card_id IS NULL

UNION ALL

SELECT
    'card_sets.set_id -> sets.id',
    COUNT(*)
FROM card_sets cs
LEFT JOIN sets s
    ON cs.set_id = s.id
WHERE cs.set_id IS NOT NULL
  AND s.id IS NULL

UNION ALL

SELECT
    'card_sets.rarity_id -> rarities.id',
    COUNT(*)
FROM card_sets cs
LEFT JOIN rarities r
    ON cs.rarity_id = r.id
WHERE cs.rarity_id IS NOT NULL
  AND r.id IS NULL;
