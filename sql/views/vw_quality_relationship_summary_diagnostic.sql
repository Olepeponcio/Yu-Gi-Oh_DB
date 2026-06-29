-- Calidad de relaciones: resumen de cobertura de tablas hijas.
-- Sirve para revisar volumen de filas hijas y claves padre usadas.

CREATE OR REPLACE VIEW vw_quality_relationship_summary_diagnostic AS
SELECT
    'cards' AS parent_table,
    'card_sets' AS child_table,
    COUNT(*) AS child_rows,
    COUNT(DISTINCT card_id) AS parent_keys_used
FROM card_sets

UNION ALL

SELECT
    'cards',
    'card_images',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_images

UNION ALL

SELECT
    'cards',
    'card_prices',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_prices

UNION ALL

SELECT
    'cards',
    'card_price_history',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_price_history

UNION ALL

SELECT
    'cards',
    'card_banlist',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_banlist

UNION ALL

SELECT
    'cards',
    'card_typelines',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_typelines

UNION ALL

SELECT
    'cards',
    'card_linkmarkers',
    COUNT(*),
    COUNT(DISTINCT card_id)
FROM card_linkmarkers;
