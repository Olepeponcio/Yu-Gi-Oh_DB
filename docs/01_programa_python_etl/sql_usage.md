# Uso SQL

## Crear estructura

El esquema se crea desde MySQL ejecutando el script del proyecto. Este paso enlaza la base de datos local con las tablas definidas en el repositorio.

`main_schema.sql` no lo genera el programa Python. Primero se disena el modelo SQL, despues se crean las tablas en MySQL y finalmente el ETL carga datos en esa estructura.

Uso normal:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`main_schema.sql` usa `CREATE TABLE IF NOT EXISTS`, por tanto puede ejecutarse varias veces sin borrar datos. El programa Python actual no crea automaticamente las tablas.

Comprobacion basica:

```sql
SHOW TABLES;
DESCRIBE cards;
```

## Cargar datos

Despues de crear las tablas, los datos se empujan desde Python:

```powershell
python -m src.etl
```

Ese comando extrae datos desde YGOPRODeck, guarda el JSON raw, transforma la informacion y la inserta/actualiza en MySQL.

Si se modifica el esquema, hay que validar que la transformacion y la carga Python sigan coincidiendo con las columnas reales de MySQL.

## Reiniciar estructura

Uso destructivo:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/reset_main_schema.sql;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`reset_main_schema.sql` borra tablas y datos. Solo debe usarse cuando se quiera reconstruir la base desde cero.

## Analisis SQL y capa semantica

La fuente principal de analisis deben ser las views de MySQL definidas en:

```text
sql/analysis/views/
sql/analysis/views/diagnostic/
```

Estas views conservan la logica SQL sobre las tablas base. Power BI consume las views oficiales en modo Importar:

```text
vw_dim_*       -> dimensiones
vw_fact_*      -> hechos
vw_bridge_*    -> relaciones muchos-a-muchos
vw_agg_*       -> agregados
vw_desc_*      -> descriptivo auxiliar
vw_ref_*       -> referencias normalizadas
views/diagnostic/vw_diag_* -> diagnostico auxiliar fuera del modelo relacional
```

Views principales actualmente localizadas:

```text
sql/analysis/views/dim/vw_dim_card.sql
sql/analysis/views/dim/vw_dim_set.sql
sql/analysis/views/dim/vw_dim_rarity.sql
sql/analysis/views/bridge/vw_bridge_card_set.sql
sql/analysis/views/bridge/vw_bridge_card_banlist.sql
sql/analysis/views/fact/vw_fact_card_prices.sql
sql/analysis/views/fact/vw_fact_price_history.sql
sql/analysis/views/ref/vw_ref_banlist_status.sql
sql/analysis/views/diagnostic/vw_diag_competitive_staple_candidates.sql
sql/analysis/views/diagnostic/vw_diag_high_demand_archetypes.sql
sql/analysis/views/diagnostic/vw_diag_price_by_rarity.sql
sql/analysis/views/diagnostic/vw_diag_price_outliers.sql
```

Los CSV de `sql/analysis/CSV/` son snapshots locales de resultados exportados. Power BI puede leerlos como tablas independientes, pero no contienen la logica original de joins, filtros o agrupaciones.

## Utilidad auxiliar desde CSV

`src.csv_sql_scripts` no forma parte del flujo principal. Puede usarse en el futuro para generar scripts SQL de recuperacion desde CSV:

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```

El comando escribe en:

```text
sql/generated/from_csv/
```

No ejecuta SQL ni usa credenciales.

## Cambios futuros

`main_schema.sql` contiene el esquema completo vigente para construir la base desde cero.

Si en el futuro se cambia el modelo sobre una base ya en uso, crear una migracion incremental en:

```text
sql/migrations/001_add_column_example.sql
```
