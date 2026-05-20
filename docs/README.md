# Documentacion del proyecto

Indice del marco tecnico del proyecto. El README raiz contiene la guia operativa; esta carpeta conserva explicaciones, decisiones y consultas de apoyo.

## Flujo documentado

```text
MySQL ejecuta sql/schema.sql -> crea tablas
Python ejecuta python -m src.etl.run_etl -> descarga, transforma y carga datos
Power BI / SQL -> consumen la base resultante
```

## Documentos

- `api_json_analysis.md`: estructura del JSON de YGOPRODeck y entidades candidatas.
- `analytic_objective.md`: objetivo de negocio, preguntas analiticas y marco Power BI.
- `data_model.md`: tablas, relaciones, claves y criterio de carga.
- `etl_flow.md`: flujo API -> JSON raw -> transformacion Python -> MySQL.
- `sql_usage.md`: creacion del esquema, reinicio y consultas de validacion.

## Criterio de organizacion

- `README.md` en raiz: comandos principales y estado actual.
- `docs/`: marco tecnico reutilizable.
- `sql/`: scripts ejecutables en MySQL.
- `sql/analysis/`: vistas y consultas de la fase analitica.
- `src/`: codigo Python del ETL.
- `data/raw/`: copias JSON descargadas desde la API.

## Nota sobre migraciones

`sql/schema.sql` representa el esquema completo vigente para construir la base desde cero y `sql/reset_schema.sql` reconstruye la base de forma destructiva. `sql/migrations/` queda reservado para futuras escaladas incrementales del modelo.
