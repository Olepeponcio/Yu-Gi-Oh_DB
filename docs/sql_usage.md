# Uso SQL

## Crear estructura

Uso normal:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

`schema.sql` usa `CREATE TABLE IF NOT EXISTS`, por tanto puede ejecutarse varias veces sin borrar datos.

Comprobacion basica:

```sql
SHOW TABLES;
DESCRIBE cards;
```

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

`schema.sql` crea la estructura inicial, pero no modifica tablas existentes.

Si se cambia el modelo, conviene crear migraciones:

```text
sql/migrations/001_add_column_example.sql
```
