-- create_or_replace_views.sql
-- Crea o reemplaza todas las views de consumo dentro de yugioh_db.
--
-- Uso:
--   1. Ejecutar primero sql/schema.sql si las tablas madre no existen.
--   2. Desde MySQL: OPCION PARA CONSOLA
--      SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/create_or_replace_views.sql;
--
-- Mantenimiento:
--   - Crear cada view como archivo independiente en sql/views/.
--   - Usar CREATE OR REPLACE VIEW dentro de cada archivo.
--   - Anadir aqui un SOURCE por cada nueva view.
--   - Si mueves el proyecto, actualizar la ruta base de los SOURCE.

SET NAMES utf8mb4;

USE `yugioh_db`;

-- Dimensiones
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_cards_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_sets_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_rarities_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_marketplaces_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_currencies_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_snapshots_descriptive.sql;

-- Hechos
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_prices_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_set_appearances.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_price_variation_predictive.sql;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';
