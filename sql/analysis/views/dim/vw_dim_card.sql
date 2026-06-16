CREATE view vw_dim_card AS
SELECT c.card_id, 
c.name,
c.card_type,
c.frame_type,
c.attribute
FROM cards c
