CREATE TABLE card_comercial_actions AS

SELECT c.name, c.archetype,
r.rarity_name,
'cardmarket_price' AS 'Marketplace',
cardmarket_price AS 'Price',
'EUR' AS 'Currency'

FROM cards c 
INNER JOIN card_prices 
ON c.card_id = card_prices.card_id
INNER JOIN rarities r 
ON r.id = c.card_id

UNION ALL 

SELECT c.name, c.archetype,
r.rarity_name,
'tcgplayer_price' AS 'Marketplace',
tcgplayer_price AS 'Price',
'USD' AS 'Currency'
FROM cards c 
INNER JOIN card_prices 
ON c.card_id = card_prices.card_id
INNER JOIN rarities r 
ON r.id = c.card_id

UNION ALL 

SELECT c.name, c.archetype,
r.rarity_name,
'ebay_price' AS 'Marketplace',
ebay_price AS 'Price',
'USD' AS 'Currency'
FROM cards c 
INNER JOIN card_prices 
ON c.card_id = card_prices.card_id
INNER JOIN rarities r 
ON r.id = c.card_id

UNION ALL 

SELECT c.name, c.archetype,
r.rarity_name,
'amazon_price' AS 'Marketplace',
amazon_price AS 'Price',
'USD' AS 'Currency'
FROM cards c 
INNER JOIN card_prices 
ON c.card_id = card_prices.card_id
INNER JOIN rarities r 
ON r.id = c.card_id;






