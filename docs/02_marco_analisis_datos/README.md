# Marco de analisis de datos

Este documento fija las premisas del punto base.

## Fuente

La fuente externa es la API publica de YGOPRODeck.

La fuente interna es MySQL:

```text
yugioh_db
```

## Punto de partida

El analisis empieza desde las tablas madre definidas en:

```text
sql/main_schema.sql
```

No hay resultados analiticos consolidados.

## Premisas

- Mantener `cards.card_id` como identificador estable de carta.
- Separar carta, set, rareza, imagen, precio, historico, banlist y listas multivalor.
- No mezclar monedas sin conversion o segmentacion.
- Tratar `set_price` como dato de aparicion de carta en set.
- No interpretar `set_price` como precio propio de una rareza.
- Conservar trazabilidad hacia el JSON de origen.

## Estado

```text
punto base sin resultados analiticos consolidados
```
