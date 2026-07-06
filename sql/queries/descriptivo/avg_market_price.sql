SELECT 
    cp.card_id,
    cp.cardmarket_price AS cardmarket_EUR,
    cp.tcgplayer_price AS tcgplayer_USD,
    cp.ebay_price AS ebay_USD,
    cp.amazon_price AS amazon_USD,
    cp.coolstuffinc_price AS coolstuffinc_USD,

    (
        COALESCE(cp.tcgplayer_price, 0) +
        COALESCE(cp.ebay_price, 0) +
        COALESCE(cp.amazon_price, 0) +
        COALESCE(cp.coolstuffinc_price, 0)
    )
    /
    NULLIF(
        (cp.tcgplayer_price IS NOT NULL) +
        (cp.ebay_price IS NOT NULL) +
        (cp.amazon_price IS NOT NULL) +
        (cp.coolstuffinc_price IS NOT NULL),
        0
    ) AS avg_price_usd,
    
    cs.id AS card_set_id,
    cs.set_price,
    cs.set_name AS set_name,

    c.name AS card_name

FROM card_sets cs 
INNER JOIN cards c 
    ON c.card_id = cs.card_id
INNER JOIN card_prices cp
    ON cp.card_id = c.card_id;