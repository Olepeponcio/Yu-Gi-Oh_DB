SELECT marketplace, COUNT(*) AS total_rows, price
FROM vw_fact_card_prices
GROUP BY marketplace, price
ORDER BY price DESC
LIMIT 150;
