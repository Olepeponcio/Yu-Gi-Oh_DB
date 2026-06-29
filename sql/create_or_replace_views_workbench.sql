-- create_or_replace_views_workbench.sql
-- Crea o reemplaza todas las views de consumo dentro de yugioh_db.
-- Version compatible con hoja SQL / MySQL Workbench: no usa SOURCE.
--
-- Mantenimiento:
--   - Las views fuente viven como archivos independientes en sql/views/.
--   - Si se modifica una view individual, regenerar o copiar aqui su definicion.

SET NAMES utf8mb4;

USE `yugioh_db`;

-- ============================================================
-- sql\views\vw_dim_cards_descriptive.sql
-- ============================================================
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

-- ============================================================
-- sql\views\vw_dim_sets_descriptive.sql
-- ============================================================
-- Dimension BI: catalogo de sets.
-- 1 fila = 1 set.

CREATE OR REPLACE VIEW vw_dim_sets_descriptive AS
SELECT
    s.id AS set_id,
    s.set_name,
    s.created_at,
    s.updated_at
FROM sets s;

-- ============================================================
-- sql\views\vw_dim_rarities_descriptive.sql
-- ============================================================
-- Dimension BI: catalogo de rarezas.
-- 1 fila = 1 rareza por codigo de impresion.

CREATE OR REPLACE VIEW vw_dim_rarities_descriptive AS
SELECT
    r.id AS rarity_id,
    r.set_code,
    r.rarity_name,
    r.rarity_code,
    CONCAT(r.set_code, '|', r.rarity_name, '|', r.rarity_code) AS rarity_business_key,
    r.created_at,
    r.updated_at
FROM rarities r;

-- ============================================================
-- sql\views\vw_dim_rarity_names_descriptive.sql
-- ============================================================
-- Dimension BI: nombres de rareza usados en analisis agregado.
-- 1 fila = 1 rarity_name.

CREATE OR REPLACE VIEW vw_dim_rarity_names_descriptive AS
SELECT
    rarity_name,
    COUNT(*) AS rarity_catalog_rows,
    COUNT(DISTINCT set_code) AS total_set_codes,
    COUNT(DISTINCT rarity_code) AS total_rarity_codes
FROM rarities
GROUP BY
    rarity_name;

-- ============================================================
-- sql\views\vw_dim_marketplaces_descriptive.sql
-- ============================================================
-- Dimension BI: fuentes de precio.
-- 1 fila = 1 marketplace.

CREATE OR REPLACE VIEW vw_dim_marketplaces_descriptive AS
SELECT
    'cardmarket' AS marketplace,
    'Cardmarket' AS marketplace_name,
    'EUR' AS default_currency,
    'Europe' AS market_region

UNION ALL

SELECT
    'tcgplayer',
    'TCGplayer',
    'USD',
    'United States'

UNION ALL

SELECT
    'ebay',
    'eBay',
    'USD',
    'Global'

UNION ALL

SELECT
    'amazon',
    'Amazon',
    'USD',
    'Global'

UNION ALL

SELECT
    'coolstuffinc',
    'CoolStuffInc',
    'USD',
    'United States';

-- ============================================================
-- sql\views\vw_dim_currencies_descriptive.sql
-- ============================================================
-- Dimension BI: monedas declaradas en las vistas de precios.
-- 1 fila = 1 moneda.

CREATE OR REPLACE VIEW vw_dim_currencies_descriptive AS
SELECT
    'EUR' AS currency,
    'Euro' AS currency_name,
    'EUR' AS currency_symbol_text

UNION ALL

SELECT
    'USD',
    'US Dollar',
    'USD';

-- ============================================================
-- sql\views\vw_dim_snapshots_descriptive.sql
-- ============================================================
-- Dimension BI: fechas de snapshots de precios.
-- 1 fila = 1 snapshot_at disponible en el historico.

CREATE OR REPLACE VIEW vw_dim_snapshots_descriptive AS
SELECT
    cph.snapshot_at,
    DATE(cph.snapshot_at) AS snapshot_date,
    YEAR(cph.snapshot_at) AS snapshot_year,
    QUARTER(cph.snapshot_at) AS snapshot_quarter,
    MONTH(cph.snapshot_at) AS snapshot_month,
    MONTHNAME(cph.snapshot_at) AS snapshot_month_name,
    DAY(cph.snapshot_at) AS snapshot_day,
    HOUR(cph.snapshot_at) AS snapshot_hour,
    DAYOFWEEK(cph.snapshot_at) AS snapshot_day_of_week
FROM card_price_history cph
GROUP BY
    cph.snapshot_at;

-- ============================================================
-- sql\views\vw_fact_card_set_coverage_descriptive.sql
-- ============================================================
-- entender distribucion general
-- validar si las cartas tienen o no apariciones
-- alimentar visuales descriptivos
CREATE OR REPLACE VIEW vw_fact_card_set_coverage_descriptive AS
SELECT
    c.card_id,
    c.name AS card_name,
    COUNT(cs.id) AS total_appearances,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    COUNT(DISTINCT cs.set_rarity) AS total_rarities
FROM cards c
LEFT JOIN card_sets cs
    ON c.card_id = cs.card_id
GROUP BY
    c.card_id,
    c.name
ORDER BY total_sets DESC, total_appearances DESC;

-- ============================================================
-- sql\views\vw_fact_card_prices_descriptive.sql
-- ============================================================
-- describir precios actuales por marketplace.
-- separar marketplaces y declarar moneda

CREATE OR REPLACE VIEW vw_fact_card_prices_descriptive AS
SELECT
    c.card_id,
    c.name AS card_name,
    'cardmarket' AS marketplace,
    'EUR' AS currency,
    cp.cardmarket_price AS price
FROM card_prices cp
LEFT JOIN cards c ON cp.card_id = c.card_id
WHERE cp.cardmarket_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'tcgplayer' AS marketplace,
    'USD' AS currency,
    cp.tcgplayer_price AS price
FROM card_prices cp
LEFT JOIN cards c ON cp.card_id = c.card_id
WHERE cp.tcgplayer_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'ebay' AS marketplace,
    'USD' AS currency,
    cp.ebay_price AS price
FROM card_prices cp
LEFT JOIN cards c ON cp.card_id = c.card_id
WHERE cp.ebay_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'amazon' AS marketplace,
    'USD' AS currency,
    cp.amazon_price AS price
FROM card_prices cp
LEFT JOIN cards c ON cp.card_id = c.card_id
WHERE cp.amazon_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'coolstuffinc' AS marketplace,
    'USD' AS currency,
    cp.coolstuffinc_price AS price
FROM card_prices cp
LEFT JOIN cards c ON cp.card_id = c.card_id
WHERE cp.coolstuffinc_price IS NOT NULL;

-- ============================================================
-- sql\views\vw_fact_card_set_coverage_diagnostic.sql
-- ============================================================
-- detectar cartas muy reimpresas
-- interpretar disponibilidad
-- identificar cartas relevantes para revisar
-- Diagnóstico = explicar qué cartas destacan y por qué.
CREATE OR REPLACE VIEW vw_fact_card_set_coverage_diagnostic AS
SELECT
    c.card_id,
    c.name AS card_name,
    COUNT(cs.id) AS total_appearances,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    COUNT(DISTINCT cs.set_rarity) AS total_rarities
FROM cards c
JOIN card_sets cs
    ON c.card_id = cs.card_id
GROUP BY
    c.card_id,
    c.name
ORDER BY
    total_appearances DESC,
    total_sets DESC;

-- ============================================================
-- sql\views\vw_fact_current_prices_diagnostic.sql
-- ============================================================
-- vista base para explorar outliers entre tablas
-- 1 fila = 1 carta + 1 fuente de precio + 1 moneda


CREATE OR REPLACE VIEW vw_fact_current_prices_diagnostic AS
SELECT
    c.card_id,
    c.name AS card_name,
    'cardmarket' AS price_source,
    'EUR' AS currency,
    cp.cardmarket_price AS price
FROM card_prices cp
JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.cardmarket_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'tcgplayer' AS price_source,
    'USD' AS currency,
    cp.tcgplayer_price AS price
FROM card_prices cp
JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.tcgplayer_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'ebay' AS price_source,
    'USD' AS currency,
    cp.ebay_price AS price
FROM card_prices cp
JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.ebay_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'amazon' AS price_source,
    'USD' AS currency,
    cp.amazon_price AS price
FROM card_prices cp
JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.amazon_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'coolstuffinc' AS price_source,
    'USD' AS currency,
    cp.coolstuffinc_price AS price
FROM card_prices cp
JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.coolstuffinc_price IS NOT NULL;

-- ============================================================
-- sql\views\vw_fact_price_outlier_candidates_diagnostic.sql
-- ============================================================
-- vista de extremos sobre la vista base

CREATE OR REPLACE VIEW vw_fact_price_outlier_candidates_diagnostic AS
SELECT
    card_id,
    card_name,
    price_source,
    currency,
    price,
    CASE
        WHEN price <= 0 THEN 'REVISAR_PRECIO_CERO'
        WHEN currency = 'EUR' AND price >= 50 THEN 'REVISAR_PRECIO_ALTO_EUR'
        WHEN currency = 'USD' AND price >= 50 THEN 'REVISAR_PRECIO_ALTO_USD'
        ELSE 'OK'
    END AS review_flag
FROM vw_fact_current_prices_diagnostic
WHERE
    price <= 0
    OR (currency = 'EUR' AND price >= 50)
    OR (currency = 'USD' AND price >= 50);

-- ============================================================
-- sql\views\vw_fact_rarity_price_summary_diagnostic.sql
-- ============================================================
-- Relacion entre rareza y precio de aparicion
-- analizar si ciertas rarezas aparecen asociadas a precios distintos.
-- No agrupar por cs.set_price si quieres calcular estadísticos.
CREATE OR REPLACE VIEW vw_fact_rarity_price_summary_diagnostic AS
SELECT
    COALESCE(r.rarity_name, cs.set_rarity) AS rarity_name,
    COUNT(*) AS total_appearances,
    COUNT(DISTINCT cs.card_id) AS total_cards,
    COUNT(DISTINCT cs.set_name) AS total_sets,
    AVG(cs.set_price) AS avg_set_price,
    MIN(cs.set_price) AS min_set_price,
    MAX(cs.set_price) AS max_set_price
FROM card_sets cs
LEFT JOIN rarities r
    ON cs.rarity_id = r.id
WHERE cs.set_price IS NOT NULL
GROUP BY
    COALESCE(r.rarity_name, cs.set_rarity);

-- ============================================================
-- sql\views\vw_quality_duplicate_grain_diagnostic.sql
-- ============================================================
-- Calidad de grano: duplicados en apariciones carta + set + rareza.
-- Resultado esperado: sin filas.

CREATE OR REPLACE VIEW vw_quality_duplicate_grain_diagnostic AS
SELECT
    card_id,
    set_name,
    set_code,
    set_rarity,
    set_rarity_code,
    COUNT(*) AS duplicate_count
FROM card_sets
GROUP BY
    card_id,
    set_name,
    set_code,
    set_rarity,
    set_rarity_code
HAVING COUNT(*) > 1;

-- ============================================================
-- sql\views\vw_quality_fk_orphans_diagnostic.sql
-- ============================================================
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

-- ============================================================
-- sql\views\vw_quality_nullable_fk_diagnostic.sql
-- ============================================================
-- Calidad FK: claves foraneas opcionales sin resolver.
-- No siempre es error; sirve como aviso previo a visualizacion.

CREATE OR REPLACE VIEW vw_quality_nullable_fk_diagnostic AS
SELECT
    'card_sets.set_id nullable' AS check_name,
    COUNT(*) AS affected_rows
FROM card_sets
WHERE set_id IS NULL

UNION ALL

SELECT
    'card_sets.rarity_id nullable',
    COUNT(*)
FROM card_sets
WHERE rarity_id IS NULL;

-- ============================================================
-- sql\views\vw_quality_relationship_summary_diagnostic.sql
-- ============================================================
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

-- ============================================================
-- sql\views\vw_fact_price_snapshot_summary_predictive.sql
-- ============================================================
-- Predictivo: comprobar si existe historico suficiente para analizar variacion.
-- 1 fila = 1 snapshot de precios.
-- La view se actualiza logicamente al consultar; los snapshots los inserta el ETL en card_price_history.

CREATE OR REPLACE VIEW vw_fact_price_snapshot_summary_predictive AS
SELECT
    snapshot_at,
    COUNT(*) AS total_price_rows,
    COUNT(DISTINCT card_id) AS total_cards,
    SUM(CASE WHEN cardmarket_price IS NOT NULL THEN 1 ELSE 0 END) AS cardmarket_price_rows,
    SUM(CASE WHEN tcgplayer_price IS NOT NULL THEN 1 ELSE 0 END) AS tcgplayer_price_rows,
    SUM(CASE WHEN ebay_price IS NOT NULL THEN 1 ELSE 0 END) AS ebay_price_rows,
    SUM(CASE WHEN amazon_price IS NOT NULL THEN 1 ELSE 0 END) AS amazon_price_rows,
    SUM(CASE WHEN coolstuffinc_price IS NOT NULL THEN 1 ELSE 0 END) AS coolstuffinc_price_rows,
    MIN(cardmarket_price) AS min_cardmarket_price_eur,
    MAX(cardmarket_price) AS max_cardmarket_price_eur,
    AVG(cardmarket_price) AS avg_cardmarket_price_eur,
    MIN(tcgplayer_price) AS min_tcgplayer_price_usd,
    MAX(tcgplayer_price) AS max_tcgplayer_price_usd,
    AVG(tcgplayer_price) AS avg_tcgplayer_price_usd,
    MIN(ebay_price) AS min_ebay_price_usd,
    MAX(ebay_price) AS max_ebay_price_usd,
    AVG(ebay_price) AS avg_ebay_price_usd,
    MIN(amazon_price) AS min_amazon_price_usd,
    MAX(amazon_price) AS max_amazon_price_usd,
    AVG(amazon_price) AS avg_amazon_price_usd,
    MIN(coolstuffinc_price) AS min_coolstuffinc_price_usd,
    MAX(coolstuffinc_price) AS max_coolstuffinc_price_usd,
    AVG(coolstuffinc_price) AS avg_coolstuffinc_price_usd
FROM card_price_history
GROUP BY
    snapshot_at;

-- ============================================================
-- sql\views\vw_fact_card_price_variation_predictive.sql
-- ============================================================
-- Predictivo: medir cambios de precio por carta entre snapshots consecutivos.
-- 1 fila = 1 carta + 1 marketplace + 1 moneda + 1 snapshot con snapshot anterior comparable.
-- Requiere MySQL 8+ por uso de LAG().

CREATE OR REPLACE VIEW vw_fact_card_price_variation_predictive AS
WITH price_history_long AS (
    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'cardmarket' AS marketplace,
        'EUR' AS currency,
        cph.cardmarket_price AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.cardmarket_price IS NOT NULL

    UNION ALL

    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'tcgplayer' AS marketplace,
        'USD' AS currency,
        cph.tcgplayer_price AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.tcgplayer_price IS NOT NULL

    UNION ALL

    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'ebay' AS marketplace,
        'USD' AS currency,
        cph.ebay_price AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.ebay_price IS NOT NULL

    UNION ALL

    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'amazon' AS marketplace,
        'USD' AS currency,
        cph.amazon_price AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.amazon_price IS NOT NULL

    UNION ALL

    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'coolstuffinc' AS marketplace,
        'USD' AS currency,
        cph.coolstuffinc_price AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.coolstuffinc_price IS NOT NULL
),
price_history_with_previous AS (
    SELECT
        card_id,
        card_name,
        marketplace,
        currency,
        snapshot_at,
        price,
        LAG(snapshot_at) OVER (
            PARTITION BY card_id, marketplace, currency
            ORDER BY snapshot_at
        ) AS previous_snapshot_at,
        LAG(price) OVER (
            PARTITION BY card_id, marketplace, currency
            ORDER BY snapshot_at
        ) AS previous_price
    FROM price_history_long
)
SELECT
    card_id,
    card_name,
    marketplace,
    currency,
    snapshot_at,
    previous_snapshot_at,
    DATEDIFF(snapshot_at, previous_snapshot_at) AS days_between_snapshots,
    price,
    previous_price,
    price - previous_price AS price_change,
    CASE
        WHEN previous_price IS NULL OR previous_price = 0 THEN NULL
        ELSE ((price - previous_price) / previous_price) * 100
    END AS price_change_pct
FROM price_history_with_previous
WHERE previous_snapshot_at IS NOT NULL;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';
