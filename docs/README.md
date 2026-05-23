# Documentacion del proyecto

Indice documental del proyecto SQL DB Yu-Gi-Oh.

## Finalidad

Proyecto de aprendizaje y portfolio para practicar analisis de datos con un flujo completo:

- ETL en Python desde la API de YGOPRODeck.
- Carga de datos normalizados en MySQL.
- Analisis mediante SQL sobre la base cargada.
- Comunicacion de resultados mediante Power BI.

## Flujo base

```text
MySQL ejecuta sql/main_schema.sql -> crea tablas
Python ejecuta python -m src.etl -> descarga, transforma y carga datos
SQL crea views analiticas sobre las tablas base
Power BI consume MySQL views o CSV locales como snapshots
```

## Grupo 0: gestion del proyecto

Marco de trabajo del repositorio:

- `00_gestion_proyecto/versionado_y_flujo_git.md`: historico hasta `v0.1.0`, modelo de ramas, SemVer y flujo practico.

## Grupo 1: programa Python ETL

Documentacion de desarrollo y uso del programa Python:

- `01_programa_python_etl/etl_flow.md`: flujo API -> JSON raw -> transformacion Python -> MySQL.
- `01_programa_python_etl/sql_usage.md`: creacion del esquema, reinicio y uso SQL conectado al ETL.

## Grupo 2: marco documental de analisis de datos

Marco previo para el analisis. No se implementan nuevos documentos en este paso:

- `02_marco_analisis_datos/README.md`: proceso de puesta en practica del analisis de datos.
- `02_marco_analisis_datos/api_json_analysis.md`: estructura del JSON de YGOPRODeck y entidades candidatas.
- `02_marco_analisis_datos/data_model.md`: tablas, relaciones, claves y criterio de carga.
- `02_marco_analisis_datos/relational_model.svg`: imagen del modelo relacional base.

## Criterio de organizacion

- `README.md` en raiz: comandos principales y estado actual.
- `docs/00_gestion_proyecto/`: versionado, ramas y buenas practicas de gestion del repositorio.
- `docs/01_programa_python_etl/`: documentacion del programa Python y uso operativo.
- `docs/02_marco_analisis_datos/`: marco documental para analisis de datos.
- `sql/`: scripts ejecutables en MySQL.
- `sql/analysis/`: views oficiales, consultas exploratorias y CSV locales.
- `src/`: codigo Python del ETL y utilidades auxiliares.
- `data/raw/`: copias JSON descargadas desde la API.

## Utilidades no principales

`src/csv_sql_scripts/` queda aislado del flujo principal. Sirve para una escalada futura: recuperar CSV analiticos como scripts SQL de staging/view sin ejecutar nada contra MySQL.

## Nota sobre migraciones

`sql/main_schema.sql` representa el esquema principal vigente para construir la base desde cero y `sql/reset_main_schema.sql` reconstruye la base de forma destructiva. `sql/migrations/` queda reservado para futuras escaladas incrementales del modelo.
