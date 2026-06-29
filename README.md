# Proyecto SQL DB Yu-Gi-Oh

Base del proyecto: programa Python + MySQL para extraer, transformar y cargar datos de cartas de Yu-Gi-Oh desde YGOPRODeck.

Este README explica como esta construido el programa y como llega hasta la creacion/carga de las tablas madre.

## 1. Objetivo del programa

```text
API YGOPRODeck -> JSON raw local -> transformacion Python -> tablas madre MySQL
```

El programa no contiene analisis consolidado. Su responsabilidad termina cuando MySQL queda cargado con el modelo relacional madre.

## 2. Estructura principal

```text
src/api/                  -> extraccion desde YGOPRODeck
src/etl/                  -> orquestacion ETL
src/etl/transform/        -> normalizacion por dominio
src/database/             -> conexion MySQL
sql/schema.sql            -> crea las tablas madre dentro de yugioh_db
docs/                     -> documentacion de trabajo
tests/                    -> pruebas del ETL
data/raw/                 -> JSON raw local
data/processed/           -> reservado para datos procesados locales
data/reporting/           -> reportes locales de ejecucion
```

## 3. Modulos de `src`

### `src/api`

Responsabilidad: obtener datos desde YGOPRODeck.

Archivo principal:

```text
src/api/ygoprodeck_client.py
```

Hace:

- Llama al endpoint publico de cartas.
- Guarda una copia raw en `data/raw/cardinfo_latest.json`.
- Conserva metadatos de ingesta cuando estan disponibles.

### `src/database`

Responsabilidad: abrir conexion con MySQL.

Archivo principal:

```text
src/database/connection.py
```

Usa variables de `.env`:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

### `src/etl`

Responsabilidad: coordinar el flujo completo.

Entradas:

```text
src/etl/__main__.py
src/etl/main.py
src/etl/cli.py
```

Orquestacion:

```text
src/etl/pipeline.py
```

Carga:

```text
src/etl/load.py
```

Reporte:

```text
src/etl/reporting.py
src/etl/report_file.py
```

### `src/etl/transform`

Responsabilidad: convertir el JSON de la API en filas compatibles con MySQL.

```text
common.py     -> conversiones, validacion y deduplicacion
cards.py      -> carta base, imagenes y banlist
sets.py       -> sets, rarezas y apariciones carta-set
prices.py     -> precios actuales por marketplace
relations.py  -> typelines y linkmarkers
pipeline.py   -> coordinador de transformacion
```

## 4. Flujo ETL

```text
1. Leer argumentos de CLI.
2. Descargar JSON o leer JSON local.
3. Normalizar entidades.
4. Validar claves y campos requeridos.
5. Insertar/actualizar tablas madre.
6. Registrar snapshot de precios en card_price_history.
7. Emitir resumen de ejecucion.
```

## 5. Tablas madre

`sql/schema.sql` crea:

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

## 6. Preparar entorno

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configurar `.env` desde `.env.example`.

Regla de seguridad:

- El ETL debe conectarse con un usuario MySQL limitado, por ejemplo `pepin`.
- No usar `root` para ejecutar cargas normales.
- `.env` guarda las credenciales locales y no se versiona.

## 7. Preparar MySQL

Proceso base:

- Crear manualmente el schema `yugioh_db` en MySQL.
- Ejecutar `sql/schema.sql` para crear las tablas madre.
- Conceder al usuario de ETL permisos limitados sobre `yugioh_db`.
- Ejecutar el ETL para cargar o actualizar datos desde la API.

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

## 8. Ejecutar

Prueba sin escribir:

```powershell
python -m src.etl --dry-run
```

Carga completa:

```powershell
python -m src.etl
```

Desde JSON local:

```powershell
python -m src.etl --source file --raw-path data/raw/cardinfo_latest.json
```

Tests:

```powershell
python -m unittest discover
```

## 9. README principales

```text
README.md                              -> programa Python y ETL hasta tablas madre
docs/02_marco_analisis_datos/README.md -> diario del proceso de analisis
docs/03_powerbi/README.md              -> proceso de trabajo en Power BI
```
