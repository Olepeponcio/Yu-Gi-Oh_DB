CREATE OR REPLACE VIEW vw_bridge_card_banlist AS
SELECT
    card_id,
    'TCG' AS format,
    ban_tcg AS ban_status,
    CONCAT('TCG', '|', ban_tcg) AS banlist_status_key
FROM card_banlist
WHERE ban_tcg IS NOT NULL

UNION ALL

SELECT
    card_id,
    'OCG' AS format,
    ban_ocg AS ban_status,
    CONCAT('OCG', '|', ban_ocg) AS banlist_status_key
FROM card_banlist
WHERE ban_ocg IS NOT NULL

UNION ALL

SELECT
    card_id,
    'GOAT' AS format,
    ban_goat AS ban_status,
    CONCAT('GOAT', '|', ban_goat) AS banlist_status_key
FROM card_banlist
WHERE ban_goat IS NOT NULL;
