# Modelo de datos

## Objetivo

Representar la informacion de YGOPRODeck en tablas relacionales normalizadas. El esquema ejecutable vive en `sql/schema.sql`.

## Tabla principal

### `cards`

Una fila por carta.

Clave:

```text
card_id
```

## Catalogos y tablas hijas

### `sets`

Catalogo de sets.

Relacion:

```text
sets.id -> card_sets.set_id
```

### `rarities`

Catalogo de rarezas por codigo de impresion.

Relacion:

```text
rarities.id -> card_sets.rarity_id
```

### `card_sets`

Apariciones de cartas en sets.

Grano:

```text
1 fila = 1 carta + 1 set/codigo + 1 rareza
```

Relaciones:

```text
cards.card_id -> card_sets.card_id
sets.id -> card_sets.set_id
rarities.id -> card_sets.rarity_id
```

Regla:

```text
set_price pertenece a card_sets.
```

### `card_images`

Imagenes asociadas a cartas.

```text
cards.card_id -> card_images.card_id
```

### `card_prices`

Precios actuales por carta y marketplace.

```text
cards.card_id -> card_prices.card_id
```

Regla de moneda:

```text
cardmarket_price   -> EUR
tcgplayer_price    -> USD
ebay_price         -> USD
amazon_price       -> USD
coolstuffinc_price -> USD
```

Aviso: cualquier consulta de consumo debe conservar o declarar la moneda. Si se comparan marketplaces, primero debe convertirse moneda o segmentarse el resultado.

### `card_price_history`

Snapshots de precios por ejecucion del ETL.

```text
cards.card_id -> card_price_history.card_id
```

Aplica la misma regla de moneda que en `card_prices`.

### `card_banlist`

Estado de banlist por carta.

```text
cards.card_id -> card_banlist.card_id
```

### `card_typelines`

Elementos de typeline por carta.

```text
cards.card_id -> card_typelines.card_id
```

### `card_linkmarkers`

Marcadores Link por carta.

```text
cards.card_id -> card_linkmarkers.card_id
```

## Criterio de carga

- `cards`, `card_images`, `card_prices` y `card_banlist`: insercion/actualizacion.
- `sets` y `rarities`: catalogos reutilizables.
- `card_price_history`: inserta snapshot por ejecucion real.
- `card_sets`, `card_typelines` y `card_linkmarkers`: se refrescan por carta.
