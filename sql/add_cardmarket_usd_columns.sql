-- Añade la columna USD calculada de Cardmarket a una base existente.
-- Ejecutar una sola vez antes de cargar el ETL actualizado.

USE `yugioh_db`;

ALTER TABLE `yugioh_db`.`card_prices`
    ADD COLUMN cardmarket_usd DECIMAL(10,2) NULL AFTER cardmarket_price;

ALTER TABLE `yugioh_db`.`card_price_history`
    ADD COLUMN cardmarket_usd DECIMAL(10,2) NULL AFTER cardmarket_price;
