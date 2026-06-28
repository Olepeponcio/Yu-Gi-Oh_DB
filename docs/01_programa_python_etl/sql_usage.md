# Uso SQL

## Crear estructura

El esquema se crea desde MySQL ejecutando el script principal del proyecto.

`main_schema.sql` no lo genera Python. Primero se define el modelo SQL, despues se crean las tablas en MySQL y finalmente el ETL carga datos en esa estructura.

Uso normal:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`main_schema.sql` usa `CREATE TABLE IF NOT EXISTS`, por tanto puede ejecutarse varias veces sin borrar datos.

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

## Reiniciar estructura

Uso destructivo:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/reset_main_schema.sql;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`reset_main_schema.sql` borra tablas y datos. Solo debe usarse cuando se quiera reconstruir la base desde cero.

## Analisis SQL

La fuente principal de analisis son las tablas madre de MySQL:

```text
cards
sets
rarities
card_sets
card_images
card_prices
card_price_history
card_banlist
card_typelines
card_linkmarkers
```

Las consultas viven en:

```text
sql/analysis/queries/
```

Funcion de las consultas:

- Convertir hechos en preguntas.
- Validar calidad e integridad.
- Detectar outliers o relaciones relevantes.
- Probar criterios comerciales antes de llevarlos a Power BI.

No hay capa SQL intermedia oficial. Power BI debe conectarse a tablas base y construir alli el modelo semantico, medidas y clasificaciones.

## Cambios futuros

`main_schema.sql` contiene el esquema completo vigente para construir la base desde cero.

Si en el futuro se cambia el modelo sobre una base ya en uso, crear una migracion incremental en:

```text
sql/migrations/001_add_column_example.sql
```
