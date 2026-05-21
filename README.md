# Proyecto SQL DB Yu-Gi-Oh

Proyecto de datos para construir una base MySQL de cartas de Yu-Gi-Oh desde la API de YGOPRODeck y dejarla preparada para SQL, analisis y Power BI.

## Piezas del proyecto

```text
sql/main_schema.sql  -> esquema principal vigente para crear la DB desde cero
sql/migrations/      -> reservado para futuras escaladas del modelo
sql/reset_main_schema.sql -> reinicio destructivo de tablas principales
sql/analysis/        -> SQL analitico, views oficiales y CSV locales
src/api/             -> extraccion desde YGOPRODeck
src/etl/             -> transformacion y carga en MySQL
src/csv_sql_scripts/ -> utilidad auxiliar futura para recuperar CSV como SQL
src/database/        -> conexion Python -> MySQL
data/raw/            -> ultimo JSON raw descargado
docs/                -> documentacion tecnica y analitica
```

## Idea clave

```text
main_schema.sql = esquema principal actual
migrations/ = cambios futuros cuando el modelo vuelva a evolucionar
```

El modelo actual, incluyendo `sets`, `rarities` y `card_price_history`, forma parte de `sql/main_schema.sql`.

## Flujo general

```text
1. MySQL crea la estructura desde sql/main_schema.sql
2. Python ETL extrae datos de YGOPRODeck
3. Python transforma y normaliza datos
4. Python carga/actualiza MySQL
5. MySQL expone views analiticas para Power BI
6. Power BI tambien puede consumir CSV locales como snapshots
```

## Herramientas necesarias

- MySQL Server local.
- Cliente MySQL, MySQL Workbench o terminal MySQL.
- Python con dependencias de `requirements.txt`.
- Archivo `.env` con credenciales MySQL.
- Power BI para la fase de dashboard.

## 1. Configurar conexion

Crear `.env` a partir de `.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=yugioh_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
```

`localhost` es el servidor MySQL local. Python se conecta a MySQL solo cuando ejecuta la carga.

## 2. Construir la base desde cero

Crear la base:

```sql
CREATE DATABASE IF NOT EXISTS yugioh_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Crear toda la estructura actual:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

Este paso crea las tablas actuales del proyecto:

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

No uses `reset_main_schema.sql` salvo que quieras borrar tablas y datos para reconstruir desde cero.

## 3. Probar el ETL sin escribir en MySQL

Desde la raiz del proyecto:

```powershell
python -m src.etl.run_etl --dry-run
```

Con JSON local:

```powershell
python -m src.etl.run_etl --source file --raw-path data/raw/cardinfo_latest.json --dry-run
```

## 4. Cargar o actualizar datos

Ejecutar ingesta completa:

```powershell
python -m src.etl.run_etl
```

Este comando:

```text
descarga datos desde la API
actualiza data/raw/cardinfo_latest.json
normaliza cartas, sets, rarezas, precios, banlist e imagenes
actualiza tablas base en MySQL
inserta snapshot historico en card_price_history
```

Para actualizar la DB, se vuelve a ejecutar el mismo comando.

## 5. Preparar analisis y Power BI

Los artefactos analiticos se guardan en:

```text
sql/analysis/views/   -> scripts oficiales CREATE VIEW sobre tablas base MySQL
sql/analysis/CSV/     -> CSV locales exportados, utiles como snapshots para Power BI
```

Power BI debe consumir preferentemente las views de MySQL. Los CSV son una fuente secundaria: conservan resultados exportados, pero no la logica SQL original.

Ejemplo:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/analysis/views/vw_bi_competitive_staples.sql;
```

## Utilidades auxiliares

`src/csv_sql_scripts/` no forma parte del flujo principal actual. Es una utilidad de escalado futuro para leer CSV locales y generar scripts SQL de recuperacion en:

```text
sql/generated/from_csv/
```

Uso opcional:

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```

Esos scripts no sustituyen a las views oficiales de `sql/analysis/views/`.

## Orden rapido

```text
1. Crear yugioh_db
2. SOURCE sql/main_schema.sql
3. python -m src.etl.run_etl --dry-run
4. python -m src.etl.run_etl
5. Crear o ejecutar views oficiales desde sql/analysis/views/
6. Conectar Power BI a MySQL views o a CSV locales si se necesita snapshot
```

## Documentacion

- [Indice tecnico](docs/README.md)
- [Objetivo analitico](docs/analytic_objective.md)
- [Flujo ETL](docs/etl_flow.md)
- [Modelo de datos](docs/data_model.md)
- [Uso SQL](docs/sql_usage.md)
