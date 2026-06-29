-- Calidad FK: claves foraneas opcionales sin resolver.
-- No siempre es error; sirve como aviso previo a visualizacion.

CREATE OR REPLACE VIEW vw_quality_nullable_fk_diagnostic AS
SELECT
    'card_sets.set_id nullable' AS check_name,
    COUNT(*) AS affected_rows
FROM card_sets
WHERE set_id IS NULL

UNION ALL

SELECT
    'card_sets.rarity_id nullable',
    COUNT(*)
FROM card_sets
WHERE rarity_id IS NULL;
