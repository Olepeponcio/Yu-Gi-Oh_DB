# Documentacion del proyecto

Indice documental del proyecto SQL DB Yu-Gi-Oh.

## Funcion de este README

Este archivo solo sirve como mapa de documentos. No define preguntas analiticas, flujo operativo ni convenciones SQL.

Referencias principales:

```text
README.md                         -> entrada rapida y comandos principales
docs/02_marco_analisis_datos/README.md -> decision, alcance y preguntas marco
sql/analysis/README.md            -> organizacion de queries y views SQL
powerbi/README.md                 -> modelo Power BI, relaciones y artefactos
```

## Grupo 0: gestion del proyecto

- `00_gestion_proyecto/versionado_y_flujo_git.md`: versionado, ramas, SemVer y flujo practico.
- `00_gestion_proyecto/revision_seguridad_publicacion.md`: revision de secretos, datos locales y riesgos antes de publicacion publica.

## Grupo 1: programa Python ETL

- `01_programa_python_etl/etl_flow.md`: flujo API -> JSON raw -> transformacion Python -> MySQL.
- `01_programa_python_etl/sql_usage.md`: creacion del esquema, reinicio y uso SQL conectado al ETL.

## Grupo 2: marco de analisis de datos

- `02_marco_analisis_datos/README.md`: fuente canonica de decision, alcance y preguntas marco.
- `02_marco_analisis_datos/api_json_analysis.md`: estructura del JSON de YGOPRODeck y entidades candidatas.
- `02_marco_analisis_datos/data_model.md`: tablas, relaciones, claves, criterio de carga y modelo semantico por views.
- `02_marco_analisis_datos/relational_model.svg`: imagen del modelo relacional base.
- `02_marco_analisis_datos/infografia_views_sql.svg`: mapa visual de views SQL.
