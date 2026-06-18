CREATE OR REPLACE VIEW vw_ref_banlist_status AS
SELECT
    format,
    ban_status,
    ban_status AS normalized_status,
    CASE ban_status
        WHEN 'Forbidden' THEN 1
        WHEN 'Banned' THEN 1
        WHEN 'Limited' THEN 2
        WHEN 'Semi-Limited' THEN 3
        WHEN 'Unlimited' THEN 4
        ELSE 99
    END AS sort_order,
    CASE
        WHEN ban_status IN ('Forbidden', 'Banned') THEN 0
        ELSE 1
    END AS is_playable
FROM (
    SELECT DISTINCT 'TCG' AS format, ban_tcg AS ban_status
    FROM card_banlist
    WHERE ban_tcg IS NOT NULL

    UNION

    SELECT DISTINCT 'OCG' AS format, ban_ocg AS ban_status
    FROM card_banlist
    WHERE ban_ocg IS NOT NULL

    UNION

    SELECT DISTINCT 'GOAT' AS format, ban_goat AS ban_status
    FROM card_banlist
    WHERE ban_goat IS NOT NULL
) x;