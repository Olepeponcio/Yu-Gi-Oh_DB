-- Dimension BI: fuentes de precio.
-- 1 fila = 1 marketplace.

CREATE OR REPLACE VIEW vw_dim_marketplaces_descriptive AS
SELECT
	1 AS marketplace_id,
    'cardmarket' AS marketplace,
    'Cardmarket' AS marketplace_name,
    'EUR' AS default_currency,
    'Europe' AS market_region

UNION ALL

SELECT
	2 AS marketplace_id,
    'tcgplayer',
    'TCGplayer',
    'USD',
    'United States'

UNION ALL

SELECT
	3 AS marketplace_id,
    'ebay',
    'eBay',
    'USD',
    'Global'

UNION ALL

SELECT
	4 AS marketplace_id,
    'amazon',
    'Amazon',
    'USD',
    'Global'

UNION ALL

SELECT
	5 AS marketplace_id,
    'coolstuffinc',
    'CoolStuffInc',
    'USD',
    'United States';
