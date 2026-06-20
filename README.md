# Proyecto SQL DB Yu-Gi-Oh

Proyecto de datos para construir una base MySQL de cartas de Yu-Gi-Oh desde la API de YGOPRODeck, analizarla con SQL y comunicar resultados en Power BI.

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
powerbi/             -> documentacion, consultas y plantillas Power BI
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
5. MySQL expone views semanticas y diagnosticas
6. Power BI consume las views oficiales en modo Importar
7. Power BI construye el modelo relacional, medidas y narrativa
```

## Herramientas necesarias

- MySQL Server local.
- Cliente MySQL, MySQL Workbench o terminal MySQL.
- Python con dependencias de `requirements.txt`.
- Archivo `.env` con credenciales MySQL.
- Power BI Desktop para construir el modelo y exportar plantilla `.pbit`.

## 0. Preparar entorno Python

Desde PowerShell, en la raiz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

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
python -m src.etl --dry-run
```

Con JSON local:

```powershell
python -m src.etl --source file --raw-path data/raw/cardinfo_latest.json --dry-run
```

Ejecutar tests del ETL:

```powershell
python -m unittest discover
```

## 4. Cargar o actualizar datos

Ejecutar ingesta completa:

```powershell
python -m src.etl
```

Este comando:

```text
descarga datos desde la API
actualiza data/raw/cardinfo_latest.json
normaliza cartas, sets, rarezas, precios, banlist e imagenes
actualiza tablas base en MySQL
inserta snapshot historico en card_price_history
guarda un reporte .txt en data/reporting/
```

Los reportes se nombran con formato ordenable por fecha:

```text
data/reporting/etl_report_YYYYMMDD_HHMMSS.txt
```

Para actualizar la DB, se vuelve a ejecutar el mismo comando.

## 5. Preparar analisis SQL y Power BI

El origen de preguntas, problemas y decisiones analiticas vive en:

```text
docs/02_marco_analisis_datos/README.md
```

Los artefactos de implementacion se separan por capa:

```text
sql/analysis/README.md -> organizacion SQL, queries y views
powerbi/README.md      -> modelo Power BI, relaciones, medidas y plantilla
```

Los README de SQL y Power BI no deben redefinir las preguntas marco; solo explican como se implementan.

Ejemplo:

```sql
USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/analysis/views/fact/vw_fact_card_prices.sql;
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
3. python -m src.etl --dry-run
4. python -m src.etl
5. Crear o ejecutar views oficiales desde sql/analysis/views/
6. Mantener views diagnosticas en sql/analysis/views/diagnostic/
7. Cargar views en Power BI en modo Importar
8. Exportar plantilla `.pbit` sin datos cargados
```

## Documentacion

- [Indice tecnico](docs/README.md)
- [Versionado y flujo Git](docs/00_gestion_proyecto/versionado_y_flujo_git.md)
- [Flujo ETL](docs/01_programa_python_etl/etl_flow.md)
- [Uso SQL](docs/01_programa_python_etl/sql_usage.md)
- [Analisis JSON API](docs/02_marco_analisis_datos/api_json_analysis.md)
- [Modelo de datos](docs/02_marco_analisis_datos/data_model.md)
