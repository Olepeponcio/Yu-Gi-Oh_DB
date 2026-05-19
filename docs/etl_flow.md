# Flujo ETL

## Objetivo

Ejecutar el flujo completo:

```text
API YGOPRODeck -> JSON raw local -> transformacion Python -> MySQL
```

## Punto de entrada

```text
src/etl/run_etl.py
```

## Responsabilidades

- `src/api/ygoprodeck_client.py`: extrae datos desde la API y guarda el JSON original.
- `src/etl/transform.py`: normaliza datos por tabla SQL.
- `src/etl/load.py`: carga datos en MySQL.
- `src/etl/run_etl.py`: coordina extraccion, transformacion y carga.

## Datos raw

Los datos originales se guardan en:

```text
data/raw/
├── cardinfo_YYYYMMDD_HHMMSS.json
└── cardinfo_latest.json
```

El JSON raw incluye:

- `ingested_at`: fecha/hora de descarga.
- `source_last_updated`: cabecera `Last-Modified` si la API la informa.
- `record_count`: numero de cartas recibidas.
- `data`: lista original de cartas.

## Ejecucion

Prueba sin cargar MySQL:

```powershell
python -m src.etl.run_etl --dry-run
```

Carga completa:

```powershell
python -m src.etl.run_etl
```

Reproducir desde JSON local:

```powershell
python -m src.etl.run_etl --source file --raw-path data/raw/cardinfo_latest.json
```

## Tablas cargadas

- `cards`
- `card_sets`
- `card_images`
- `card_prices`
- `card_banlist`
- `card_typelines`
- `card_linkmarkers`
