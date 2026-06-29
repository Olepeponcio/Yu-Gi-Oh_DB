-- Predictivo: comprobar si existe historico suficiente para analizar variacion.
-- 1 fila = 1 snapshot de precios.
-- La view se actualiza logicamente al consultar; los snapshots los inserta el ETL en card_price_history.

CREATE OR REPLACE VIEW vw_fact_price_snapshot_summary_predictive AS
SELECT
    snapshot_at,
    COUNT(*) AS total_price_rows,
    COUNT(DISTINCT card_id) AS total_cards,
    SUM(CASE WHEN cardmarket_price IS NOT NULL THEN 1 ELSE 0 END) AS cardmarket_price_rows,
    SUM(CASE WHEN tcgplayer_price IS NOT NULL THEN 1 ELSE 0 END) AS tcgplayer_price_rows,
    SUM(CASE WHEN ebay_price IS NOT NULL THEN 1 ELSE 0 END) AS ebay_price_rows,
    SUM(CASE WHEN amazon_price IS NOT NULL THEN 1 ELSE 0 END) AS amazon_price_rows,
    SUM(CASE WHEN coolstuffinc_price IS NOT NULL THEN 1 ELSE 0 END) AS coolstuffinc_price_rows,
    MIN(cardmarket_price) AS min_cardmarket_price_eur,
    MAX(cardmarket_price) AS max_cardmarket_price_eur,
    AVG(cardmarket_price) AS avg_cardmarket_price_eur,
    MIN(tcgplayer_price) AS min_tcgplayer_price_usd,
    MAX(tcgplayer_price) AS max_tcgplayer_price_usd,
    AVG(tcgplayer_price) AS avg_tcgplayer_price_usd,
    MIN(ebay_price) AS min_ebay_price_usd,
    MAX(ebay_price) AS max_ebay_price_usd,
    AVG(ebay_price) AS avg_ebay_price_usd,
    MIN(amazon_price) AS min_amazon_price_usd,
    MAX(amazon_price) AS max_amazon_price_usd,
    AVG(amazon_price) AS avg_amazon_price_usd,
    MIN(coolstuffinc_price) AS min_coolstuffinc_price_usd,
    MAX(coolstuffinc_price) AS max_coolstuffinc_price_usd,
    AVG(coolstuffinc_price) AS avg_coolstuffinc_price_usd
FROM card_price_history
GROUP BY
    snapshot_at;
