-- Calidad de grano: duplicados en apariciones carta + set + rareza.
-- Resultado esperado: sin filas.

CREATE OR REPLACE VIEW vw_quality_duplicate_grain_diagnostic AS
SELECT
    card_id,
    set_name,
    set_code,
    set_rarity,
    set_rarity_code,
    COUNT(*) AS duplicate_count
FROM card_sets
GROUP BY
    card_id,
    set_name,
    set_code,
    set_rarity,
    set_rarity_code
HAVING COUNT(*) > 1;
