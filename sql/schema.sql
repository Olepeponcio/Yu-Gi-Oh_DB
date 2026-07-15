-- Punto de partida relacional de yugioh_db.
-- Solo crea tablas madre: las views se disenaran en una fase posterior.

SET NAMES utf8mb4;
USE `yugioh_db`;

CREATE TABLE IF NOT EXISTS cards (
    card_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    card_type VARCHAR(100) NOT NULL,
    human_readable_card_type VARCHAR(150) NULL,
    frame_type VARCHAR(50) NULL,
    description TEXT NULL,
    race VARCHAR(100) NULL,
    archetype VARCHAR(150) NULL,
    ygoprodeck_url VARCHAR(500) NULL,
    atk INT NULL,
    def INT NULL,
    attribute VARCHAR(30) NULL,
    level INT NULL,
    scale INT NULL,
    pendulum_description TEXT NULL,
    monster_description TEXT NULL,
    link_value INT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (card_id),
    INDEX idx_cards_name (name),
    INDEX idx_cards_card_type (card_type),
    INDEX idx_cards_archetype (archetype)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS sets (
    set_id INT NOT NULL AUTO_INCREMENT,
    set_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (set_id),
    UNIQUE KEY uq_sets_name (set_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS rarity_types (
    rarity_id INT NOT NULL AUTO_INCREMENT,
    rarity_name VARCHAR(100) NOT NULL,
    rarity_code VARCHAR(50) NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (rarity_id),
    UNIQUE KEY uq_rarity_types_name_code (rarity_name, rarity_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_printings (
    printing_id BIGINT NOT NULL AUTO_INCREMENT,
    card_id INT NOT NULL,
    set_id INT NOT NULL,
    rarity_id INT NULL,
    set_code VARCHAR(100) NOT NULL,
    raw_rarity_name VARCHAR(100) NOT NULL,
    raw_rarity_code VARCHAR(50) NOT NULL DEFAULT '',
    rarity_source_quality VARCHAR(40) NOT NULL,
    set_price_usd DECIMAL(12,2) NULL,
    PRIMARY KEY (printing_id),
    UNIQUE KEY uq_card_printings_grain (card_id, set_code, raw_rarity_name, raw_rarity_code),
    INDEX idx_card_printings_set (set_id),
    INDEX idx_card_printings_rarity (rarity_id),
    INDEX idx_card_printings_quality (rarity_source_quality),
    CONSTRAINT fk_card_printings_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_card_printings_set FOREIGN KEY (set_id) REFERENCES sets (set_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_card_printings_rarity FOREIGN KEY (rarity_id) REFERENCES rarity_types (rarity_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_card_printings_price CHECK (set_price_usd IS NULL OR set_price_usd >= 0),
    CONSTRAINT chk_card_printings_quality CHECK (
        rarity_source_quality IN ('valid', 'normalized_typo', 'invalid_numeric_source', 'internal_api_label', 'missing')
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS marketplaces (
    marketplace_id SMALLINT NOT NULL,
    marketplace_code VARCHAR(40) NOT NULL,
    marketplace_name VARCHAR(80) NOT NULL,
    market_region VARCHAR(80) NULL,
    PRIMARY KEY (marketplace_id),
    UNIQUE KEY uq_marketplaces_code (marketplace_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS currencies (
    currency_code CHAR(3) NOT NULL,
    currency_name VARCHAR(80) NOT NULL,
    PRIMARY KEY (currency_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO marketplaces (marketplace_id, marketplace_code, marketplace_name, market_region) VALUES
    (1, 'cardmarket', 'Cardmarket', 'Europe'),
    (2, 'tcgplayer', 'TCGplayer', 'United States'),
    (3, 'ebay', 'eBay', 'Global'),
    (4, 'amazon', 'Amazon', 'Global'),
    (5, 'coolstuffinc', 'CoolStuffInc', 'United States')
ON DUPLICATE KEY UPDATE marketplace_name = VALUES(marketplace_name), market_region = VALUES(market_region);

INSERT INTO currencies (currency_code, currency_name) VALUES
    ('EUR', 'Euro'), ('USD', 'US Dollar')
ON DUPLICATE KEY UPDATE currency_name = VALUES(currency_name);

-- Hecho largo y append-only. El ultimo snapshot representa el precio vigente;
-- todos los anteriores forman el historico y se preservan en cada reset.
CREATE TABLE IF NOT EXISTS card_price_history (
    price_history_id BIGINT NOT NULL AUTO_INCREMENT,
    card_id INT NOT NULL,
    marketplace_id SMALLINT NOT NULL,
    currency_code CHAR(3) NOT NULL,
    snapshot_at DATETIME NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    price_origin VARCHAR(30) NOT NULL DEFAULT 'api',
    exchange_rate DECIMAL(18,8) NULL,
    PRIMARY KEY (price_history_id),
    UNIQUE KEY uq_price_history_grain (card_id, marketplace_id, currency_code, snapshot_at),
    INDEX idx_price_history_snapshot (snapshot_at),
    INDEX idx_price_history_market_currency (marketplace_id, currency_code),
    CONSTRAINT fk_price_history_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_price_history_marketplace FOREIGN KEY (marketplace_id) REFERENCES marketplaces (marketplace_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_price_history_currency FOREIGN KEY (currency_code) REFERENCES currencies (currency_code)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_price_history_price CHECK (price >= 0),
    CONSTRAINT chk_price_history_origin CHECK (price_origin IN ('api', 'currency_conversion'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_images (
    image_id INT NOT NULL,
    card_id INT NOT NULL,
    image_url VARCHAR(500) NULL,
    image_url_small VARCHAR(500) NULL,
    image_url_cropped VARCHAR(500) NULL,
    PRIMARY KEY (image_id),
    INDEX idx_card_images_card (card_id),
    CONSTRAINT fk_card_images_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_banlist (
    card_id INT NOT NULL,
    ban_tcg VARCHAR(50) NULL,
    ban_ocg VARCHAR(50) NULL,
    ban_goat VARCHAR(50) NULL,
    PRIMARY KEY (card_id),
    CONSTRAINT fk_card_banlist_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_typelines (
    card_id INT NOT NULL,
    typeline VARCHAR(100) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, typeline),
    CONSTRAINT fk_card_typelines_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_linkmarkers (
    card_id INT NOT NULL,
    linkmarker VARCHAR(50) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, linkmarker),
    CONSTRAINT fk_card_linkmarkers_card FOREIGN KEY (card_id) REFERENCES cards (card_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SHOW TABLES;
