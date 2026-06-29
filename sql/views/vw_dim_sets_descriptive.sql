-- Dimension BI: catalogo de sets.
-- 1 fila = 1 set.

CREATE OR REPLACE VIEW vw_dim_sets_descriptive AS
SELECT
    s.id AS set_id,
    s.set_name,
    s.created_at,
    s.updated_at
FROM sets s;
