# Modelo de datos

## Objetivo

Representar la informacion de cartas de YGOPRODeck en tablas relacionales normalizadas.

## Tipo de modelo

El esquema actual de `yugioh_db` es un modelo relacional normalizado. No es un modelo dimensional en estrella puro.

Clasificacion:

```text
MySQL / yugioh_db = fuente unica relacional
SQL queries = analisis, diagnostico y validacion de reglas
Power BI = modelo semantico, relaciones, medidas y narrativa
```

Decision de arquitectura:

> Mantener MySQL como modelo relacional base y construir el modelo semantico al conectar desde Power BI.

Motivo:

- `cards` funciona como tabla principal de entidad.
- `card_images`, `card_prices`, `card_banlist`, `card_typelines` y `card_linkmarkers` son tablas hijas normalizadas.
- `sets` y `rarities` funcionan como catalogos reutilizables.
- `card_sets` representa apariciones de cartas en sets y conserva `set_price`.
- `card_price_history` almacena mediciones de precios por carta y fecha de snapshot.

## Modelo semantico futuro

Power BI debe construir dimensiones, hechos, relaciones y medidas desde tablas base.

Dimensiones candidatas:

- `DimCard`: desde `cards`.
- `DimSet`: desde `sets`.
- `DimRarity`: desde `rarities`.
- `DimMarketplace`: derivada en Power BI desde columnas de precio.
- `DimBanlistFormat`: TCG, OCG y GOAT.
- `Calendario`: tabla calculada en Power BI desde `card_price_history.snapshot_at`.
- `DimArchetype`: derivada de `cards.archetype` si el analisis lo requiere.
- `DimCardType`: derivada de `cards.card_type` si el analisis lo requiere.

Hechos candidatos:

- `FactCardSetPrintings`: desde `card_sets`.
- `FactCardPricesCurrent`: desde `card_prices`, despivotando marketplaces.
- `FactCardPricesHistory`: desde `card_price_history`, despivotando marketplaces.
- `FactCardBanlistStatus`: desde `card_banlist`, despivotando formatos.
- `FactCardTypelines`: desde `card_typelines` si se analiza tipologia multivalor.

Estas tablas semanticas no viven como objetos SQL oficiales. Se construyen en Power BI o mediante queries exploratorias mientras se valida el modelo.

## Tabla principal

### `cards`

Contiene una fila por carta.

Campos clave:

- `card_id`: identificador de carta recibido desde YGOPRODeck.
- `name`: nombre.
- `card_type`: tipo general.
- `human_readable_card_type`: tipo legible.
- `frame_type`: marco logico/visual.
- `description`: descripcion.
- `race`, `archetype`, `attribute`: atributos clasificatorios.
- `atk`, `def`, `level`, `scale`, `link_value`: campos de juego cuando aplican.

## Tablas hijas y catalogos

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

Regla:

La rareza no contiene precio. El precio asociado a set vive en `card_sets.set_price`.

### `card_sets`

Apariciones de cartas en productos o sets.

Relacion:

```text
cards.card_id -> card_sets.card_id
sets.id -> card_sets.set_id
rarities.id -> card_sets.rarity_id
```

Grano:

```text
1 fila = 1 carta + 1 set/codigo + 1 rareza
```

Regla:

`set_price` es precio observado en la aparicion de una carta dentro de un set. No es precio intrinseco de la rareza.

### `card_images`

Imagenes asociadas a una carta.

Relacion:

```text
cards.card_id -> card_images.card_id
```

### `card_prices`

Precios actuales por marketplace.

Relacion:

```text
cards.card_id -> card_prices.card_id
```

Regla:

No mezclar EUR y USD sin conversion o segmentacion visible.

### `card_price_history`

Historico de precios por ejecucion del ETL.

Relacion:

```text
cards.card_id -> card_price_history.card_id
```

Grano semantico esperado en Power BI:

```text
1 carta + 1 snapshot + 1 marketplace
```

### `card_banlist`

Restricciones por formato.

Relacion:

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
- `sets` y `rarities` se cargan de forma idempotente como catalogos.
- `card_price_history` inserta una foto de precios por ejecucion del ETL.
- `card_sets`, `card_typelines` y `card_linkmarkers` se refrescan por carta para evitar acumulacion de datos obsoletos.
- Las claves foraneas hacia `cards` usan `ON DELETE CASCADE`.
- Las dimensiones `sets` y `rarities` usan `ON DELETE SET NULL` desde `card_sets`.
