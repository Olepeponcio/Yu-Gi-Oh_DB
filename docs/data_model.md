# Modelo de datos

## Objetivo

Representar la informacion de cartas de YGOPRODeck en tablas relacionales normalizadas.

## Tabla principal

### `cards`

Contiene una fila por carta.

Campos clave:

- `id`: identificador de carta.
- `name`: nombre.
- `card_type`: tipo general.
- `frame_type`: marco logico/visual.
- `description`: descripcion.
- `atk`, `def`, `attribute`, `level`: campos de monstruos.
- `scale`, `pendulum_description`, `monster_description`: campos Pendulum.
- `link_value`: valor Link.

## Tablas hijas

### `card_sets`

Apariciones de cartas en productos o sets.

Relacion:

```text
cards.id -> card_sets.card_id
```

### `card_images`

Imagenes asociadas a una carta.

Relacion:

```text
cards.id -> card_images.card_id
```

### `card_prices`

Precios por marketplace.

Relacion 1:1:

```text
cards.id -> card_prices.card_id
```

### `card_banlist`

Restricciones por formato.

Relacion 1:1 opcional:

```text
cards.id -> card_banlist.card_id
```

### `card_typelines`

Lista normalizada de elementos de `typeline`.

Relacion:

```text
cards.id -> card_typelines.card_id
```

### `card_linkmarkers`

Lista normalizada de marcadores Link.

Relacion:

```text
cards.id -> card_linkmarkers.card_id
```

## Criterio de carga

- `cards`, `card_images`, `card_prices` y `card_banlist` se cargan de forma idempotente.
- `card_sets`, `card_typelines` y `card_linkmarkers` se refrescan por carta para evitar acumulacion de datos obsoletos.
- Las claves foraneas usan `ON DELETE CASCADE`.
