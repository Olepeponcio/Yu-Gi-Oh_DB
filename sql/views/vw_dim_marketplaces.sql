CREATE OR REPLACE VIEW vw_fact_card_prices_current AS
SELECT
    ranked.price_history_id,
    ranked.card_id,
    ranked.marketplace_id,
    ranked.snapshot_at,
    ranked.price AS card_price_usd
FROM (
    SELECT
        ph.price_history_id,
        ph.card_id,
        ph.marketplace_id,
        ph.snapshot_at,
        ph.price,
        ROW_NUMBER() OVER (
            PARTITION BY
                ph.card_id,
                ph.marketplace_id
            ORDER BY
                ph.snapshot_at DESC,
                ph.price_history_id DESC
        ) AS row_num
    FROM card_price_history AS ph
    INNER JOIN cards AS c
        ON c.card_id = ph.card_id
    WHERE ph.currency_code = 'USD'
) AS ranked
WHERE ranked.row_num = 1;