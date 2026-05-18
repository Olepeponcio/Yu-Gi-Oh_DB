-- Reinicio completo del esquema.
-- ADVERTENCIA: este archivo borra tablas y datos.
-- Usar solo en pruebas o cuando se quiera reconstruir la base desde cero.

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS card_linkmarkers;
DROP TABLE IF EXISTS card_typelines;
DROP TABLE IF EXISTS card_banlist;
DROP TABLE IF EXISTS card_prices;
DROP TABLE IF EXISTS card_images;
DROP TABLE IF EXISTS card_sets;
DROP TABLE IF EXISTS cards;

SET FOREIGN_KEY_CHECKS = 1;
