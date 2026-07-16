CREATE OR REPLACE VIEW vw_dim_sets AS
SELECT 
s.set_id,
s.set_name
FROM sets s
ORDER BY s.set_id ASC, s.set_name ASC;
