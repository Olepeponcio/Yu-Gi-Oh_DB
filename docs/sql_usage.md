# Uso SQL

## Crear estructura

El esquema se crea desde MySQL ejecutando el script del proyecto. Este paso enlaza la base de datos local con las tablas definidas en el repositorio.

`schema.sql` no lo genera el programa Python. Primero se disena el modelo SQL, despues se crean las tablas en MySQL y finalmente el ETL carga datos en esa estructura.

Uso normal:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

`schema.sql` usa `CREATE TABLE IF NOT EXISTS`, por tanto puede ejecutarse varias veces sin borrar datos. El programa Python actual no crea automaticamente las tablas.

Comprobacion basica:

```sql
SHOW TABLES;
DESCRIBE cards;
```

## Cargar datos

Despues de crear las tablas, los datos se empujan desde Python:

```powershell
python -m src.etl.run_etl
```

Ese comando extrae datos desde YGOPRODeck, guarda el JSON raw, transforma la informacion y la inserta/actualiza en MySQL.

Si se modifica el esquema, hay que validar que la transformacion y la carga Python sigan coincidiendo con las columnas reales de MySQL.

## Reiniciar estructura

Uso destructivo:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/reset_schema.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

`reset_schema.sql` borra tablas y datos. Solo debe usarse cuando se quiera reconstruir la base desde cero.

## Consultas de calidad

Ejecutar:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/queries/01_data_quality.sql;
```

El archivo valida:

- conteos por tabla,
- campos obligatorios vacios,
- duplicados logicos,
- filas huerfanas,
- cartas sin imagen o precios,
- precios invalidos,
- posiciones duplicadas en listas normalizadas.

## Cambios futuros

`schema.sql` contiene el esquema completo vigente para construir la base desde cero.

Si en el futuro se cambia el modelo sobre una base ya en uso, crear una migracion incremental en:

```text
sql/migrations/001_add_column_example.sql
```
