-- Dimension BI: nombres de rareza usados en analisis agregado.
-- 1 fila = 1 rarity_name.

CREATE OR REPLACE VIEW vw_dim_rarity_names_descriptive AS
SELECT
    rarity_name,
    COUNT(*) AS rarity_catalog_rows,
    COUNT(DISTINCT set_code) AS total_set_codes,
    COUNT(DISTINCT rarity_code) AS total_rarity_codes
FROM rarities
GROUP BY
    rarity_name;
