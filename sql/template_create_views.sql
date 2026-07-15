-- template_create_views.sql
-- Crea o reemplaza todas las vistas mantenidas en sql/views.
--
-- Uso:
--   SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/template_create_views.sql;
--
-- Nota:
--   Esta plantilla no modifica tablas.
--   cardmarket_price_eur se mantiene como EUR.
--   cardmarket_usd se expone para comparativas USD entre marketplaces.

SET NAMES utf8mb4;

USE `yugioh_db`;

-- ---------------------------------------------------------------------------
-- Dimensiones
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW vw_dim_cards_descriptive AS
SELECT
    c.card_id,
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

CREATE OR REPLACE VIEW vw_dim_marketplaces_descriptive AS
SELECT
    1 AS marketplace_id,
    'cardmarket' AS marketplace,
    'Cardmarket' AS marketplace_name,
    'EUR' AS default_currency,
    'Europe' AS market_region

UNION ALL

SELECT
    2 AS marketplace_id,
    'tcgplayer',
    'TCGplayer',
    'USD',
    'United States'

UNION ALL

SELECT
    3 AS marketplace_id,
    'ebay',
    'eBay',
    'USD',
    'Global'

UNION ALL

SELECT
    4 AS marketplace_id,
    'amazon',
    'Amazon',
    'USD',
    'Global'

UNION ALL

SELECT
    5 AS marketplace_id,
    'coolstuffinc',
    'CoolStuffInc',
    'USD',
    'United States';

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

CREATE OR REPLACE VIEW vw_dim_sets_descriptive AS
SELECT
    s.id AS set_id,
    s.set_name,
    s.created_at,
    s.updated_at
FROM sets s;

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

-- ---------------------------------------------------------------------------
-- Hechos
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW vw_fact_avg_market_price AS
WITH avg_market_price AS (
    SELECT
        cp.card_id,
        cp.cardmarket_price_eur AS cardmarket_eur,
        cp.cardmarket_usd AS cardmarket_usd,
        cp.tcgplayer_price AS tcgplayer,
        cp.ebay_price AS ebay,
        cp.amazon_price AS amazon,
        cp.coolstuffinc_price AS coolstuffinc,
        (
            COALESCE(cp.cardmarket_usd, 0) +
            COALESCE(cp.tcgplayer_price, 0) +
            COALESCE(cp.ebay_price, 0) +
            COALESCE(cp.amazon_price, 0) +
            COALESCE(cp.coolstuffinc_price, 0)
        )
        /
        NULLIF(
            (cp.cardmarket_usd IS NOT NULL) +
            (cp.tcgplayer_price IS NOT NULL) +
            (cp.ebay_price IS NOT NULL) +
            (cp.amazon_price IS NOT NULL) +
            (cp.coolstuffinc_price IS NOT NULL),
            0
        ) AS avg_price_USD
    FROM card_prices cp
)
SELECT
    amp.card_id,
    c.name AS card_name,
    amp.cardmarket_eur,
    amp.cardmarket_usd,
    amp.tcgplayer,
    amp.ebay,
    amp.amazon,
    amp.coolstuffinc,
    amp.avg_price_USD
FROM avg_market_price amp
JOIN cards c
    ON c.card_id = amp.card_id
ORDER BY avg_price_USD DESC;

CREATE OR REPLACE VIEW vw_fact_card_prices_descriptive AS
SELECT
    c.card_id,
    c.name AS card_name,
    'cardmarket' AS marketplace,
    'EUR' AS currency,
    cp.cardmarket_price_eur AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.cardmarket_price_eur IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'cardmarket' AS marketplace,
    'USD' AS currency,
    cp.cardmarket_usd AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.cardmarket_usd IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'tcgplayer' AS marketplace,
    'USD' AS currency,
    cp.tcgplayer_price AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.tcgplayer_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'ebay' AS marketplace,
    'USD' AS currency,
    cp.ebay_price AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.ebay_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'amazon' AS marketplace,
    'USD' AS currency,
    cp.amazon_price AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.amazon_price IS NOT NULL

UNION ALL

SELECT
    c.card_id,
    c.name AS card_name,
    'coolstuffinc' AS marketplace,
    'USD' AS currency,
    cp.coolstuffinc_price AS price
FROM card_prices cp
LEFT JOIN cards c
    ON cp.card_id = c.card_id
WHERE cp.coolstuffinc_price IS NOT NULL;

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

CREATE OR REPLACE VIEW vw_fact_card_price_variation_predictive AS
WITH price_history_long AS (
    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'cardmarket' AS marketplace,
        'EUR' AS currency,
        cph.cardmarket_price_eur AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.cardmarket_price_eur IS NOT NULL

    UNION ALL

    SELECT
        cph.card_id,
        c.name AS card_name,
        cph.snapshot_at,
        'cardmarket' AS marketplace,
        'USD' AS currency,
        cph.cardmarket_usd AS price
    FROM card_price_history cph
    LEFT JOIN cards c
        ON cph.card_id = c.card_id
    WHERE cph.cardmarket_usd IS NOT NULL

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
        ELSE ((price - previous_price) / previous_price)
    END AS price_change_pct
FROM price_history_with_previous
WHERE previous_snapshot_at IS NOT NULL;


CREATE OR REPLACE VIEW vw_fact_price_rarity_marketplace AS
SELECT
    p.card_id,
    a.rarity_id,
    p.marketplace,
    p.currency,
    AVG(p.price) AS avg_price,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price,
    COUNT(*) AS rows_count
FROM vw_fact_card_prices_descriptive p
INNER JOIN vw_fact_card_set_appearances a
    ON p.card_id = a.card_id
WHERE
    a.rarity_id IS NOT NULL
    AND p.price IS NOT NULL
    AND p.price > 0
GROUP BY
    p.card_id,
    a.rarity_id,
    p.marketplace,
    p.currency;



-- ---------------------------------------------------------------------------
-- Herramientas
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW `yugioh_db`.`vw_card_tooltip_images_sets` AS
SELECT 
    `c`.`card_id` AS `card_id`,
    `c`.`name` AS `card_name`,
    `c`.`card_type` AS `card_type`,
    `c`.`archetype` AS `card_archetype`,
    `ci`.`image_id` AS `image_id`,
    `ci`.`image_url` AS `image_url`,
    `ci`.`image_url_small` AS `image_url_small`,
    `ci`.`image_url_cropped` AS `image_url_cropped`,
    `cs`.`set_id` AS `set_id`,
    `cs`.`set_name` AS `set_name`
FROM `yugioh_db`.`cards` `c`
LEFT JOIN `yugioh_db`.`card_images` `ci`
    ON `ci`.`card_id` = `c`.`card_id`
LEFT JOIN `yugioh_db`.`card_sets` `cs`
    ON `cs`.`card_id` = `c`.`card_id`;
