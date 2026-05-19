-- Consultas de calidad de datos.
-- Objetivo: validar integridad basica tras la ingesta desde YGOPRODeck.
-- Base esperada: yugioh_db.

USE yugioh_db;

-- 1. Conteo total por tabla.
SELECT 'cards' AS table_name, COUNT(*) AS row_count FROM cards
UNION ALL
SELECT 'card_sets', COUNT(*) FROM card_sets
UNION ALL
SELECT 'card_images', COUNT(*) FROM card_images
UNION ALL
SELECT 'card_prices', COUNT(*) FROM card_prices
UNION ALL
SELECT 'card_banlist', COUNT(*) FROM card_banlist
UNION ALL
SELECT 'card_typelines', COUNT(*) FROM card_typelines
UNION ALL
SELECT 'card_linkmarkers', COUNT(*) FROM card_linkmarkers;

-- 2. Campos obligatorios nulos o vacios.
SELECT
    COUNT(*) AS cards_with_required_data_issues
FROM cards
WHERE id IS NULL
   OR name IS NULL
   OR TRIM(name) = ''
   OR card_type IS NULL
   OR TRIM(card_type) = '';

-- 3. Duplicados logicos por nombre.
SELECT
    name,
    COUNT(*) AS duplicate_count
FROM cards
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, name;

-- 4. Tablas hijas sin carta padre.
SELECT 'card_sets' AS table_name, COUNT(*) AS orphan_rows
FROM card_sets cs
LEFT JOIN cards c ON c.id = cs.card_id
WHERE c.id IS NULL
UNION ALL
SELECT 'card_images', COUNT(*)
FROM card_images ci
LEFT JOIN cards c ON c.id = ci.card_id
WHERE c.id IS NULL
UNION ALL
SELECT 'card_prices', COUNT(*)
FROM card_prices cp
LEFT JOIN cards c ON c.id = cp.card_id
WHERE c.id IS NULL
UNION ALL
SELECT 'card_banlist', COUNT(*)
FROM card_banlist cb
LEFT JOIN cards c ON c.id = cb.card_id
WHERE c.id IS NULL
UNION ALL
SELECT 'card_typelines', COUNT(*)
FROM card_typelines ct
LEFT JOIN cards c ON c.id = ct.card_id
WHERE c.id IS NULL
UNION ALL
SELECT 'card_linkmarkers', COUNT(*)
FROM card_linkmarkers cl
LEFT JOIN cards c ON c.id = cl.card_id
WHERE c.id IS NULL;

-- 5. Cartas sin imagen o sin precios.
SELECT
    COUNT(*) AS cards_without_images
FROM cards c
LEFT JOIN card_images ci ON ci.card_id = c.id
WHERE ci.card_id IS NULL;

SELECT
    COUNT(*) AS cards_without_prices
FROM cards c
LEFT JOIN card_prices cp ON cp.card_id = c.id
WHERE cp.card_id IS NULL;

-- 6. Duplicados logicos en apariciones de sets.
SELECT
    card_id,
    set_name,
    set_code,
    set_rarity,
    COUNT(*) AS duplicate_count
FROM card_sets
GROUP BY card_id, set_name, set_code, set_rarity
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, card_id, set_name
LIMIT 50;

-- 7. Imagenes con URL principal ausente.
SELECT
    COUNT(*) AS images_without_main_url
FROM card_images
WHERE image_url IS NULL
   OR TRIM(image_url) = '';

-- 8. Precios completamente nulos.
SELECT
    COUNT(*) AS rows_without_any_price
FROM card_prices
WHERE cardmarket_price IS NULL
  AND tcgplayer_price IS NULL
  AND ebay_price IS NULL
  AND amazon_price IS NULL
  AND coolstuffinc_price IS NULL;

-- 9. Valores negativos en precios.
SELECT
    COUNT(*) AS rows_with_negative_prices
FROM card_prices
WHERE cardmarket_price < 0
   OR tcgplayer_price < 0
   OR ebay_price < 0
   OR amazon_price < 0
   OR coolstuffinc_price < 0;

-- 10. Posiciones duplicadas en listas normalizadas.
SELECT
    'card_typelines' AS table_name,
    card_id,
    position,
    COUNT(*) AS duplicate_count
FROM card_typelines
GROUP BY card_id, position
HAVING COUNT(*) > 1
UNION ALL
SELECT
    'card_linkmarkers',
    card_id,
    position,
    COUNT(*)
FROM card_linkmarkers
GROUP BY card_id, position
HAVING COUNT(*) > 1;
