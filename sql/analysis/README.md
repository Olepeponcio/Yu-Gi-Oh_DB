# SQL de analisis

Directorio de implementacion SQL para responder al marco canonico:

```text
docs/02_marco_analisis_datos/README.md
```

Este README no define preguntas analiticas. Solo documenta organizacion, convenciones y artefactos SQL.

## Estructura

```text
queries/              -> consultas exploratorias y reglas en validacion
queries/descriptive/  -> analisis descriptivo
queries/diagnostic/   -> analisis diagnostico
views/                -> views estables sobre MySQL yugioh_db
views/dim/            -> dimensiones del modelo semantico
views/bridge/         -> relaciones muchos-a-muchos
views/fact/           -> hechos granulares
views/ref/            -> catalogos normalizados
views/diagnostic/     -> diagnostico auxiliar fuera del nucleo relacional
CSV/                  -> snapshots CSV locales si se necesitan
```

## Criterio de uso

```text
query exploratoria -> validacion -> view estable -> consumo Power BI
```

- `queries/`: pruebas de logica, validacion de hipotesis y reglas prescriptivas no consolidadas.
- `views/`: logica reutilizable, versionada y apta para Power BI.
- `views/diagnostic/`: diagnostico, calidad y narrativa; no forman el nucleo estrella.
- `CSV/`: foto fija exportada; no sustituye la logica SQL original.

## Convenciones

Prefijos:

```text
q_desc_... = consulta descriptiva
q_diag_... = consulta diagnostica
vw_dim_... = dimension semantica
vw_fact_... = hecho granular
vw_bridge_... = puente relacional
vw_ref_... = referencia normalizada
vw_diag_... = diagnostico auxiliar
```

Las reglas prescriptivas pueden vivir temporalmente en `queries/` hasta que sean estables.

Estado prescriptivo actual:

- La primera clasificacion comercial se esta validando en Power BI mediante columnas DAX sobre `vw_diag_competitive_staple_candidates`.
- Columnas: `clasificacion_comercial` y `motivo_clasificacion`.
- No existe aun una view SQL estable para esa clasificacion.
- Solo debe crearse una nueva `vw_*` cuando las reglas queden validadas como reutilizables.

## Views actuales

```text
views/dim/vw_dim_card.sql
views/dim/vw_dim_card_image.sql
views/dim/vw_dim_card_typelines.sql
views/dim/vw_dim_set.sql
views/dim/vw_dim_rarity.sql
views/bridge/vw_bridge_card_set.sql
views/bridge/vw_bridge_card_banlist.sql
views/fact/vw_fact_card_prices.sql
views/fact/vw_fact_price_history.sql
views/ref/vw_ref_banlist_status.sql
views/diagnostic/vw_diag_competitive_staple_candidates.sql
views/diagnostic/vw_diag_high_demand_archetypes.sql
views/diagnostic/vw_diag_price_by_rarity.sql
views/diagnostic/vw_diag_price_outliers.sql
```

## Queries actuales

```text
queries/card_comercial_actions.sql
queries/descriptive/q_desc_card_avg_marketplace_price.sql
queries/descriptive/q_desc_cards_by_set_count.sql
queries/descriptive/q_desc_price_distribution_by_marketplace.sql
queries/descriptive/q_desc_price_history_snapshots.sql
queries/diagnostic/q_diag_card_rarity_printings.sql
queries/diagnostic/q_diag_price_variation_usd.sql
queries/diagnostic/q_diag_relevant_price_increases.sql
```

`queries/card_comercial_actions.sql` pertenece al bloque prescriptivo: convierte criterios analiticos en clasificaciones comerciales. Si se reutiliza en Power BI, debe consolidarse como view.

Nota:

La pagina prescriptiva actual no depende todavia de `queries/card_comercial_actions.sql`. Usa reglas DAX experimentales en Power BI para validar la clasificacion antes de moverla a SQL.

## Dependencias base

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
```

## Utilidad auxiliar desde CSV

`src.csv_sql_scripts` puede generar scripts SQL desde CSV locales:

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```

Genera archivos en `sql/generated/from_csv/`. Es recuperacion auxiliar, no flujo analitico principal.
