# SQL de analisis

Directorio de implementacion SQL para responder al marco canonico:

```text
docs/02_marco_analisis_datos/README.md
```

Este README documenta la organizacion de consultas SQL sobre la fuente unica MySQL.

## Estado actual

La capa SQL intermedia queda retirada del proyecto.

La fuente unica de verdad son las tablas madre creadas por:

```text
sql/main_schema.sql
```

Las consultas de `sql/analysis/queries/` sirven para explorar, diagnosticar y validar reglas antes de trasladarlas a Power BI como medidas, columnas calculadas o decisiones de modelo.

## Estructura

```text
queries/              -> consultas exploratorias y reglas en validacion
queries/descriptive/  -> analisis descriptivo
queries/diagnostic/   -> analisis diagnostico y control de calidad
CSV/                  -> snapshots locales auxiliares si se necesitan
```

No existe ya una capa SQL intermedia oficial. Si aparece una necesidad recurrente, primero debe formularse como query y despues decidir si pertenece a Power BI, al ETL o al esquema relacional.

## Criterio de uso

```text
tabla madre -> query exploratoria -> validacion -> medida/modelo Power BI o cambio ETL
```

- `queries/`: pruebas de logica, validacion de hipotesis y reglas no consolidadas.
- `queries/descriptive/`: consultas para entender catalogo, precios, sets y cobertura.
- `queries/diagnostic/`: consultas para explicar riesgos, outliers, variacion y calidad.
- `CSV/`: foto fija exportada; no sustituye MySQL.

## Convenciones

Prefijos:

```text
q_desc_... = consulta descriptiva
q_diag_... = consulta diagnostica
```

Regla:

```text
Toda query debe declarar claramente su grano y no crear una fuente paralela.
```

Ejemplos de grano:

```text
1 fila = 1 carta
1 fila = 1 carta + marketplace
1 fila = 1 carta + set + rareza
1 fila = 1 carta + snapshot + marketplace
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

`queries/card_comercial_actions.sql` pertenece al bloque prescriptivo. Convierte criterios analiticos en clasificaciones comerciales, pero no debe materializarse como tabla estable sin validar su utilidad.

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
card_linkmarkers
```

## Regla sobre precios

`set_price` pertenece al grano de `card_sets`: una aparicion de carta en un set con una rareza.

No debe interpretarse como precio intrinseco de una rareza.

Los precios actuales e historicos por marketplace viven en:

```text
card_prices
card_price_history
```
