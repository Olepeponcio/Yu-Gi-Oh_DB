# Proyecto SQL DB Yu-Gi-Oh

Proyecto portfolio para practicar un flujo ETL con Python, MySQL y consultas SQL sobre datos de cartas de Yu-Gi-Oh.

El objetivo es construir una base local desde la API de YGOPRODeck, guardar el JSON original, transformar los datos a tablas relacionales y analizarlos con SQL.

## Estado actual

- Conexion Python -> MySQL validada.
- Esquema SQL inicial creado en `sql/schema.sql`.
- Ingesta completa desde YGOPRODeck implementada.
- JSON original guardado en `data/raw/`.
- Tablas cargadas: `cards`, `card_sets`, `card_images`, `card_prices`, `card_banlist`, `card_typelines`, `card_linkmarkers`.
- Consultas de calidad creadas en `sql/queries/01_data_quality.sql`.

## Estructura

```text
proyecto_SQL-DB_Yu-Gi-Oh/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── README.md
│   ├── api_json_analysis.md
│   ├── data_model.md
│   ├── etl_flow.md
│   └── sql_usage.md
├── sql/
│   ├── queries/
│   │   └── 01_data_quality.sql
│   ├── reset_schema.sql
│   └── schema.sql
├── src/
│   ├── api/
│   │   └── ygoprodeck_client.py
│   ├── database/
│   │   └── connection.py
│   └── etl/
│       ├── load.py
│       ├── run_etl.py
│       └── transform.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Comandos principales

Crear estructura SQL:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

Probar ETL sin cargar MySQL:

```powershell
python -m src.etl.run_etl --dry-run
```

Ejecutar ingesta completa:

```powershell
python -m src.etl.run_etl
```

Reproducir desde JSON local:

```powershell
python -m src.etl.run_etl --source file --raw-path data/raw/cardinfo_latest.json --dry-run
```

Ejecutar calidad de datos:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/queries/01_data_quality.sql;
```

## Documentacion

- [Indice de documentacion](docs/README.md)
- [Analisis JSON API](docs/api_json_analysis.md)
- [Flujo ETL](docs/etl_flow.md)
- [Modelo de datos](docs/data_model.md)
- [Uso SQL](docs/sql_usage.md)
