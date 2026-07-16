# 01 — Descriptive

[Inicio](../../../../README.md) → [Diseño de views](../README.md) → Descriptive

## Propósito

Responder qué existe, cuánto existe y cómo se distribuye, sin explicar causas ni emitir recomendaciones. Este módulo publica las dimensiones conformadas y los hechos base que consumirán los módulos posteriores.

## Preguntas guía

### Vista general

- ¿Qué volumen de cartas, sets, rarezas válidas y marketplaces contiene el modelo, y qué monedas/snapshots condicionan su lectura?

Los tipos, atributos, arquetipos, cobertura raw y número de impresiones son desgloses de esta pregunta; no requieren preguntas ni views independientes.

### Análisis descriptive

- ¿Qué cartas tienen mayor precio vigente por marketplace?
- ¿Qué sets concentran mayor valor de impresión mediante `set_price_usd`?

Moneda, último snapshot y cobertura se tratan como condiciones obligatorias de lectura, no como análisis separados.

## Backlog de views base

### `vw_dim_cards`

- Estado: propuesta.
- Pregunta: ¿qué atributos describen una carta única?
- Fuente: `cards`.
- Grano: una carta.
- Clave: `card_id`.
- Riesgo: usar nombres como relación en lugar de `card_id`.
- Aceptación: `COUNT(*) = COUNT(DISTINCT card_id)`.

### `vw_dim_sets`

- Estado: propuesta.
- Fuente: `sets`.
- Grano: un set.
- Clave: `set_id`.
- Aceptación: nombre no vacío y `set_id` único.

### `vw_dim_rarities`

- Estado: propuesta.
- Fuente: `rarity_types`.
- Grano: tipo de rareza + código normalizado.
- Clave: `rarity_id`.
- Filtro: solo catálogo normalizado; no incorporar etiquetas internas raw.
- Riesgo: interpretar `rarity_id` como impresión.

### `vw_dim_marketplaces`

- Estado: propuesta.
- Fuente: `marketplaces`.
- Grano: un marketplace.
- Clave: `marketplace_id`.

### `vw_dim_currencies`

- Estado: propuesta.
- Fuente: `currencies`.
- Grano: una moneda.
- Clave: `currency_code`.

### `vw_fact_card_printings`

- Estado: propuesta.
- Pregunta: ¿en qué set y rareza existe cada impresión?
- Fuentes: `card_printings` y sus FK.
- Grano: una impresión.
- Clave: `printing_id`.
- FK: `card_id`, `set_id`, `rarity_id` nullable por calidad.
- Medida física: `set_price_usd`.
- Riesgo: sumar precios y confundir volumen con valor.

### `vw_fact_card_prices_current`

- Estado: propuesta; requiere acordar la regla de “último snapshot”.
- Pregunta: ¿cuál es la observación más reciente por carta, marketplace y moneda?
- Fuente: `card_price_history`.
- Grano: carta + marketplace + moneda.
- Clave: `card_id + marketplace_id + currency_code`.
- Riesgo: usar un máximo global de fecha cuando una serie no tenga ese snapshot.
- Aceptación: seleccionar el máximo `snapshot_at` dentro de cada serie.

## Medidas que no justifican otra view

- Conteo de cartas, sets e impresiones.
- Precio medio, mediana, mínimo y máximo.
- Participación porcentual por categoría.
- Rankings Top N.

Estas medidas deben calcularse en Power BI sobre los hechos base.
