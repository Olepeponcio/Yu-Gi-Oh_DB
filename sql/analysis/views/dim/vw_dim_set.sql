CREATE OR REPLACE VIEW vw_dim_set AS
SELECT
    s.id AS set_id,
    s.set_name
FROM sets s;

