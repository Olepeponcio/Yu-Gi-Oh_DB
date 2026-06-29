-- Dimension BI: catalogo de rarezas.
-- 1 fila = 1 rareza por codigo de impresion.

CREATE OR REPLACE VIEW vw_dim_rarities_descriptive AS
SELECT
    r.id AS rarity_id,
    r.set_code,
    r.rarity_name,
    r.rarity_code,
    CONCAT(r.set_code, '|', r.rarity_name, '|', r.rarity_code) AS rarity_business_key,
    r.created_at,
    r.updated_at
FROM rarities r;
