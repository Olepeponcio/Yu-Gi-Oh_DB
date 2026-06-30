-- create_or_replace_views_workbench.sql
-- Crea o reemplaza las views del modelo relacional simplificado para Power BI.
--
-- Uso:
--   Abrir este archivo en MySQL Workbench y ejecutar.
--   Este archivo no usa SOURCE; contiene las definiciones completas.

SET NAMES utf8mb4;

USE `yugioh_db`;

-- sql/views/vw_dim_cards_descriptive.sql

CREATE OR REPLACE VIEW vw_dim_cards_descriptive AS
SELECT c.card_id,
c.name,
c.card_type,
c.human_readable_card_type,
c.frame_type,
c.race,
COALESCE(c.archetype, 'Sin arquetipo') AS archetype,
CAST(c.atk AS SIGNED) AS atk,
CAST(c.def AS SIGNED) AS def,
COALESCE(c.attribute, 'No aplica') AS attribute,
CAST(c.level AS SIGNED) AS level,
CAST(c.scale AS SIGNED) AS scale,
CAST(c.link_value AS SIGNED) AS link_value

FROM cards c;

-- sql/views/vw_dim_sets_descriptive.sql

CREATE OR REPLACE VIEW vw_dim_sets_descriptive AS
SELECT
    s.id AS set_id,
    s.set_name,
    s.created_at,
    s.updated_at
FROM sets s;

-- sql/views/vw_dim_rarities_descriptive.sql

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

-- sql/views/vw_dim_marketplaces_descriptive.sql

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

-- sql/views/vw_dim_currencies_descriptive.sql

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

-- sql/views/vw_dim_snapshots_descriptive.sql

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

-- sql/views/vw_fact_card_prices_descriptive.sql

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

-- sql/views/vw_fact_card_set_appearances.sql

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

-- sql/views/vw_fact_card_price_variation_predictive.sql

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
