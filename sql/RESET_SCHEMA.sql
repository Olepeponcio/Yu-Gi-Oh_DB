-- RESET_SCHEMA.sql
-- Limpia por completo la base yugioh_db y la deja creada, vacia y lista
-- para volver a ejecutar sql/main_schema.sql.
--
-- ADVERTENCIA: borra todos los datos de yugioh_db.

DROP DATABASE IF EXISTS yugioh_db;

CREATE DATABASE yugioh_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE yugioh_db;
