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

## Power BI y analisis

La fuente principal para Power BI deben ser las views de MySQL definidas en:

```text
sql/analysis/views/
```

Estas views conservan la logica SQL sobre las tablas base.

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
