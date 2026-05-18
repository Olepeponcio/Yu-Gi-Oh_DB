# Analisis JSON API YGOPRODeck

Fecha de analisis: 2026-05-18.

Fuente oficial: https://ygoprodeck.com/api-guide/

Endpoint base:

```text
https://db.ygoprodeck.com/api/v7/cardinfo.php
```

## Objetivo del microbloque

Entender la forma real del JSON antes de crear tablas SQL.

El objetivo no es disenar aun el esquema definitivo, sino detectar:

- campos principales,
- campos opcionales,
- listas anidadas,
- entidades candidatas,
- riesgos de normalizacion.

## Muestras revisadas

Se revisaron dos muestras:

1. Una muestra paginada pequena:

```text
https://db.ygoprodeck.com/api/v7/cardinfo.php?num=12&offset=0
```

2. Una muestra controlada por nombres para cubrir tipos variados:

```text
Dark Magician
Blue-Eyes White Dragon
Ash Blossom & Joyous Spring
Odd-Eyes Pendulum Dragon
Number 39: Utopia
Decode Talker
Raigeki
Mirror Force
```

## Forma general

La respuesta devuelve un objeto raiz con una lista `data`.

```text
{
  "data": [
    { carta_1 },
    { carta_2 }
  ]
}
```

Cada carta es un objeto principal. Algunas claves aparecen siempre y otras dependen del tipo de carta.

## Campos principales detectados

Campos comunes o muy frecuentes:

- `id`: identificador numerico de la carta.
- `name`: nombre.
- `type`: tipo general de carta.
- `humanReadableCardType`: tipo legible.
- `frameType`: marco visual/logico.
- `desc`: descripcion.
- `race`: raza del monstruo o subtipo de Spell/Trap.
- `archetype`: arquetipo, si aplica.
- `ygoprodeck_url`: URL publica de YGOPRODeck.

Campos propios de monstruos:

- `atk`
- `def`
- `attribute`
- `level`
- `typeline`

Campos especificos detectados:

- `scale`: cartas Pendulum.
- `pend_desc`: descripcion Pendulum.
- `monster_desc`: descripcion de monstruo en cartas Pendulum.
- `linkval`: cartas Link.
- `linkmarkers`: marcadores Link.

## Listas y objetos anidados

### `card_sets`

Lista de apariciones de una carta en productos/sets.

Campos detectados:

- `set_name`
- `set_code`
- `set_rarity`
- `set_rarity_code`
- `set_price`

Observacion: una carta puede aparecer varias veces en sets distintos o incluso en el mismo set con rarezas distintas.

### `card_images`

Lista de imagenes asociadas a una carta.

Campos detectados:

- `id`
- `image_url`
- `image_url_small`
- `image_url_cropped`

Observacion: puede haber mas de una imagen por carta si existen artes alternativas.

### `card_prices`

Lista de precios por marketplace.

Campos detectados:

- `cardmarket_price`
- `tcgplayer_price`
- `ebay_price`
- `amazon_price`
- `coolstuffinc_price`

Observacion: los precios llegan como texto. Conviene convertirlos a tipo decimal durante la carga.

### `banlist_info`

Objeto opcional con restricciones por formato.

Campos detectados en muestra:

- `ban_tcg`
- `ban_ocg`
- `ban_goat`

Observacion: no aparece en todas las cartas y sus claves varian segun formatos disponibles.

## Campos opcionales relevantes

No todas las cartas tienen los mismos campos.

Ejemplos:

- Spell/Trap no tienen `atk`, `def`, `attribute`, `level` ni `typeline`.
- Link Monster puede tener `def` como `null`, `level` como `0`, y usa `linkval` / `linkmarkers`.
- Pendulum separa texto en `pend_desc` y `monster_desc`, ademas de `desc`.
- Xyz aparece con clave `level` en la respuesta de la API, aunque conceptualmente sea Rank.
- `archetype` no es obligatorio.
- `banlist_info` no es obligatorio.
- `card_sets` puede faltar en cartas sin impresiones detectadas en la muestra.

## Entidades candidatas para SQL

Todavia no es el esquema final, pero el JSON sugiere separar:

- `cards`: datos base de cada carta.
- `card_sets`: apariciones de cartas en sets.
- `card_images`: imagenes y artes alternativas.
- `card_prices`: precios por carta.
- `banlist_info`: restricciones por formato.
- `card_typelines`: lista normalizada de elementos de `typeline`.
- `card_linkmarkers`: lista normalizada de marcadores Link.
