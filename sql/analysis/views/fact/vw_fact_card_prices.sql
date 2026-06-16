CREATE OR REPLACE VIEW vw_fact_card_prices AS
SELECT
    c.card_id,
    c.name,
    'tcgplayer' AS marketplace,
    cp.tcgplayer_price AS price,
    'USD' AS currency
FROM card_prices cp
JOIN cards c ON c.card_id = cp.card_id
WHERE cp.tcgplayer_price > 0

UNION ALL

SELECT
    c.card_id,
    c.name,
    'ebay' AS marketplace,
    cp.ebay_price AS price,
    'USD' AS currency
FROM card_prices cp
JOIN cards c ON c.card_id = cp.card_id
WHERE cp.ebay_price > 0

UNION ALL

SELECT
    c.card_id,
    c.name,
    'amazon' AS marketplace,
    cp.amazon_price AS price,
    'USD' AS currency
FROM card_prices cp
JOIN cards c ON c.card_id = cp.card_id
WHERE cp.amazon_price > 0

UNION ALL

SELECT
    c.card_id,
    c.name,
    'coolstuffinc' AS marketplace,
    cp.coolstuffinc_price AS price,
    'USD' AS currency
FROM card_prices cp
JOIN cards c ON c.card_id = cp.card_id
WHERE cp.coolstuffinc_price > 0;
