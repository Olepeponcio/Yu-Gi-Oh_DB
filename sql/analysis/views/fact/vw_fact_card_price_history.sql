CREATE OR REPLACE VIEW vw_fact_price_history AS
SELECT
    h.card_id,
    h.snapshot_at,
    DATE(h.snapshot_at) AS snapshot_date,
    'cardmarket' AS marketplace,
    h.cardmarket_price AS price,
    'EUR' AS currency
FROM card_price_history h
WHERE h.cardmarket_price IS NOT NULL
  AND h.cardmarket_price > 0

UNION ALL

SELECT
    h.card_id,
    h.snapshot_at,
    DATE(h.snapshot_at) AS snapshot_date,
    'tcgplayer' AS marketplace,
    h.tcgplayer_price AS price,
    'USD' AS currency
FROM card_price_history h
WHERE h.tcgplayer_price IS NOT NULL
  AND h.tcgplayer_price > 0

UNION ALL

SELECT
    h.card_id,
    h.snapshot_at,
    DATE(h.snapshot_at) AS snapshot_date,
    'ebay' AS marketplace,
    h.ebay_price AS price,
    'USD' AS currency
FROM card_price_history h
WHERE h.ebay_price IS NOT NULL
  AND h.ebay_price > 0
  
UNION ALL

SELECT h.card_id,
h.snapshot_at,
DATE(h.snapshot_at) AS snapshot_date,
'amazon' AS marketplace,
h.amazon_price AS price,
'USD' AS currency
FROM card_price_history h
WHERE h.amazon_price IS NOT NULL
AND h.amazon_price > 0

UNION ALL 

SELECT h.card_id,
h.snapshot_at,
DATE(h.snapshot_at) AS snapshot_date,
'coolstuffinc' AS marketplace,
h.coolstuffinc_price AS price,
'USD' AS currency
FROM card_price_history h
WHERE h.coolstuffinc_price IS NOT NULL
AND h.coolstuffinc_price > 0;
