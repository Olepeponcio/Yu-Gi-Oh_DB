-- Evolucion del modelo para analisis de mercado.
-- Uso: ejecutar una vez sobre una base ya creada con sql/schema.sql.

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS sets (
    id INT NOT NULL AUTO_INCREMENT,
    set_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_sets_set_name (set_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS rarities (
    id INT NOT NULL AUTO_INCREMENT,
    rarity_name VARCHAR(100) NOT NULL,
    rarity_code VARCHAR(50) NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_rarities_name_code (rarity_name, rarity_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_price_history (
    id BIGINT NOT NULL AUTO_INCREMENT,
    card_id INT NOT NULL,
    snapshot_at DATETIME NOT NULL,
    cardmarket_price DECIMAL(10,2) NULL,
    tcgplayer_price DECIMAL(10,2) NULL,
    ebay_price DECIMAL(10,2) NULL,
    amazon_price DECIMAL(10,2) NULL,
    coolstuffinc_price DECIMAL(10,2) NULL,
    PRIMARY KEY (id),
    INDEX idx_card_price_history_card_id (card_id),
    INDEX idx_card_price_history_snapshot_at (snapshot_at),
    UNIQUE KEY uq_card_price_history_snapshot (card_id, snapshot_at),
    CONSTRAINT fk_card_price_history_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO sets (set_name)
SELECT DISTINCT set_name
FROM card_sets
WHERE set_name IS NOT NULL;

INSERT IGNORE INTO rarities (rarity_name, rarity_code)
SELECT DISTINCT set_rarity, COALESCE(set_rarity_code, '')
FROM card_sets
WHERE set_rarity IS NOT NULL;

ALTER TABLE card_sets
    ADD COLUMN set_id INT NULL AFTER card_id,
    ADD COLUMN rarity_id INT NULL AFTER set_id,
    ADD INDEX idx_card_sets_set_id (set_id),
    ADD INDEX idx_card_sets_rarity_id (rarity_id);

UPDATE card_sets cs
LEFT JOIN sets s
    ON s.set_name = cs.set_name
LEFT JOIN rarities r
    ON r.rarity_name = cs.set_rarity
    AND r.rarity_code = COALESCE(cs.set_rarity_code, '')
SET
    cs.set_id = s.id,
    cs.rarity_id = r.id;

ALTER TABLE card_sets
    ADD CONSTRAINT fk_card_sets_set
        FOREIGN KEY (set_id) REFERENCES sets (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    ADD CONSTRAINT fk_card_sets_rarity
        FOREIGN KEY (rarity_id) REFERENCES rarities (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
