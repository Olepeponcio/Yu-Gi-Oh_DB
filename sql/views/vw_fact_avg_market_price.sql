CREATE OR REPLACE VIEW vw_fact_avg_market_price AS

WITH avg_market_price AS (
SELECT 
    cp.card_id,
    cp.cardmarket_price_eur AS cardmarket_eur,
    cp.cardmarket_usd AS cardmarket_usd,
    cp.tcgplayer_price AS tcgplayer,
    cp.ebay_price AS ebay,
    cp.amazon_price AS amazon,
    cp.coolstuffinc_price AS coolstuffinc,
 (
        COALESCE(cp.cardmarket_usd, 0) +
        COALESCE(cp.tcgplayer_price, 0) +
        COALESCE(cp.ebay_price, 0) +
        COALESCE(cp.amazon_price, 0) +
        COALESCE(cp.coolstuffinc_price, 0)
    )
    /
    NULLIF(
        (cp.cardmarket_usd IS NOT NULL) +
        (cp.tcgplayer_price IS NOT NULL) +
        (cp.ebay_price IS NOT NULL) +
        (cp.amazon_price IS NOT NULL) +
        (cp.coolstuffinc_price IS NOT NULL),
        0
    ) AS avg_price_USD
    FROM card_prices cp
    )
    
    SELECT 
    amp.card_id,
    c.name AS card_name,
    amp.cardmarket_eur,
    amp.cardmarket_usd,
    amp.tcgplayer,
    amp.ebay,
    amp.amazon,
    amp.coolstuffinc,
    amp.avg_price_USD
    
    FROM avg_market_price amp
    
    JOIN cards c
    ON c.card_id = amp.card_id
    
    ORDER BY avg_price_USD DESC;
    
