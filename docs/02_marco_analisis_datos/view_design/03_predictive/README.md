# 03 — Predictive

[Inicio](../../../../README.md) → [Diseño de views](../README.md) → Predictive

## Propósito

Estudiar evolución y variación temporal. “Predictive” no implica pronóstico automático: primero exige histórico suficiente, comparable y estable.

## Preguntas guía

- ¿Qué tendencias aparecen entre snapshots comparables?
- ¿Qué cartas muestran variaciones relevantes por marketplace y moneda?

El número de snapshots, intervalo, huecos y origen de conversión son condiciones de validez de estas preguntas, no preguntas analíticas independientes.

## Backlog

### `vw_fact_card_price_history`

- Estado: propuesta.
- Fuente: `card_price_history`.
- Grano: carta + marketplace + moneda + snapshot.
- Clave: `price_history_id`; clave de negocio igual al grano.
- FK: `card_id`, `marketplace_id`, `currency_code`.
- Medidas: `price`, `exchange_rate` cuando proceda.
- Aceptación: cero duplicados del grano y snapshots explícitos.

### `vw_fact_card_price_changes`

- Estado: candidata condicionada.
- Pregunta: ¿cuánto cambió cada serie frente a su observación anterior?
- Grano: serie + snapshot con observación previa.
- Técnica prevista: `LAG()` particionado por carta, marketplace y moneda.
- Campos derivados: snapshot anterior, días transcurridos, cambio absoluto y relativo.
- Riesgo: comparar intervalos temporales diferentes como si fueran equivalentes.
- Criterio: crearla solo si el cálculo en Power BI resulta opaco o costoso.

## Umbrales antes de hablar de tendencia

Se deben acordar y registrar:

- mínimo de snapshots por serie;
- ventana temporal mínima;
- tolerancia a huecos;
- tratamiento de precio cero;
- separación entre datos API y conversión monetaria.

Sin esos acuerdos solo se describen variaciones históricas; no se etiqueta una predicción.
