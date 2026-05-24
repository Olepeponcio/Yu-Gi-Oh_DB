# Modelo de datos

## Objetivo

Representar la informacion de cartas de YGOPRODeck en tablas relacionales normalizadas.

## Tipo de modelo

El esquema actual de `yugioh_db` no es un modelo dimensional en estrella puro.

Es un modelo relacional normalizado orientado a conservar datos limpios, consistentes y reutilizables desde MySQL. Su finalidad principal es servir como capa persistente del proyecto despues del ETL.

Clasificacion:

```text
MySQL / yugioh_db = modelo relacional normalizado
Power BI = capa analitica y modelo dimensional
```

Motivo:

- `cards` funciona como tabla principal de entidad, no como tabla de hechos.
- `card_images`, `card_prices`, `card_banlist`, `card_typelines` y `card_linkmarkers` son tablas hijas normalizadas.
- `sets` y `rarities` funcionan como catalogos o dimensiones reutilizables.
- `card_sets` actua como tabla de relacion entre cartas, sets y rarezas.
- `card_price_history` es la tabla mas cercana a una tabla de hechos, porque almacena mediciones de precios por carta y fecha de snapshot.

Decision de arquitectura:

> Mantener MySQL como modelo relacional base y construir el modelo dimensional en Power BI.

Esta decision evita forzar el diseno de MySQL hacia estrella antes de tener claras las preguntas analiticas definitivas. Power BI podra crear dimensiones, hechos, relaciones y medidas a partir de las tablas o views de MySQL.

Modelo dimensional inicial sugerido para Power BI:

```text
FactPrices
  -> DimCard
  -> DimDate

FactCardSets
  -> DimCard
  -> DimSet
  -> DimRarity
```

Posibles dimensiones derivadas:

- `DimCard`: desde `cards`.
- `DimSet`: desde `sets`.
- `DimRarity`: desde `rarities`.
- `DimDate`: generada en Power BI desde `snapshot_at`.
- `DimArchetype`: derivada de `cards.archetype` si el analisis lo requiere.
- `DimCardType`: derivada de `cards.card_type` si el analisis lo requiere.

Evolucion esperada:

- Primero, mantener el modelo relacional de MySQL estable.
- Despues, construir el modelo dimensional en Power BI segun las preguntas de negocio.
- Si el modelo dimensional se consolida, crear views SQL especificas para alimentar Power BI con menos transformacion manual.

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
