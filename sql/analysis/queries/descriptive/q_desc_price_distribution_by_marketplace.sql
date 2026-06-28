-- Grano: 1 fila = marketplace + precio actual observado.
-- Fuente: card_prices.

SELECT
    marketplace,
    price,
    COUNT(*) AS total_rows
FROM (
    SELECT 'cardmarket' AS marketplace, cardmarket_price AS price
    FROM card_prices
    WHERE cardmarket_price IS NOT NULL
      AND cardmarket_price > 0

    UNION ALL

    SELECT 'tcgplayer' AS marketplace, tcgplayer_price AS price
    FROM card_prices
    WHERE tcgplayer_price IS NOT NULL
      AND tcgplayer_price > 0

    UNION ALL

    SELECT 'ebay' AS marketplace, ebay_price AS price
    FROM card_prices
    WHERE ebay_price IS NOT NULL
      AND ebay_price > 0

    UNION ALL

    SELECT 'amazon' AS marketplace, amazon_price AS price
    FROM card_prices
    WHERE amazon_price IS NOT NULL
      AND amazon_price > 0

    UNION ALL

    SELECT 'coolstuffinc' AS marketplace, coolstuffinc_price AS price
    FROM card_prices
    WHERE coolstuffinc_price IS NOT NULL
      AND coolstuffinc_price > 0
) prices
GROUP BY marketplace, price
ORDER BY price DESC
LIMIT 150;
