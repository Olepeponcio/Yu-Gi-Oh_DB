WITH usd_avg_history AS (
    SELECT
        h.card_id,
        c.name,
        h.snapshot_at,
        (
            COALESCE(h.tcgplayer_price, 0) +
            COALESCE(h.ebay_price, 0) +
            COALESCE(h.amazon_price, 0) +
            COALESCE(h.coolstuffinc_price, 0)
        ) / NULLIF(
            (h.tcgplayer_price IS NOT NULL) +
            (h.ebay_price IS NOT NULL) +
            (h.amazon_price IS NOT NULL) +
            (h.coolstuffinc_price IS NOT NULL),
            0
        ) AS avg_usd_price
    FROM card_price_history h
    JOIN cards c ON c.card_id = h.card_id
),
changes AS (
    SELECT
        card_id,
        name,
        snapshot_at,
        avg_usd_price,
        LAG(avg_usd_price) OVER (
            PARTITION BY card_id
            ORDER BY snapshot_at
        ) AS previous_avg_usd_price
    FROM usd_avg_history
    WHERE avg_usd_price IS NOT NULL
)
SELECT
    card_id,
    name,
    previous_avg_usd_price,
    avg_usd_price AS current_avg_usd_price,
    ROUND(avg_usd_price - previous_avg_usd_price, 2) AS price_change_usd,
    ROUND(
        ((avg_usd_price - previous_avg_usd_price) / previous_avg_usd_price) * 100,
        2
    ) AS growth_pct
FROM changes
WHERE previous_avg_usd_price IS NOT NULL
  AND previous_avg_usd_price > 0
  AND avg_usd_price > previous_avg_usd_price
ORDER BY growth_pct DESC
LIMIT 50;