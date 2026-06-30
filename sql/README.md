# SQL de analisis

Este directorio contiene las vistas `vw_` que se cargan en Power BI a partir de las tablas madre de `sql/schema.sql`.

## Estructura

```text
sql/views/   -> vistas del modelo relacional simplificado para Power BI
```

Plantillas de creacion/reemplazo:

```text
sql/create_or_replace_views.sql           -> consola mysql, usa SOURCE
sql/create_or_replace_views_workbench.sql -> hoja SQL / MySQL Workbench
```

## Uso

Consola `mysql`:

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/create_or_replace_views.sql;
```

MySQL Workbench:

```text
abrir y ejecutar sql/create_or_replace_views_workbench.sql
```

## Vistas del modelo Power BI

| Vista | Tipo | Grano | Uso |
|---|---|---|---|
| `vw_dim_cards_descriptive` | Dimension | 1 carta | Catalogo base y filtros de carta |
| `vw_dim_sets_descriptive` | Dimension | 1 set | Catalogo de sets |
| `vw_dim_rarities_descriptive` | Dimension | 1 rareza catalogada | Catalogo tecnico de rarezas |
| `vw_dim_marketplaces_descriptive` | Dimension | 1 marketplace | Fuente de precio |
| `vw_dim_currencies_descriptive` | Dimension | 1 moneda | Segmentacion EUR/USD |
| `vw_dim_snapshots_descriptive` | Dimension temporal | 1 snapshot | Fecha de captura historica |
| `vw_fact_card_prices_descriptive` | Hecho | 1 carta + 1 marketplace + 1 moneda | Precio actual en formato largo |
| `vw_fact_card_set_appearances` | Hecho puente | 1 carta + 1 set + 1 rareza | Apariciones, reimpresiones y precio de set |
| `vw_fact_card_price_variation_predictive` | Hecho historico | 1 carta + 1 marketplace + 1 moneda + 1 snapshot | Variacion entre snapshots |

## Relaciones recomendadas

```text
vw_dim_cards_descriptive[card_id]
    1 -> * vw_fact_card_prices_descriptive[card_id]
    1 -> * vw_fact_card_set_appearances[card_id]
    1 -> * vw_fact_card_price_variation_predictive[card_id]

vw_dim_sets_descriptive[set_id]
    1 -> * vw_fact_card_set_appearances[set_id]

vw_dim_rarities_descriptive[rarity_id]
    1 -> * vw_fact_card_set_appearances[rarity_id]

vw_dim_marketplaces_descriptive[marketplace]
    1 -> * vw_fact_card_prices_descriptive[marketplace]
    1 -> * vw_fact_card_price_variation_predictive[marketplace]

vw_dim_currencies_descriptive[currency]
    1 -> * vw_fact_card_prices_descriptive[currency]
    1 -> * vw_fact_card_price_variation_predictive[currency]

vw_dim_snapshots_descriptive[snapshot_at]
    1 -> * vw_fact_card_price_variation_predictive[snapshot_at]
```

## Reglas de diseno

- Declarar el grano de cada vista antes de crearla.
- No mezclar EUR y USD en una metrica sin conversion explicita.
- Usar `UNION ALL` para transformar precios de columnas a formato largo.
- Las preguntas de ranking, revision y resumen se resuelven desde hechos base en Power BI.
- No relacionar hechos entre si en Power BI salvo necesidad justificada.
- Cada nueva view usada en Power BI debe anadirse a `sql/create_or_replace_views.sql` y `sql/create_or_replace_views_workbench.sql`.

## Preguntas cubiertas

```text
catalogo de cartas       -> vw_dim_cards_descriptive
precios actuales         -> vw_fact_card_prices_descriptive
apariciones sets/rarezas -> vw_fact_card_set_appearances
relacion rareza-precio   -> vw_fact_card_set_appearances + vw_dim_rarities_descriptive
historico de precios     -> vw_fact_card_price_variation_predictive + vw_dim_snapshots_descriptive
```
