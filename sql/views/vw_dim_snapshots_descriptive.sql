-- Dimension BI: fechas de snapshots de precios.
-- 1 fila = 1 snapshot_at disponible en el historico.

CREATE OR REPLACE VIEW vw_dim_snapshots_descriptive AS
SELECT
    cph.snapshot_at,
    DATE(cph.snapshot_at) AS snapshot_date,
    YEAR(cph.snapshot_at) AS snapshot_year,
    QUARTER(cph.snapshot_at) AS snapshot_quarter,
    MONTH(cph.snapshot_at) AS snapshot_month,
    MONTHNAME(cph.snapshot_at) AS snapshot_month_name,
    DAY(cph.snapshot_at) AS snapshot_day,
    HOUR(cph.snapshot_at) AS snapshot_hour,
    DAYOFWEEK(cph.snapshot_at) AS snapshot_day_of_week
FROM card_price_history cph
GROUP BY
    cph.snapshot_at;
