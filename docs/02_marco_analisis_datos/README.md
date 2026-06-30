# Diario de analisis de datos

Este README registra el proceso de analisis desde la base relacional cargada por Python hasta las consultas futuras de consumo.

Fuente interna:

```text
yugioh_db
```

Modelo base:

```text
sql/schema.sql
```

Premisas:

- `cards.card_id` identifica la carta base.
- `card_sets` identifica la aparicion de una carta en set/rareza.
- `set_price` pertenece a `card_sets`.
- `set_price` no es precio propio de una rareza.
- `cardmarket_price` llega en EUR.
- `tcgplayer_price`, `ebay_price`, `amazon_price` y `coolstuffinc_price` llegan en USD.
- Los precios actuales se consumen en formato largo desde `vw_fact_card_prices_descriptive`.
- Las apariciones se consumen desde `vw_fact_card_set_appearances`.
- `vw_fact_card_prices_descriptive` tiene grano `1 carta + 1 marketplace + 1 moneda`.
- Los outliers y rankings se calculan como medidas o filtros en Power BI desde hechos base.
- Las consultas se documentaran aqui cuando se generen.

## Flujo de analisis

```text
programa Python -> carga MySQL -> tablas madre -> pregunta analitica -> consulta -> Power BI
```

Responsabilidades:

- Python carga y actualiza las tablas madre.
- MySQL conserva la fuente relacional.
- Cada pregunta o decision se formaliza en este diario antes de crear una consulta.
- Power BI consumira consultas documentadas, no reglas improvisadas.

Regla:

```text
si no hay pregunta o decision registrada, no se crea consulta
```

## Analisis descriptivo

Objetivo: entender que existe y como se distribuye.

### Catalogo de cartas disponibles

- Pregunta o decision: conocer el catalogo base disponible.
- Tablas madre: `cards`.
- Consulta correspondiente: `vw_dim_cards_descriptive`
- Estado: hecho
- Criterio de avance: conteo y segmentacion base.
- Notas: punto inicial del catalogo.

### Distribucion por tipo de carta

- Pregunta o decision: entender como se reparte el catalogo por tipo.
- Tablas madre: `cards`.
- Consulta correspondiente: `vw_dim_cards_descriptive`
- Estado: hecho.
- Criterio de avance: agrupar por `card_type` y `frame_type`.
- Notas: validar nulos y categorias.

### Cobertura de sets por carta

- Pregunta o decision: medir en cuantos sets aparece cada carta.
- Tablas madre: `cards`, `card_sets`, `sets`.
- Consulta correspondiente: `vw_fact_card_set_appearances`
- Estado: hecho.
- Criterio de avance: contar apariciones por carta y set.
- Notas: no confundir carta con impresion.

### Distribucion de precios actuales

- Pregunta o decision: describir precios actuales por marketplace.
- Tablas madre: `card_prices`.
- Consulta correspondiente: `vw_fact_card_prices_descriptive`
- Estado hecho.
- Criterio de avance: separar marketplaces y declarar moneda.
- Grano: `1 carta + 1 marketplace + 1 moneda`.
- Notas: si se comparan marketplaces, convertir moneda o segmentar EUR/USD. No calcular medias mezclando monedas.

### Modelo relacional y uso de consulta

El analisis descriptivo debe partir de entidades y recuentos simples. Las consultas de este bloque deberan exponer datos de lectura directa, con grano declarado y sin reglas comerciales.

Uso esperado de consulta:

```text
explorar catalogo -> validar cobertura -> alimentar visuales descriptivos
```

## Analisis diagnostico

Objetivo: explicar relaciones, riesgos y diferencias observadas.

### Cartas con mas apariciones en sets

- Pregunta o decision: detectar cartas con mayor presencia en sets.
- Tablas madre: `cards`, `card_sets`, `sets`.
- Consulta correspondiente: `vw_fact_card_set_appearances`
- Estado: Hecho.
- Criterio de avance: ranking por apariciones.
- Notas: interpretar como disponibilidad o reimpresion.

### Relacion entre rareza y precio de aparicion

- Pregunta o decision: analizar si ciertas rarezas aparecen asociadas a precios distintos.
- Tablas madre: `card_sets`, `rarities`.
- Consulta correspondiente: `vw_fact_card_set_appearances`
- Estado: Hecho.
- Criterio de avance: agregar con grano controlado.
- Notas: `set_price` no pertenece a `rarities`.

### Deteccion de precios extremos

- Pregunta o decision: localizar precios que exigen revision antes de interpretar.
- Tablas madre: `card_prices`.
- Consulta base: `vw_fact_card_prices_descriptive`.
- Consulta correspondiente: medida o filtro de revision en Power BI.
- Estado: Preparado desde hecho base.
- Criterio de avance: definir umbrales y revisar casos.
- Grano esperado: `1 carta + 1 marketplace + 1 moneda + 1 precio candidato`.
- Notas: no usar outliers como conclusion directa.
- Umbral inicial de trabajo: revisar `price <= 0`, `EUR >= 50` y `USD >= 50`.

### Calidad de relaciones FK

- Pregunta o decision: comprobar que las relaciones entre tablas madre son coherentes.
- Tablas madre: todas las tablas hijas.
- Consulta correspondiente: comprobaciones puntuales sobre tablas madre o consultas temporales.
- Estado: fuera del modelo relacional de Power BI.
- Criterio de avance: buscar huerfanos o claves nulas criticas.
- Criterio minimo: 0 huerfanos obligatorios, 0 duplicados de grano y revision explicita de FK nullable.
- Notas: control previo a visualizacion. Estos controles no explican negocio; validan si el modelo es fiable.

### Modelo relacional y uso de consulta

El diagnostico debe explicar por que algo destaca. Las consultas de este bloque pueden agregar o filtrar, pero deben conservar el grano y la regla de origen.

Uso esperado de consulta:

```text
detectar patrones -> explicar causa probable -> senalar riesgo de interpretacion
```

## Analisis predictivo

Objetivo: estudiar variacion temporal solo cuando haya suficientes snapshots.

### Numero de snapshots disponibles

- Pregunta o decision: saber si existe historico suficiente para analizar variacion.
- Tablas madre: `card_price_history`.
- Consulta correspondiente: `vw_dim_snapshots_descriptive`.
- Estado: Preparado.
- Criterio de avance: contar fechas distintas.
- Notas: sin minimo de historico no hay tendencia. La view no crea snapshots; el ETL los inserta en `card_price_history` en cada carga real.

### Variacion de precio por carta

- Pregunta o decision: medir cambios de precio por carta entre snapshots.
- Tablas madre: `card_price_history`, `cards`.
- Consulta correspondiente: `vw_fact_card_price_variation_predictive`.
- Estado: Hecho.
- Criterio de avance: comparar snapshots por marketplace.
- Grano esperado: `1 carta + 1 marketplace + 1 moneda + 1 snapshot con snapshot anterior comparable`.
- Notas: conservar moneda; `cardmarket_price` es EUR y el resto de marketplaces son USD. Requiere al menos dos snapshots comparables por carta y marketplace.

### Cartas con subida relevante

- Pregunta o decision: detectar subidas que merecen seguimiento.
- Tablas madre: `card_price_history`, `cards`.
- Consulta correspondiente:
- Estado: Pendiente.
- Criterio de avance: definir variacion minima.
- Notas: no convertir en recomendacion automatica.

### Modelo relacional y uso de consulta

El predictivo depende del historico real generado por el ETL. La consulta debe declarar intervalo temporal, marketplace y moneda. Si mezcla EUR/USD, debe incluir conversion explicita o separar resultados.

Uso esperado de consulta:

```text
medir variacion -> validar suficiente historico -> preparar seguimiento
```

## Analisis prescriptivo

Objetivo: convertir criterios validados en decisiones accionables.

### Seleccionar carta principal potencial

- Pregunta o decision: identificar cartas que podrian actuar como carta principal.
- Tablas madre: `cards`, `card_sets`, `card_prices`, `card_banlist`.
- Consulta correspondiente:
- Estado: Pendiente.
- Criterio de avance: combinar valor, presencia y legalidad.
- Notas: requiere reglas validadas.

### Seleccionar carta complementaria

- Pregunta o decision: identificar cartas de apoyo con sentido comercial.
- Tablas madre: `cards`, `card_sets`, `card_prices`.
- Consulta correspondiente:
- Estado: Pendiente.
- Criterio de avance: precio moderado y coherencia tematica.
- Notas: evitar criterio solo por precio.

### Marcar carta para revision

- Pregunta o decision: separar casos que no deben convertirse aun en recomendacion.
- Tablas madre: `card_sets`, `card_prices`, `card_price_history`.
- Consulta correspondiente:
- Estado: Pendiente.
- Criterio de avance: outlier, moneda mezclada o dato incompleto.
- Notas: decision de control de calidad.

### Modelo relacional y uso de consulta

El prescriptivo no debe nacer de un ranking aislado. Las consultas de este bloque deben consumir criterios ya validados en descriptivo, diagnostico y predictivo.

Uso esperado de consulta:

```text
criterio validado -> clasificacion -> decision revisable
```
