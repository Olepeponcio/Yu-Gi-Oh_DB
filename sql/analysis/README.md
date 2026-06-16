# SQL de analisis

Directorio para scripts SQL de la fase analitica.

Uso previsto:

```text
sql/analysis/queries/              -> consultas exploratorias y de validacion
sql/analysis/queries/descriptive/  -> analisis descriptivo
sql/analysis/queries/diagnostic/   -> analisis diagnostico
sql/analysis/views/                -> views descriptivas y futuras views semanticas
sql/analysis/views/diagnostic/     -> views diagnosticas fuera del modelo relacional
sql/analysis/CSV/                  -> CSV locales exportados desde consultas previas, consumibles por Power BI como snapshots
```

Los scripts de `views/` se ejecutan desde MySQL sobre `yugioh_db` y quedan versionados en el proyecto.

## Criterio de uso

```text
queries/ = exploracion previa, pruebas de logica y validacion de hipotesis
views/ = logica SQL oficial, estable y reutilizable sobre MySQL
views/diagnostic/ = diagnostico estable, no parte del modelo relacional
CSV/ = resultados exportados, utiles como respaldo o fuente snapshot
sql/generated/from_csv/ = recuperacion auxiliar fuera de analysis
```

Power BI queda pausado. La criba actual se aplica primero en MySQL `yugioh_db`: separar views semanticas futuras de views diagnosticas.

La capa esperada queda separada en:

```text
vw_dim_*                  = dimensiones del modelo semantico
vw_fact_*                 = hechos granulares del modelo semantico
vw_bridge_*               = relaciones muchos-a-muchos
vw_agg_*                  = agregados calculados sobre dimensiones/hechos
vw_desc_*                 = descriptivo auxiliar
vw_ref_*                  = catalogos de referencia
views/diagnostic/vw_diag_* = diagnostico auxiliar fuera del modelo relacional
```

Los CSV pueden usarse cuando interese trabajar con una foto fija del resultado.

## Convencion de nombres

Las consultas exploratorias se agrupan por nivel de analisis:

```text
descriptive/ = que existe, cuanto hay, distribuciones basicas
diagnostic/ = relaciones, diferencias, variaciones y posibles causas
```

Las consultas exploratorias usan prefijo de archivo:

```text
queries/descriptive/q_desc_... = consulta descriptiva
queries/diagnostic/q_diag_... = consulta diagnostica
```

Las views se segmentan por funcion:

```text
views/vw_desc_... = view descriptiva
views/vw_dim_... = dimension semantica
views/vw_fact_... = hecho semantico
views/vw_bridge_... = puente relacional
views/vw_agg_... = agregado analitico
views/vw_ref_... = referencia normalizada
views/diagnostic/vw_diag_... = view diagnostica
```

Flujo recomendado:

```text
query exploratoria -> validacion -> CREATE VIEW estable -> MySQL yugioh_db
```

## Catalogo inicial de views

Views actuales:

```text
views/vw_fact_card_prices.sql
views/diagnostic/vw_diag_competitive_staple_candidates.sql
views/diagnostic/vw_diag_high_demand_archetypes.sql
views/diagnostic/vw_diag_price_by_rarity.sql
views/diagnostic/vw_diag_price_outliers.sql
```

Consulta candidata a view estable:

```text
queries/diagnostic/q_diag_price_variation_usd.sql
```

Consultas exploratorias actuales:

```text
queries/descriptive/q_desc_card_avg_marketplace_price.sql
queries/descriptive/q_desc_cards_by_set_count.sql
queries/descriptive/q_desc_price_distribution_by_marketplace.sql
queries/descriptive/q_desc_price_history_snapshots.sql
queries/diagnostic/q_diag_card_rarity_printings.sql
queries/diagnostic/q_diag_price_variation_usd.sql
queries/diagnostic/q_diag_relevant_price_increases.sql
```

Dependencias principales sobre tablas base:

```text
cards
sets
rarities
card_sets
card_prices
card_price_history
card_banlist
```

Views candidatas para convertir consultas en capa estable:

| Nombre de view | Problema que resuelve |
|---|---|
| `vw_dim_card` | Carta como entidad principal de filtro y relacion. |
| `vw_dim_set` | Set como entidad de analisis comercial. |
| `vw_dim_rarity` | Rareza como categoria de segmentacion. |
| `vw_ref_banlist_status` | Estados normalizados de banlist. |
| `vw_bridge_card_set` | Relacion carta-set-rareza-codigo. |
| `vw_fact_card_prices` | Precios actuales por marketplace. |
| `vw_fact_price_history` | Historico por snapshot de ETL. |
| `vw_agg_card_price_current` | Precio actual resumido por carta. |
| `vw_agg_set_value` | Valor potencial acumulado por set. |
| `vw_diag_cards_without_price` | Cartas sin precio. |
| `vw_diag_orphan_relations` | Relaciones sin entidad padre valida. |
| `vw_diag_price_outliers` | Valores de precio extremos. |

Las futuras `vw_dim_*`, `vw_fact_*`, `vw_bridge_*` y `vw_agg_*` deben apoyarse en tablas base y producir salidas limpias. No se crean automaticamente en este repositorio en esta fase.

## Utilidad auxiliar desde CSV

`src.csv_sql_scripts` puede generar scripts SQL de staging/view desde CSV locales:

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```

Por cada CSV se crea un script en `sql/generated/from_csv/` con:

```text
CREATE TABLE IF NOT EXISTS staging_...
CREATE OR REPLACE VIEW vw_... AS SELECT ... FROM staging_...
```

El modulo solo genera archivos `.sql`; no conecta con MySQL ni ejecuta cambios en la base. Es una herramienta futura de recuperacion, no el flujo analitico principal.
