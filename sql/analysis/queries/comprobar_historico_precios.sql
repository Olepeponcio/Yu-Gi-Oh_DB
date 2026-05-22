SELECT
    COUNT(DISTINCT snapshot_at) AS total_snapshots,
    MIN(snapshot_at) AS first_snapshot,
    MAX(snapshot_at) AS last_snapshot
FROM card_price_history;