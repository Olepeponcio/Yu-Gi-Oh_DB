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
