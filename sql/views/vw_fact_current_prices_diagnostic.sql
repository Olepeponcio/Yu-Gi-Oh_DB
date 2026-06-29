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
