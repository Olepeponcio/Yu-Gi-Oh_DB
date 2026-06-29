-- schema.sql
-- Crea las tablas madre del proyecto dentro de yugioh_db.
--
-- Uso:
--   1. Crear manualmente el schema yugioh_db en MySQL.
--   2. Ejecutar:
--      SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
--
-- Este script no crea ni borra la base de datos. Solo crea tablas.

SET NAMES utf8mb4;

USE `yugioh_db`;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`cards` (
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
    INDEX idx_cards_frame_type (frame_type),
    INDEX idx_cards_archetype (archetype),
    INDEX idx_cards_attribute (attribute)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`sets` (
    id INT NOT NULL AUTO_INCREMENT,
    set_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_sets_set_name (set_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`rarities` (
    id INT NOT NULL AUTO_INCREMENT,
    set_code VARCHAR(100) NOT NULL,
    rarity_name VARCHAR(100) NOT NULL,
    rarity_code VARCHAR(50) NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_rarities_set_code (set_code),
    UNIQUE KEY uq_rarities_set_code_name_code (set_code, rarity_name, rarity_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_sets` (
    id INT NOT NULL AUTO_INCREMENT,
    card_id INT NOT NULL,
    set_id INT NULL,
    rarity_id INT NULL,
    set_name VARCHAR(255) NOT NULL,
    set_code VARCHAR(100) NULL,
    set_rarity VARCHAR(100) NULL,
    set_rarity_code VARCHAR(50) NULL,
    set_price DECIMAL(10,2) NULL,
    PRIMARY KEY (id),
    INDEX idx_card_sets_card_id (card_id),
    INDEX idx_card_sets_set_id (set_id),
    INDEX idx_card_sets_rarity_id (rarity_id),
    INDEX idx_card_sets_set_name (set_name),
    INDEX idx_card_sets_set_code (set_code),
    CONSTRAINT fk_card_sets_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_card_sets_set
        FOREIGN KEY (set_id) REFERENCES `yugioh_db`.`sets` (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_card_sets_rarity
        FOREIGN KEY (rarity_id) REFERENCES `yugioh_db`.`rarities` (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_images` (
    image_id INT NOT NULL,
    card_id INT NOT NULL,
    image_url VARCHAR(500) NULL,
    image_url_small VARCHAR(500) NULL,
    image_url_cropped VARCHAR(500) NULL,
    PRIMARY KEY (image_id),
    INDEX idx_card_images_card_id (card_id),
    CONSTRAINT fk_card_images_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_prices` (
    card_id INT NOT NULL,
    cardmarket_price DECIMAL(10,2) NULL,
    tcgplayer_price DECIMAL(10,2) NULL,
    ebay_price DECIMAL(10,2) NULL,
    amazon_price DECIMAL(10,2) NULL,
    coolstuffinc_price DECIMAL(10,2) NULL,
    PRIMARY KEY (card_id),
    CONSTRAINT fk_card_prices_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_price_history` (
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
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_banlist` (
    card_id INT NOT NULL,
    ban_tcg VARCHAR(50) NULL,
    ban_ocg VARCHAR(50) NULL,
    ban_goat VARCHAR(50) NULL,
    PRIMARY KEY (card_id),
    CONSTRAINT fk_card_banlist_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_typelines` (
    card_id INT NOT NULL,
    typeline VARCHAR(100) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, typeline),
    INDEX idx_card_typelines_typeline (typeline),
    CONSTRAINT fk_card_typelines_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `yugioh_db`.`card_linkmarkers` (
    card_id INT NOT NULL,
    linkmarker VARCHAR(50) NOT NULL,
    position INT NOT NULL,
    PRIMARY KEY (card_id, linkmarker),
    INDEX idx_card_linkmarkers_linkmarker (linkmarker),
    CONSTRAINT fk_card_linkmarkers_card
        FOREIGN KEY (card_id) REFERENCES `yugioh_db`.`cards` (card_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SHOW TABLES;
