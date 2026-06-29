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

-- Descriptivo
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_cards_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_sets_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_rarities_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_rarity_names_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_marketplaces_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_currencies_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_dim_snapshots_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_set_coverage_descriptive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_prices_descriptive.sql;

-- Diagnostico
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_set_coverage_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_current_prices_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_price_outlier_candidates_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_rarity_price_summary_diagnostic.sql;

-- Diagnostico / calidad de modelo
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_quality_duplicate_grain_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_quality_fk_orphans_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_quality_nullable_fk_diagnostic.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_quality_relationship_summary_diagnostic.sql;

-- Predictivo
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_price_snapshot_summary_predictive.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/views/vw_fact_card_price_variation_predictive.sql;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';
