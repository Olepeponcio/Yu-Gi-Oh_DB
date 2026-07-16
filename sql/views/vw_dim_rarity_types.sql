CREATE OR REPLACE VIEW vw_dim_rarity_types AS
SELECT 
r.rarity_id,
r.rarity_name,
r.rarity_code
FROM rarity_types r;