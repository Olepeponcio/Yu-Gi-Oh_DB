# Proyecto SQL DB Yu-Gi-Oh

Proyecto de datos para construir una base MySQL de cartas de Yu-Gi-Oh desde la API de YGOPRODeck y dejarla preparada para SQL, analisis y Power BI.

## Piezas del proyecto

```text
sql/schema.sql       -> esquema completo vigente para crear la DB desde cero
sql/migrations/      -> reservado para futuras escaladas del modelo
sql/reset_schema.sql -> reinicio destructivo de tablas
sql/queries/         -> consultas de calidad de datos
sql/analysis/        -> vistas y consultas de la fase analitica
src/api/             -> extraccion desde YGOPRODeck
src/etl/             -> transformacion y carga en MySQL
src/database/        -> conexion Python -> MySQL
data/raw/            -> ultimo JSON raw descargado
docs/                -> documentacion tecnica y analitica
```

## Idea clave

```text
schema.sql = esquema completo actual
migrations/ = cambios futuros cuando el modelo vuelva a evolucionar
```

El modelo actual, incluyendo `sets`, `rarities` y `card_price_history`, forma parte de `sql/schema.sql`.

## Flujo general

```text
1. MySQL crea la estructura desde sql/schema.sql
2. Python ETL extrae datos de YGOPRODeck
3. Python transforma y normaliza datos
4. Python carga/actualiza MySQL
5. SQL valida calidad
6. MySQL expone vistas para Power BI
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
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=yugioh_db
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
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
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

No uses `reset_schema.sql` salvo que quieras borrar tablas y datos para reconstruir desde cero.

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

## 5. Validar calidad de datos

Ejecutar desde MySQL:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/queries/01_data_quality.sql;
```

## 6. Preparar analisis y Power BI

Las vistas y consultas analiticas se guardan en:

```text
sql/analysis/views/
sql/analysis/queries/
```

Ejemplo futuro:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/analysis/views/01_powerbi_views.sql;
```

Power BI se conecta a MySQL y consume preferentemente vistas.

## Orden rapido

```text
1. Crear yugioh_db
2. SOURCE sql/schema.sql
3. python -m src.etl.run_etl --dry-run
4. python -m src.etl.run_etl
5. SOURCE sql/queries/01_data_quality.sql
6. Crear consultas/vistas en sql/analysis/
```

## Documentacion

- [Indice tecnico](docs/README.md)
- [Objetivo analitico](docs/analytic_objective.md)
- [Flujo ETL](docs/etl_flow.md)
- [Modelo de datos](docs/data_model.md)
- [Uso SQL](docs/sql_usage.md)
