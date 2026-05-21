# Documentacion del proyecto

Indice del marco tecnico del proyecto. El README raiz contiene la guia operativa; esta carpeta conserva explicaciones, decisiones y consultas de apoyo.

## Flujo documentado

```text
MySQL ejecuta sql/main_schema.sql -> crea tablas
Python ejecuta python -m src.etl.run_etl -> descarga, transforma y carga datos
SQL crea views analiticas sobre las tablas base
Power BI consume MySQL views o CSV locales como snapshots
```

## Documentos

- `api_json_analysis.md`: estructura del JSON de YGOPRODeck y entidades candidatas.
- `analytic_objective.md`: objetivo de negocio, preguntas analiticas y marco Power BI.
- `data_model.md`: tablas, relaciones, claves y criterio de carga.
- `etl_flow.md`: flujo API -> JSON raw -> transformacion Python -> MySQL.
- `sql_usage.md`: creacion del esquema, reinicio y uso analitico.

## Criterio de organizacion

- `README.md` en raiz: comandos principales y estado actual.
- `docs/`: marco tecnico reutilizable.
- `sql/`: scripts ejecutables en MySQL.
- `sql/analysis/`: views oficiales, consultas exploratorias y CSV locales.
- `src/`: codigo Python del ETL y utilidades auxiliares.
- `data/raw/`: copias JSON descargadas desde la API.

## Utilidades no principales

`src/csv_sql_scripts/` queda aislado del flujo principal. Sirve para una escalada futura: recuperar CSV analiticos como scripts SQL de staging/view sin ejecutar nada contra MySQL.

## Nota sobre migraciones

`sql/main_schema.sql` representa el esquema principal vigente para construir la base desde cero y `sql/reset_main_schema.sql` reconstruye la base de forma destructiva. `sql/migrations/` queda reservado para futuras escaladas incrementales del modelo.
