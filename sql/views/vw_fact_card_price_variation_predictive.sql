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
