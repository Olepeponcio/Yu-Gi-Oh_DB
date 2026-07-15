# Modelo de datos — tablas madre

Estado: punto de partida anterior al diseño de views.

## Principios

- Una tabla, una granularidad y una única verdad.
- PK y FK físicas antes del modelo semántico.
- Precio general de carta separado de precio de impresión.
- Moneda, marketplace y snapshot declarados en cada precio.
- Valor raw de rareza preservado; solo valores válidos entran en `rarity_types`.
- Ningún hecho se relaciona con otro hecho.

## Relaciones

```text
cards 1 -> * card_printings * <- 1 sets
rarity_types 1 -> * card_printings

cards 1 -> * card_price_history
marketplaces 1 -> * card_price_history
currencies 1 -> * card_price_history

cards 1 -> * card_images/card_typelines/card_linkmarkers
cards 1 -> 0..1 card_banlist
```

## Granularidades

`card_printings`: carta + `set_code` + rareza raw + código raw. Contiene `set_price_usd`, la única medida actualmente atribuible a rareza/set.

`card_price_history`: una carta + marketplace + moneda + snapshot. No contiene `rarity_id` porque la API no entrega ese precio al nivel de impresión.

## Siguiente hito

Validar el raw y las tablas cargadas. Después se abrirá el registro de views, declarando para cada una pregunta, grano, claves y uso en Power BI.
