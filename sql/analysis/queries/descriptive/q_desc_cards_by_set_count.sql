SELECT 
    c.name,
    COUNT(DISTINCT cs.set_name) AS total_sets
FROM cards c
JOIN card_sets cs
ON c.card_id = cs.card_id
GROUP BY c.card_id, c.name
ORDER BY total_sets DESC;
