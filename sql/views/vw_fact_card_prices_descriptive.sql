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
