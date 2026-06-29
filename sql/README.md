# SQL de analisis

Este directorio contiene consultas y vistas de consumo creadas a partir de las tablas madre.

El punto de partida son las tablas madre creadas por:

```text
sql/schema.sql
```

## Estructura

```text
sql/views/   -> vistas de consumo con sufijo por bloque analitico
```

Plantilla de creacion/reemplazo:

```text
sql/create_or_replace_views.sql           -> consola mysql, usa SOURCE
sql/create_or_replace_views_workbench.sql -> hoja SQL / MySQL Workbench, no usa SOURCE
```

Uso en consola `mysql`:

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/create_or_replace_views.sql;
```

Uso en hoja SQL / MySQL Workbench:

```text
abrir y ejecutar sql/create_or_replace_views_workbench.sql
```

Nota: `SOURCE` es un comando del cliente `mysql`, no SQL estandar. Por eso una hoja SQL puede marcarlo como error.

## Vistas actuales

| Vista | Bloque | Tipo | Grano |
|---|---|---|---|
| `vw_dim_cards_descriptive` | Descriptivo | Dimension | 1 carta |
| `vw_fact_card_set_coverage_descriptive` | Descriptivo | Hecho agregado | 1 carta |
| `vw_fact_card_prices_descriptive` | Descriptivo | Hecho | 1 carta + 1 marketplace + 1 moneda |
| `vw_fact_card_set_coverage_diagnostic` | Diagnostico | Hecho agregado | 1 carta |
| `vw_fact_current_prices_diagnostic` | Diagnostico | Hecho | 1 carta + 1 fuente de precio + 1 moneda |
| `vw_fact_price_outlier_candidates_diagnostic` | Diagnostico | Hecho filtrado/revision | 1 carta + 1 fuente de precio + 1 moneda |
| `vw_fact_rarity_price_summary_diagnostic` | Diagnostico | Hecho agregado | 1 rareza |
| `vw_quality_fk_orphans_diagnostic` | Diagnostico/calidad | Quality | 1 relacion validada |
| `vw_quality_nullable_fk_diagnostic` | Diagnostico/calidad | Quality | 1 control nullable |
| `vw_quality_duplicate_grain_diagnostic` | Diagnostico/calidad | Quality | 1 duplicado de grano |
| `vw_quality_relationship_summary_diagnostic` | Diagnostico/calidad | Quality | 1 tabla hija |
| `vw_fact_price_snapshot_summary_predictive` | Predictivo | Hecho agregado | 1 snapshot |
| `vw_fact_card_price_variation_predictive` | Predictivo | Hecho | 1 carta + 1 marketplace + 1 moneda + 1 snapshot |

Consulta descriptiva en `sql/queries/descriptivo/`:

| Consulta | Tipo | Grano |
|---|---|---|
| `vw_dim_cards_classification` | Lectura descriptiva | 1 combinacion de atributos de carta |

## Reglas de diseno

- Declarar el grano de cada vista antes de crearla.
- No mezclar EUR y USD en una misma metrica sin conversion explicita.
- Usar `UNION ALL` para transformar precios de columnas a formato largo.
- Usar `JOIN` para enriquecer con atributos; no usar `UNION` para mezclar granos.
- Las vistas de revision, como precios extremos, deben depender de una vista base estable.
- Las vistas `vw_quality_*` son controles de fiabilidad del modelo; no son vistas de negocio.
- Las vistas predictivas leen `card_price_history`; no insertan ni actualizan snapshots.
- Cada nueva view debe anadirse a `sql/create_or_replace_views.sql`.

## Historico de precios

El artefacto persistente del historico es la tabla:

```text
card_price_history
```

La carga ETL inserta una fila por carta con precio y `snapshot_at` en cada ejecucion real. Las views predictivas solo consultan ese historico:

```text
card_price_history -> vw_fact_price_snapshot_summary_predictive
card_price_history -> vw_fact_card_price_variation_predictive
```

## Vista de revision

`vw_fact_price_outlier_candidates_diagnostic` depende de `vw_fact_current_prices_diagnostic`.

Grano esperado:

```text
1 carta + 1 fuente de precio + 1 moneda + 1 precio candidato
```

Uso:

```text
localizar precios que exigen revision antes de interpretar
```
