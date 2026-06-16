-- ¿Que cartas tienen mayor precio medio combinando marketplaces disponibles?
SELECT 
    c.card_id,
    c.name,
    cp.tcgplayer_price,
    cp.ebay_price,
    cp.amazon_price,
    cp.coolstuffinc_price,
    ROUND(
        (
            IFNULL(cp.tcgplayer_price, 0) +
            IFNULL(cp.ebay_price, 0) +
            IFNULL(cp.amazon_price, 0) +
            IFNULL(cp.coolstuffinc_price, 0)
        ) / NULLIF(
            (cp.tcgplayer_price IS NOT NULL) +
            (cp.ebay_price IS NOT NULL) +
            (cp.amazon_price IS NOT NULL) +
            (cp.coolstuffinc_price IS NOT NULL),
            0
        ),
        2
    ) AS avg_usd_marketplace_price
FROM card_prices cp
JOIN cards c
    ON c.card_id = cp.card_id
ORDER BY avg_usd_marketplace_price DESC;