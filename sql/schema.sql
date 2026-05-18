-- Esquema inicial candidato para datos de YGOPRODeck.
-- Objetivo: definir estructura SQL antes de programar el ETL.
-- Base esperada: yugioh_db.
-- Uso normal: crear tablas si no existen, sin borrar datos existentes.

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS cards (
    id INT NOT NULL,
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
    PRIMARY KEY (id),
    INDEX idx_cards_name (name),
    INDEX idx_cards_card_type (card_type),
    INDEX idx_cards_frame_type (frame_type),
    INDEX idx_cards_archetype (archetype),
    INDEX idx_cards_attribute (attribute)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_sets (
    id INT NOT NULL AUTO_INCREMENT,
    card_id INT NOT NULL,
    set_name VARCHAR(255) NOT NULL,
    set_code VARCHAR(100) NULL,
    set_rarity VARCHAR(100) NULL,
    set_rarity_code VARCHAR(50) NULL,
    set_price DECIMAL(10,2) NULL,
    PRIMARY KEY (id),
    INDEX idx_card_sets_card_id (card_id),
    INDEX idx_card_sets_set_name (set_name),
    INDEX idx_card_sets_set_code (set_code),
    CONSTRAINT fk_card_sets_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_images (
    image_id INT NOT NULL,
    card_id INT NOT NULL,
    image_url VARCHAR(500) NULL,
    image_url_small VARCHAR(500) NULL,
    image_url_cropped VARCHAR(500) NULL,
    PRIMARY KEY (image_id),
    INDEX idx_card_images_card_id (card_id),
    CONSTRAINT fk_card_images_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_prices (
    card_id INT NOT NULL,
    cardmarket_price DECIMAL(10,2) NULL,
    tcgplayer_price DECIMAL(10,2) NULL,
    ebay_price DECIMAL(10,2) NULL,
    amazon_price DECIMAL(10,2) NULL,
    coolstuffinc_price DECIMAL(10,2) NULL,
    PRIMARY KEY (card_id),
    CONSTRAINT fk_card_prices_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_banlist (
    card_id INT NOT NULL,
    ban_tcg VARCHAR(50) NULL,
    ban_ocg VARCHAR(50) NULL,
    ban_goat VARCHAR(50) NULL,
    PRIMARY KEY (card_id),
    CONSTRAINT fk_card_banlist_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_typelines (
    card_id INT NOT NULL,
    typeline VARCHAR(100) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, typeline),
    INDEX idx_card_typelines_typeline (typeline),
    CONSTRAINT fk_card_typelines_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS card_linkmarkers (
    card_id INT NOT NULL,
    linkmarker VARCHAR(50) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, linkmarker),
    INDEX idx_card_linkmarkers_linkmarker (linkmarker),
    CONSTRAINT fk_card_linkmarkers_card
        FOREIGN KEY (card_id) REFERENCES cards (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
