CREATE OR REPLACE VIEW vw_dim_card_image AS
SELECT
    ci.card_id,
    MIN(ci.image_id) AS image_id,
    MIN(ci.image_url) AS image_url,
    MIN(ci.image_url_small) AS image_url_small,
    MIN(ci.image_url_cropped) AS image_url_cropped
FROM card_images ci
GROUP BY ci.card_id;