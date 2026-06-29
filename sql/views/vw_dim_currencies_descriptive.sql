-- Dimension BI: monedas declaradas en las vistas de precios.
-- 1 fila = 1 moneda.

CREATE OR REPLACE VIEW vw_dim_currencies_descriptive AS
SELECT
    'EUR' AS currency,
    'Euro' AS currency_name,
    'EUR' AS currency_symbol_text

UNION ALL

SELECT
    'USD',
    'US Dollar',
    'USD';
