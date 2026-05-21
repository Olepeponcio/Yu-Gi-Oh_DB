-- 2. Cartas potencialmente staples competitivas
-- Proxy: cartas legales en TCG, con precio relevante y muchas reimpresiones/set appearances

CREATE OR REPLACE VIEW vw_competitive_staple_candidates AS
SELECT
    c.card_id,
    c.name,
    c.card_type,
    c.human_readable_card_type,
    c.archetype,
    b.ban_tcg,
    COUNT(cs.id) AS total_printings,
    COUNT(DISTINCT cs.set_code) AS total_set_codes,
    ROUND(AVG(cs.set_price), 2) AS avg_set_price,
    ROUND(MAX(cs.set_price), 2) AS max_set_price
FROM cards c
LEFT JOIN card_sets cs
    ON c.card_id = cs.card_id
LEFT JOIN card_banlist b
    ON c.card_id = b.card_id
WHERE cs.set_price IS NOT NULL
  AND (
        b.ban_tcg IS NULL
        OR b.ban_tcg NOT IN ('Banned', 'Forbidden')
      )
GROUP BY
    c.card_id,
    c.name,
    c.card_type,
    c.human_readable_card_type,
    c.archetype,
    b.ban_tcg
HAVING
    total_printings >= 3
    AND avg_set_price >= 1
ORDER BY
    total_printings DESC,
    avg_set_price DESC;
