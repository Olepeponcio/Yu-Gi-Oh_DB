# Objetivo analitico del proyecto

## Contexto

La practica simula una empresa contratada por Konami para analizar el mercado de cartas coleccionables de Yu-Gi-Oh.

La finalidad de negocio es apoyar decisiones sobre venta de cartas, packs y sobres. El analisis debe ayudar a entender que factores pueden impulsar el interes del publico objetivo, el ticket medio, la diversificacion de compra.

## Premisa de negocio

Las cartas pueden tener valor por varios motivos:

- rareza,
- utilidad competitiva,
- pertenencia a decks o arquetipos populares,
- precio actual,
- evolucion historica del precio,
- aparicion en sets concretos,
- atractivo coleccionista.

El objetivo no es solo listar cartas, sino preparar una base que permita analizar combinaciones utiles para construir productos comerciales.

## Preguntas de analisis:

- Que rarezas elevan mas el precio medio?
- Que cartas son staples competitivas?
- Que cartas pertenecen a arquetipos con alta demanda?
- Que sets concentran mas valor?
- Que combinacion de cartas favorece venta cruzada?
- Que cartas baratas pueden acompanar cartas chase en un pack?
- Que cartas generan interes coleccionista aunque no sean competitivas?
- Que cartas muestran crecimiento de precio entre ejecuciones del ETL?
- Que marketplace muestra mayor variacion de precio?
- Que rarezas aparecen mas asociadas a cartas de precio alto?

## Modelo necesario

La base debe separar almacenamiento y analisis:

```text
API / Python ETL
-> tablas base normalizadas
-> dimensiones de mercado
-> historico de precios
-> vistas SQL analiticas
-> Power BI
```

## Tablas base

Mantienen la informacion estructural de la API:

- `cards`
- `card_sets`
- `card_images`
- `card_prices`
- `card_banlist`
- `card_typelines`
- `card_linkmarkers`

## Dimensiones de mercado

Permiten analizar productos y valor percibido:

- `sets`: catalogo unico de sets.
- `rarities`: catalogo de rarezas por codigo de impresion.

`card_sets` conserva los textos originales y anade referencias a estas dimensiones mediante `set_id` y `rarity_id`.

## Historico de precios

`card_price_history` guarda una foto de precios por carta en cada ejecucion real del ETL.

Esto permite analizar:

- evolucion de precio,
- tendencia,
- volatilidad,
- comparacion entre marketplaces,
- deteccion de cartas al alza.

## Capa analitica

Las vistas se crearan desde MySQL y se guardaran como scripts SQL en el proyecto:

```text
sql/analysis/views/
```

Ejemplos futuros:

- `vw_card_market_value`
- `vw_rarity_price_distribution`
- `vw_set_value_analysis`
- `vw_competitive_cards`
- `vw_archetype_demand`
- `vw_pack_candidate_cards`

Power BI consumira preferentemente esas vistas.

## Estado

Este README define el marco analitico inicial. Se actualizara en la etapa de analisis cuando se definan metricas, vistas y dashboards concretos.
