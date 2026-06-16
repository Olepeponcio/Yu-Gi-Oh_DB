CREATE OR REPLACE VIEW vw_dim_rarity AS
SELECT
    r.id AS rarity_id,
    r.set_code,
    r.rarity_name,
    r.rarity_code
FROM rarities r;