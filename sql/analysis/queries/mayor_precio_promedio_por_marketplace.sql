SELECT marketplace, COUNT(*) AS total_rows, price
FROM vw_desc_card_price_by_marketplace
GROUP BY marketplace, price
ORDER BY price DESC
LIMIT 150;