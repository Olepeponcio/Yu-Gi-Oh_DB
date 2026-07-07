-- security_etl_user.sql
-- Plantilla de seguridad para un usuario ETL local con permisos minimos.
--
-- Antes de ejecutar, sustituir etl_user por el usuario local elegido.
-- Ejecutar con un usuario administrador de MySQL.
-- MySQL devolvera una password aleatoria si el usuario no existe.
-- Copiar esa password solo al `.env` local. No guardarla en Git.

CREATE USER IF NOT EXISTS 'etl_user'@'localhost'
IDENTIFIED BY RANDOM PASSWORD;

REVOKE ALL PRIVILEGES, GRANT OPTION
FROM 'etl_user'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE
ON `yugioh_db`.*
TO 'etl_user'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'etl_user'@'localhost';
