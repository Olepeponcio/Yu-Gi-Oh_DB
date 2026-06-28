# Proyecto SQL DB Yu-Gi-Oh

Base del proyecto: construir una base MySQL relacional con datos de cartas de Yu-Gi-Oh obtenidos desde YGOPRODeck.

## Estado del proyecto

Punto limpio.

El repositorio conserva:

- Premisas del modelo.
- Esquema relacional madre.
- ETL Python para cargar MySQL.
- Tests del ETL.
- Documentacion minima del modelo y del flujo.

No hay analisis consolidado ni capa intermedia. El trabajo analitico empieza desde este punto.

## Estructura base

```text
sql/main_schema.sql       -> crea las tablas madre
sql/RESET_SCHEMA.sql      -> borra y recrea yugioh_db vacia
src/api/                  -> cliente YGOPRODeck
src/etl/                  -> transformacion y carga
src/database/             -> conexion MySQL
docs/                     -> documentacion base
tests/                    -> pruebas del ETL
data/raw/                 -> ubicacion del JSON raw local
data/processed/           -> reservado para salidas procesadas locales
data/reporting/           -> reportes locales de ejecucion
```

## Tablas madre

`sql/main_schema.sql` define:

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

## Crear la base

```sql
CREATE DATABASE IF NOT EXISTS yugioh_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

## Reset completo

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/RESET_SCHEMA.sql;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`RESET_SCHEMA.sql` borra `yugioh_db` completa y la crea de nuevo vacia.

## Ejecutar ETL

Preparar entorno:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configurar `.env` desde `.env.example`.

Prueba sin escribir en MySQL:

```powershell
python -m src.etl --dry-run
```

Carga:

```powershell
python -m src.etl
```

Tests:

```powershell
python -m unittest discover
```

## Documentacion

- [Uso SQL](docs/01_programa_python_etl/sql_usage.md)
- [Flujo ETL](docs/01_programa_python_etl/etl_flow.md)
- [Analisis JSON API](docs/02_marco_analisis_datos/api_json_analysis.md)
- [Modelo de datos](docs/02_marco_analisis_datos/data_model.md)
