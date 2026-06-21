CREATE OR REPLACE VIEW vw_dim_card_typelines AS
SELECT ct.card_id, 
ct.typeline, 
ct.position
FROM card_typelines ct;