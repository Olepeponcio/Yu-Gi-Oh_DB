# 02 — Diagnostic

[Inicio](../../../../README.md) → [Diseño de views](../README.md) → Diagnostic

## Propósito

Explicar por qué una distribución o valor destaca y separar señales reales de problemas de calidad o granularidad.

## Dependencia

Consume dimensiones y hechos descriptive ya validados. No crea cruces entre hechos para “fabricar” relaciones inexistentes.

## Preguntas guía

- ¿Qué rarezas válidas se asocian con precios de impresión más altos?
- ¿Qué cartas aparecen en más sets y puede la reimpresión explicar su presencia?
- ¿Hay problemas de calidad o cobertura que invaliden esas interpretaciones?

Dispersión por marketplace, outliers, nulos, huérfanos y duplicados son controles o desgloses de estas tres preguntas; no justifican por sí solos nuevas views de negocio.

## Views candidatas

### `vw_dq_card_printings`

- Estado: propuesta.
- Uso: auditoría, no cargar en el modelo principal.
- Grano: una impresión con incidencia.
- Fuente: `card_printings`.
- Salida: claves, valor raw, calidad y tipo de incidencia.
- Aceptación: cada fila debe explicar una regla incumplida.

### `vw_dq_price_history`

- Estado: propuesta.
- Uso: localizar precios o series que requieren revisión.
- Grano: una observación de precio con incidencia.
- Fuente: `card_price_history`.
- Riesgo: convertir umbrales exploratorios en reglas de negocio permanentes.

## Decisión explícitamente descartada

No recrear `vw_fact_price_rarity_marketplace`. El precio de marketplace está a nivel de carta y la rareza a nivel de impresión. Unir ambos por `card_id` replica el precio y genera outliers falsos.

## Preferencia de cálculo

Mediana, IQR, ratio de outlier, dispersión y rankings se implementarán como medidas sobre hechos base salvo que una prueba de rendimiento justifique materialización posterior.
