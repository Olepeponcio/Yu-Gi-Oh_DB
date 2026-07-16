# Flujo ETL

[Inicio](../../README.md) → [Programa Python y ETL](README.md) → Flujo ETL

## Objetivo

Ejecutar el flujo completo de datos:

```text
API YGOPRODeck -> JSON raw local -> transformacion Python -> MySQL
```

El ETL de carga no crea el esquema. `sql/schema.sql` no es generado por Python: es el modelo SQL definido en el proyecto. La preparación se realiza desde el panel o con `python -m src.etl.reset_mysql --yes` antes de la primera carga.

## Punto de entrada

```text
src/etl/main.py
```

## Responsabilidades

- `src/api/ygoprodeck_client.py`: extrae datos desde la API y guarda el JSON original.
- `src/etl/cli.py`: define argumentos de consola.
- `src/etl/main.py`: punto de entrada del paquete ETL.
- `src/etl/pipeline.py`: coordina extraccion, transformacion y carga.
- `src/etl/reporting.py`: muestra resumen de ejecucion.
- `src/etl/transform/`: normaliza datos por dominio y tabla SQL.
- `src/etl/load.py`: inserta o actualiza datos en MySQL.
- `sql/schema.sql`: crea las tablas necesarias antes de ejecutar el ETL.

El ETL depende del modelo definido en `sql/schema.sql`. Si se cambian columnas o tablas, se ajustan `src/etl/transform/` y `src/etl/load.py`, y la DB se resetea/recrea desde `sql/schema.sql`.

El mismo flujo puede operarse mediante `python -m src.control_panel`. La ventana ejecuta los comandos existentes; no duplica la lógica ETL ni contiene credenciales.

Contrato estructural:

- `sql/schema.sql` es la fuente unica para crear tablas madre.
- Python no crea ni altera la estructura de tablas.
- No se mantienen migraciones incrementales como contrato principal.

## Transformacion

```text
src/etl/transform/
├── __init__.py   -> API publica compatible: from src.etl.transform import transform_cards
├── common.py     -> conversiones, validacion y deduplicacion
├── cards.py      -> carta base, imagenes y banlist
├── sets.py       -> sets, rarezas y relacion carta-set
├── prices.py     -> precios actuales
├── relations.py  -> typelines y linkmarkers
└── pipeline.py   -> coordinador transform_cards
```

## Datos raw

Los datos originales se guardan en:

```text
data/raw/
└── cardinfo_latest.json
```

`cardinfo_latest.json` se sobrescribe en cada ejecucion del ETL. No se conservan snapshots raw historicos porque el historico analitico relevante se almacena en MySQL, especialmente en `card_price_history`.

El JSON raw incluye:

- `ingested_at`: fecha/hora de descarga.
- `source_last_updated`: cabecera `Last-Modified` si la API la informa.
- `record_count`: numero de cartas recibidas.
- `data`: lista original de cartas.

## Ejecucion

Preparar la base y las tablas antes de la primera carga:

```powershell
python -m src.etl.reset_mysql --yes
```

Prueba sin cargar MySQL:

```powershell
python -m src.etl --dry-run
```

Carga completa:

```powershell
python -m src.etl
```

Este comando es tambien el flujo normal de actualizacion.

Reproducir desde JSON local:

```powershell
python -m src.etl --source file --raw-path data/raw/cardinfo_latest.json
```

## Tablas cargadas

- `cards`
- `sets`
- `rarity_types`
- `card_printings`
- `card_images`
- `card_price_history`
- `card_banlist`
- `card_typelines`
- `card_linkmarkers`

## Criterio de escritura

- `cards`, `card_images` y `card_banlist` usan insercion/actualizacion idempotente.
- `sets` y `rarity_types` son catalogos reutilizables.
- `card_price_history` guarda observaciones largas y append-only por cada ejecucion real.
- `card_printings`, `card_typelines` y `card_linkmarkers` se eliminan y recargan por carta para evitar registros obsoletos.
