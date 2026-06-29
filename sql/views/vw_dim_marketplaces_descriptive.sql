-- Dimension BI: fuentes de precio.
-- 1 fila = 1 marketplace.

CREATE OR REPLACE VIEW vw_dim_marketplaces_descriptive AS
SELECT
    'cardmarket' AS marketplace,
    'Cardmarket' AS marketplace_name,
    'EUR' AS default_currency,
    'Europe' AS market_region

UNION ALL

SELECT
    'tcgplayer',
    'TCGplayer',
    'USD',
    'United States'

UNION ALL

SELECT
    'ebay',
    'eBay',
    'USD',
    'Global'

UNION ALL

SELECT
    'amazon',
    'Amazon',
    'USD',
    'Global'

UNION ALL

SELECT
    'coolstuffinc',
    'CoolStuffInc',
    'USD',
    'United States';
