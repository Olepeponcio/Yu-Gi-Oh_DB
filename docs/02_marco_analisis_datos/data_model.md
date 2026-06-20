# Modelo de datos

## Objetivo

Representar la informacion de cartas de YGOPRODeck en tablas relacionales normalizadas.

## Tipo de modelo

El esquema actual de `yugioh_db` no es un modelo dimensional en estrella puro.

Es un modelo relacional normalizado orientado a conservar datos limpios, consistentes y reutilizables desde MySQL. Su finalidad principal es servir como capa persistente del proyecto despues del ETL.

Clasificacion:

```text
MySQL / yugioh_db = modelo relacional normalizado
Views MySQL = capa semantica y diagnostica
Power BI = visualizacion, relaciones, medidas y narrativa
```

Motivo:

- `cards` funciona como tabla principal de entidad, no como tabla de hechos.
- `card_images`, `card_prices`, `card_banlist`, `card_typelines` y `card_linkmarkers` son tablas hijas normalizadas.
- `sets` y `rarities` funcionan como catalogos o dimensiones reutilizables.
- `card_sets` actua como tabla de relacion entre cartas, sets y rarezas.
- `card_price_history` es la tabla mas cercana a una tabla de hechos, porque almacena mediciones de precios por carta y fecha de snapshot.

Decision de arquitectura:

> Mantener MySQL como modelo relacional base y exponer una capa de views para Power BI.

Esta decision evita forzar el diseno de MySQL hacia estrella. Las preguntas analiticas se mantienen en `docs/02_marco_analisis_datos/README.md`.

Modelo semantico actual:

```text
vw_dim_card
vw_dim_set
vw_dim_rarity
vw_ref_banlist_status

vw_bridge_card_set
vw_bridge_card_banlist
vw_fact_card_prices
vw_fact_price_history
```

Posibles dimensiones derivadas:

- `DimCard`: desde `cards`.
- `DimSet`: desde `sets`.
- `DimRarity`: desde `rarities`.
- `Calendario`: tabla calculada en Power BI y marcada como tabla de fechas.
- `DimArchetype`: derivada de `cards.archetype` si el analisis lo requiere.
- `DimCardType`: derivada de `cards.card_type` si el analisis lo requiere.

Evolucion esperada:

- Mantener el modelo relacional de MySQL estable.
- Crear views `vw_dim_*`, `vw_fact_*`, `vw_bridge_*`, `vw_ref_*` y `vw_diag_*` sobre las tablas base.
- Construir relaciones y medidas en Power BI sobre esas views.

## Capa semantica en MySQL

La capa semantica se expone desde MySQL. Las tablas base son la capa persistente del ETL; las views son la capa de consumo analitico.

Criba:

```text
cards, sets, rarities, card_sets, card_prices, card_price_history, card_banlist
    -> tablas base MySQL

vw_dim_*, vw_fact_*, vw_bridge_*, vw_ref_*
    -> modelo semantico consumido por Power BI

vw_desc_*
    -> views descriptivas auxiliares

vw_ref_*
    -> catalogos de referencia normalizados

views/diagnostic/vw_diag_*
    -> views de diagnostico, fuera del modelo relacional
```

Relaciones objetivo:

```text
vw_dim_card[card_id] 1 -> * vw_bridge_card_set[card_id]
vw_dim_set[set_id] 1 -> * vw_bridge_card_set[set_id]
vw_dim_rarity[rarity_id] 1 -> * vw_bridge_card_set[rarity_id]
vw_dim_card[card_id] 1 -> * vw_bridge_card_banlist[card_id]
vw_ref_banlist_status[banlist_status_key] 1 -> * vw_bridge_card_banlist[banlist_status_key]
vw_dim_card[card_id] 1 -> * vw_fact_card_prices[card_id]
vw_dim_card[card_id] 1 -> * vw_fact_price_history[card_id]
Calendario[Date] 1 -> * vw_fact_price_history[snapshot_date]
```

Direccion de filtro: de dimension a hecho.

SQL localizado para apoyar el modelo:

```text
sql/analysis/views/dim/vw_dim_card.sql
sql/analysis/views/dim/vw_dim_set.sql
sql/analysis/views/dim/vw_dim_rarity.sql
sql/analysis/views/bridge/vw_bridge_card_set.sql
sql/analysis/views/bridge/vw_bridge_card_banlist.sql
sql/analysis/views/fact/vw_fact_card_prices.sql
sql/analysis/views/fact/vw_fact_price_history.sql
sql/analysis/views/ref/vw_ref_banlist_status.sql
sql/analysis/views/diagnostic/vw_diag_competitive_staple_candidates.sql
sql/analysis/views/diagnostic/vw_diag_high_demand_archetypes.sql
sql/analysis/views/diagnostic/vw_diag_price_by_rarity.sql
sql/analysis/views/diagnostic/vw_diag_price_outliers.sql
```

`vw_fact_card_prices.sql` funciona como hecho de precios por marketplace. Las `views/diagnostic/vw_diag_*` son agregados o filtros diagnosticos, no el nucleo del esquema estrella.

## Tabla principal

### `cards`

Contiene una fila por carta.

Campos clave:

- `card_id`: identificador de carta recibido desde YGOPRODeck.
- `name`: nombre.
- `card_type`: tipo general.
- `frame_type`: marco logico/visual.
- `description`: descripcion.
- `atk`, `def`, `attribute`, `level`: campos de monstruos.
- `scale`, `pendulum_description`, `monster_description`: campos Pendulum.
- `link_value`: valor Link.

## Tablas hijas

### `sets`

Catalogo unico de sets detectados desde `card_sets`.

Relacion:

```text
sets.id -> card_sets.set_id
```

### `rarities`

Catalogo de rarezas por codigo de impresion detectadas desde `card_sets`.

Relacion:

```text
rarities.id -> card_sets.rarity_id
rarities.set_code -> card_sets.set_code
```

### `card_sets`

Apariciones de cartas en productos o sets.

Relacion:

```text
cards.card_id -> card_sets.card_id
sets.id -> card_sets.set_id
rarities.id -> card_sets.rarity_id
```

### `card_images`

Imagenes asociadas a una carta.

Relacion:

```text
cards.card_id -> card_images.card_id
```

### `card_prices`

Precios por marketplace.

Relacion 1:1:

```text
cards.card_id -> card_prices.card_id
```

### `card_price_history`

Historico de precios por ejecucion del ETL.

Relacion:

```text
cards.card_id -> card_price_history.card_id
```

### `card_banlist`

Restricciones por formato.

Relacion 1:1 opcional:

```text
cards.card_id -> card_banlist.card_id
```

### `card_typelines`

Lista normalizada de elementos de `typeline`.

Relacion:

```text
cards.card_id -> card_typelines.card_id
```

### `card_linkmarkers`

Lista normalizada de marcadores Link.

Relacion:

```text
cards.card_id -> card_linkmarkers.card_id
```

## Criterio de carga

- `cards`, `card_images`, `card_prices` y `card_banlist` se cargan de forma idempotente.
- `sets` y `rarities` se cargan de forma idempotente como dimensiones.
- `card_price_history` inserta una foto de precios por ejecucion del ETL.
- `card_sets`, `card_typelines` y `card_linkmarkers` se refrescan por carta para evitar acumulacion de datos obsoletos.
- Las claves foraneas hacia `cards` usan `ON DELETE CASCADE`.
- Las dimensiones `sets` y `rarities` usan `ON DELETE SET NULL` desde `card_sets`.
